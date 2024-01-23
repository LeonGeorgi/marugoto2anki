import json
from dataclasses import dataclass

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
        try:
            with open(filename, 'r') as f:
                try:
                    config = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    if e.lineno == 1 and e.colno == 1:
                        # Empty config.json, might need better handling
                        config = dict()
                    else:
                        raise e
        except FileNotFoundError:
            # No config found, so just populate it with default values
            config = dict()

        if 'anki_user' not in config:
            config["anki_user"] = "User 1"
        
        # Use default platform path if not specified
        # https://docs.ankiweb.net/files.html
        if 'anki_path' not in config:
            if platform == "linux" or platform == "linux2":
                # File path of recent linux version
                config['anki_path'] = os.path.expanduser('~/.local/share/Anki2/') # Linux
            elif platform == "darwin":
                config['anki_path'] = os.path.expanduser('~/Library/Application Support/Anki2/') # MacOs
            elif platform == "win32":
                config['anki_path'] = os.path.join(os.getenv('APPDATA'), 'Anki2') # Windows
        else:
            config['anki_path'] = os.path.expanduser(config['anki_path']) # Make sure a full path is stored in config

        if 'card_model' not in config:
            config['card_model'] = "Vocabulary Simple"

        return Config(config['anki_user'], config['anki_path'], config['card_model'])