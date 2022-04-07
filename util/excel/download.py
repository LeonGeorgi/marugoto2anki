from pathlib import Path

import requests


def download_or_get_cached_file(url: str) -> Path:
    path = _get_path_for_url(url)
    if not path.is_file():
        print(f"Downloading {url}")
        download_file(url, path)
    return path


def download_file(url: str, path: Path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def _get_path_for_url(url):
    filename = generate_filename(url)
    path = Path(get_or_create_cache_path() / filename)
    return path


def generate_filename(url: str):
    return url.split('/')[-1]


def get_or_create_cache_path() -> Path:
    path = Path('./cache/')
    path.mkdir(parents=True, exist_ok=True)
    return path
