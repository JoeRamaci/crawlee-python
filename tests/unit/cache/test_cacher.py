import json
import os
import tempfile

from crawlee.cacher import _cached_router, _utils


def test_build_router_creates_entry() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        router_path = os.path.join(tmpdir, 'router.json')
        url = 'https://example.com'
        cache_path = '/cache/example1.html'

        _cached_router.build_router(url, cache_path, router_path)

        with open(router_path) as f:
            lines = f.readlines()
            assert len(lines) == 1
            data = json.loads(lines[0])
            assert data['url'] == url
            assert data['path'] == cache_path


def test_check_router_detects_url() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        router_path = os.path.join(tmpdir, 'router.json')
        entries = [
            {'url': 'https://example.com', 'path': '/cache/example1.html'},
            {'url': 'https://other.com', 'path': '/cache/example2.html'},
        ]
        with open(router_path, 'w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        assert _cached_router.check_router('https://example.com', router_path) is True
        assert _cached_router.check_router('https://notfound.com', router_path) is False


def test_iterate_name_generates_incremented_filename() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        filenames = ['cached1.html', 'cached2.html', 'cached10.html']
        for name in filenames:
            open(os.path.join(tmpdir, name), 'w').close()

        new_filename = _utils.iterate_name(base_path=tmpdir)
        assert new_filename.endswith('cached11.html')
