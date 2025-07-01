import pycurl
from io import BytesIO

from resma.shared.infrastructure.decorators import cacheable
from resma.shared.infrastructure.interactors import InternetFetcherGateway


class CurlInternetGateway(InternetFetcherGateway):
    @cacheable(key='url')
    def _fetch(self, url: str):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, (
            'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language: en-US,en;q=0.6',
            'cache-control: max-age=0',
            'sec-ch-ua-mobile: ?0',
            'sec-fetch-dest: document',
            'sec-fetch-mode: navigate',
            'sec-fetch-site: same-origin',
            'sec-fetch-user: ?1',
            'sec-gpc: 1',
            'service-worker-navigation-preload: true',
            'upgrade-insecure-requests: 1'
        ))
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.ACCEPT_ENCODING, '')
        c.setopt(pycurl.NOSIGNAL, 1)

        c.setopt(pycurl.WRITEDATA, buffer)
        c.perform()
        body = buffer.getvalue().decode('utf-8', errors='replace')
        result = {
            'html': body,
            'mimetype': c.getinfo(pycurl.CONTENT_TYPE),
            'metadata': {}
        }
        c.close()
        return result
