
from selectolax.parser import HTMLParser
from resma.shared.infrastructure.interactors import InternetFetcherGateway


class IngestInternetGateway(InternetFetcherGateway):
    APP_DOMAINS = (
        'youtube.com', 'youtu.be',
        'reddit.com',
        'instagram.com',
        'dev.to',
        'medium.com',
        'spotify',
        'chat.openai.com',
    )

    def __init__(
            self, *,
            app_internet_gateway: InternetFetcherGateway,
            page_internet_gateway: InternetFetcherGateway,
    ):
        self.app_internet_gateway = app_internet_gateway
        self.page_internet_gateway = page_internet_gateway

    def _is_app(self, url: str):
        domain = self.get_domain(url=url)
        return any(
            app_domain in domain
            for app_domain in IngestInternetGateway.APP_DOMAINS
        )

    def _get_gateway(self, url: str):
        if self._is_app(url):
            return self.app_internet_gateway
        return self.page_internet_gateway

    def _fetch(self, url):
        gateway = self._get_gateway(url)
        return gateway._fetch(url=url)

    def get_metadata(self, *, url: str):
        metadata = super().get_metadata(url=url) or {}
        content = self.get_content(url=url)
        if content:
            dom = HTMLParser(content)
            metadata['title'] = dom.root.css_first('title').text()
        return metadata
