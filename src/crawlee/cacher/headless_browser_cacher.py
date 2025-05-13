import os

import anyio
from playwright.async_api import async_playwright

from . import _cached_router, _utils


async def browser_cache(url: str) -> None:
    """Cache HTML page using a headless browser (Playwright).

    Build out json file to act as a router for the cached pages.
    """
    base_path = 'cache'
    os.makedirs(base_path, exist_ok=True)

    router_path = os.path.join(base_path, 'router.json')
    cache_path = _utils.iterate_name(base_path=base_path)

    if _cached_router.check_router(url, router_path):
        return  # Already cached

    _cached_router.build_router(url, cache_path, router_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until='networkidle', timeout=15000)
            html_content = await page.content()
        except Exception:
            await browser.close()
            return

        async with await anyio.open_file(cache_path, 'w', encoding='utf-8') as f:
            await f.write(html_content)

        await browser.close()


async def batch_browser_cache(urls: list[str]) -> None:
    """Cache multiple URLs via Playwright."""
    for url in urls:
        await browser_cache(url)
