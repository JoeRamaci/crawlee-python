import json


def build_router(url: str, cache_path: str, router_path: str) -> None:
    """Build a json file that acts as a 'router' for which pages have been cached.

    Page only cached once in key/value format:
    {
        "url": "https://crawlee.dev",
        "cache":"file_path"
    }
    """
    data = {'url': url, 'path': cache_path}
    with open(f'{router_path}', 'a') as f:
        f.write(json.dumps(data) + '\n')


def check_router(url: str, router_path: str) -> bool:
    """Check whether the target URL has been cached in the router."""
    try:
        with open(f'{router_path}') as f:
            data = []
            for line in f:
                stripped_line = line.strip()
                if not stripped_line:  # empty strings, lists, dicts, etc are falsy in Python
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # any() returns True when matching value found; otherwise, False
        return any(entry.get('url') == url for entry in data)
    except FileNotFoundError:
        return False  # if the file doesn't exist, url probably isn't written down anywhere
