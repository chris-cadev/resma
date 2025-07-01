from resma.ingest.infrastructure.ingest_internet_gateway import IngestInternetGateway
from resma.shared.infrastructure.curl_internet_gateway import CurlInternetGateway
from resma.shared.infrastructure.file_system_cache import FileSystemCache
from resma.shared.infrastructure.playwright_internet_gateway import PlaywrightInternetGateway
from resma.shared.interfaces.factories.cache_path_factory import make_cache_path


def make_ingest_internet_gateway():
    cache_dir = make_cache_path()
    return IngestInternetGateway(
        app_internet_gateway=PlaywrightInternetGateway(),
        page_internet_gateway=CurlInternetGateway(),
        cache_interactor=FileSystemCache(cache_dir=cache_dir)
    )