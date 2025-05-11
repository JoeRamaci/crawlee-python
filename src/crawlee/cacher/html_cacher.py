import os
import re

import requests

from . import _cached_router


# refactor entire cacher module as Object Oriented?
def cache(url: str) -> None:
    """Cache pure HTML webpage. Build out json file to act as a router for the cached pages."""
    base_path = 'cache'
    os.makedirs(f'{base_path}', exist_ok=True)

    router_path = f'{base_path}/router.json'
    cache_path = _iterate_name(base_path=base_path)

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


def _iterate_name(base_path: str, prefix: str = 'cached', extension: str = '.html') -> str:
    """Return a new iterated filename like 'cached1.html', 'cached2.html', etc. down the cache/cached*.html path."""
    existing_files = os.listdir(base_path)  # get all files in dir
    max_index = 0

    # Regex pattern to match filenames like cached123.html
    # .escape: handles escape characters. //d: at least 1 digit
    pattern = re.compile(f'{re.escape(prefix)}(\\d+){re.escape(extension)}')

    for f_name in existing_files:
        match = pattern.fullmatch(f_name)  # match exclusively to the compiled pattern- no substring matches
        if match:
            index = int(match.group(1))  # grab the number, cast -> int
            max_index = max(max_index, index)

    new_index = max_index + 1
    return os.path.join(base_path, f'{prefix}{new_index}{extension}')  # returns path string
