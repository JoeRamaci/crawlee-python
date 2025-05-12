import os

import requests

from . import _cached_router, _utils


# refactor entire cacher module as Object Oriented?
def cache(url: str) -> None:
    """Cache pure HTML webpage. Build out json file to act as a router for the cached pages."""
    base_path = 'cache'
    os.makedirs(f'{base_path}', exist_ok=True)

    router_path = f'{base_path}/router.json'
    cache_path = _utils.iterate_name(base_path=base_path)

    if _cached_router.check_router(url, router_path):
        return  # Skip downloading or writing again

    _cached_router.build_router(url, cache_path, router_path)  # if here, url isnt accessed before

    response = requests.get(url, timeout=10)
    html_content = response.text  # HTML as str

    with open(f'{cache_path}', 'a', encoding='utf-8') as f:
        f.write(html_content)


def batch_cache(urls: list[str]) -> None:
    """Cache multiple URLs by calling `cache` in a loop."""
    for url in urls:
        cache(url)
