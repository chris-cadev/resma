import re
from typing import Optional

from furl import furl
from resma.annotate.use_cases.note.interactors import NoteInteractor
from resma.ingest.interfaces.interactors import IngestInteractor
from resma.shared.infrastructure.interactors import InternetGateway
from resma.shared.interfaces.dto import FileDTO, TextFileWithContentDTO


class ClickIngestController(IngestInteractor):
    CREATE_REFERENCE_URL_REGEX = r'^https?://(?:www\.)?[a-zA-Z0-9_-]+(?:\.[a-zA-Z]{2,6})+(?:/\S*)?$'

    def __init__(self, *, ref_template_interactor: NoteInteractor, internet_gateway: InternetGateway):
        super().__init__()
        self.ref_template_interactor = ref_template_interactor
        self.internet_gateway = internet_gateway

    def create_reference(self, *, url: str, vault: Optional[str]) -> TextFileWithContentDTO:
        if not self._is_url_to_create_reference(url):
            raise ValueError(f"Invalid URL '{url}'")
        title = self.internet_gateway.get_metadata(url=url).get('title', '')
        if not title:
            title = self._normalize_url_as_filename(url)
        metadata = {
            'url': url,
            'author': None
        }
        return self.ref_template_interactor.execute(
            name=title,
            vault=vault,
            template='reference',
            meta=metadata,
        )

    def create_media_file(self, *, url: str, vault: Optional[str]) -> FileDTO:
        raise NotImplementedError()

    def _is_url_to_create_reference(self, url: str):
        return re.match(ClickIngestController.CREATE_REFERENCE_URL_REGEX, url.strip()) is not None

    def _normalize_url_as_filename(self, url: str) -> str:
        f = furl(url)
        domain = f.host or 'unknown'
        path = f.path.segments

        if not path:
            path = ['home']

        parts = [domain] + path
        parts = [re.sub(r'[^a-zA-Z0-9_\-]', '_', p) for p in parts]
        filename = '__'.join(parts)
        filename = re.sub(r'_+', '_', filename).strip('_').lower()

        # Max filename length to be safe across systems
        max_length = 255
        filename = filename[:max_length]

        # Windows/macOS reserved names and characters
        forbidden_names = {
            "con", "prn", "aux", "nul",
            *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))
        }

        if filename.split('__')[0] in forbidden_names:
            filename = f"file__{filename}"

        forbidden_chars = r'[<>:"/\\|?*\x00-\x1F]'
        filename = re.sub(forbidden_chars, '_', filename)

        return filename.lower()
