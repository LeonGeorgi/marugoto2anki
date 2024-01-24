import json
from dataclasses import dataclass
from configparser import ConfigParser, NoSectionError

import os
from sys import platform


@dataclass
class Urls:
    available_levels: list[str]
    level_urls: dict[str, dict[str, list[str]]]

    def get_available_languages_for_level(self, level: str):
        return set(self.level_urls[level].keys())

    def get_available_languages_for_this_and_previous_level(self, level: str):
        previous_level = self.get_previous_level(level)
        return self.get_available_languages_for_level(level).intersection(
            self.get_available_languages_for_level(previous_level)
        )

    def get_urls(self, level: str, language: str):
        return self.level_urls[level][language]

    def get_previous_level(self, level: str):
        level_index = self.available_levels.index(level)
        previous_level = None
        if level_index != 0:
            previous_level = self.available_levels[level_index - 1]

        return previous_level

    @staticmethod
    def parse_file(filename: str):
        with open(filename, 'r') as f:
            urls = json.load(f)
        return Urls(urls['levels'], urls['urls'])


@dataclass
class Config:
    anki_user: str
    anki_path: str

    card_model: str

    @staticmethod
    def parse_file(filename: str):
        anki_default_paths = {
            "linux": lambda: os.path.expanduser("~/.local/share/Anki2/"),
            "linux2": lambda: os.path.expanduser("~/.local/share/Anki2/"),
            "darwin": lambda: os.path.expanduser("~/Library/Application Support/Anki2/"),
            "win32": lambda: os.path.join(os.getenv('APPDATA'), 'Anki2')
        }

        config = ConfigParser()
        config.read(filename)
        anki_user = config.get('anki', 'user', fallback='User 1')
        try:
            anki_path = os.path.expanduser(config.get('anki', 'path'))
        except (KeyError, NoSectionError):
            anki_path = anki_default_paths[platform]()
        anki_card_model = config.get('anki', 'card_model', fallback='Vocabulary Simple')

        return Config(anki_user, anki_path, anki_card_model)
