from resma.annotate.infrastructure.note_file_repository import NoteFilesRepository
from resma.annotate.use_cases.create_template_note.interactors import CreateTemplateNoteInteractor, ReferenceTemplateNoteInteractor
from resma.ingest.infrastructure.ingest_internet_gateway import IngestInternetGateway
from resma.ingest.use_cases.create_reference.controllers import ClickIngestController
from resma.shared.infrastructure.curl_internet_gateway import CurlInternetGateway
from resma.shared.infrastructure.file_system_cache import FileSystemCache
from resma.shared.infrastructure.playwright_internet_gateway import PlaywrightInternetGateway
from resma.shared.infrastructure.template_file_repository import FileTemplatesRepository
from resma.shared.interfaces.interactors import ConfigurationInteractor


def make_ingest_reference_controller(*, config: ConfigurationInteractor, cache_dir: str):
    cache_interactor = FileSystemCache(cache_dir=cache_dir)
    return ClickIngestController(
        ref_template_interactor=CreateTemplateNoteInteractor(
            notes_repo=NoteFilesRepository(),
            templates_repo=FileTemplatesRepository(),
            config=config,
            note_template_interactor=ReferenceTemplateNoteInteractor(),
        ),
        internet_gateway=IngestInternetGateway(
            app_internet_gateway=PlaywrightInternetGateway(
                cache_interactor=cache_interactor),
            page_internet_gateway=CurlInternetGateway(
                cache_interactor=cache_interactor),
        ),
    )
