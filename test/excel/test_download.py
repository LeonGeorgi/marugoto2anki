import random
import unittest
from pathlib import Path

from requests import HTTPError

from util.excel.download import generate_filename, download_file, get_or_create_cache_path


class DownloadTest(unittest.TestCase):
    def test_generate_filename(self):
        url = "https://www.marugoto.org/assets/docs/teacher/resource/starter_a/starter_activities_vocabulary_index_en.xlsx"
        filename = generate_filename(url)
        self.assertEqual('starter_activities_vocabulary_index_en.xlsx', filename)

    def test_download_file(self):
        url = "https://www.marugoto.org/assets/docs/teacher/resource/starter_a/starter_activities_vocabulary_index_EN.xlsx"
        path = Path(f'/tmp/starter_activities_vocabulary_index_EN_{random.randint(0, 1_000_000)}.xlsx')
        download_file(url, path)
        self.assertTrue(path.is_file(), f'File "{path.name}" not found.')

    def test_download_file_with_invalid_url(self):
        url = "https://www.marugoto.org/assets/docs/teacher/resource/starter_a/abcd.xlsx"
        path = Path(f'/tmp/abcd_{random.randint(0, 1_000_000)}.xlsx')
        self.assertRaises(HTTPError, lambda: download_file(url, path))

    def test_get_or_create_cache_path(self):
        cache_path = get_or_create_cache_path()
        self.assertTrue(cache_path.is_dir())
        self.assertEqual('cache', cache_path.name)


if __name__ == '__main__':
    unittest.main()
