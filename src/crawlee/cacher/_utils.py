import os
import re


def iterate_name(base_path: str, prefix: str = 'cached', extension: str = '.html') -> str:
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
