import time
from playwright.sync_api import sync_playwright

from resma.shared.infrastructure.decorators import cacheable
from resma.shared.infrastructure.interactors import InternetFetcherGateway


class PlaywrightInternetGateway(InternetFetcherGateway):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    PAGE_WAIT_SECS = 2.5

    @cacheable(key='url')
    def _fetch(self, url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                user_agent=PlaywrightInternetGateway.USER_AGENT)
            page = context.new_page()

            page.set_extra_http_headers({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'en-US,en;q=0.6',
                'cache-control': 'max-age=0',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'service-worker-navigation-preload': 'true',
                'upgrade-insecure-requests': '1'
            })

            page.goto(url)

            page.wait_for_load_state('domcontentloaded')
            time.sleep(PlaywrightInternetGateway.PAGE_WAIT_SECS)
            return {
                'html': page.content(),
                'mimetype': page.request.headers()['Content-Type'],
                'metadata': {
                    'title': page.title(),
                }
            }
