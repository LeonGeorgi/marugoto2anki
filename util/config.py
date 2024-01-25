import json
from dataclasses import dataclass
from configparser import ConfigParser, NoSectionError, NoOptionError

import os
from sys import platform

from util.vocab_export import  VocabExporter, AnkiExporter, FileExporter,GenankiExporter


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
    exporter: VocabExporter

    @staticmethod
    def parse_file(filename: str):
        config = ConfigParser()
        config.read(filename)

        exporter = Config.parse_exporter_config(config)

        return Config(exporter)

    @staticmethod
    def parse_exporter_config(config: ConfigParser) -> VocabExporter:
        exporter_type = config.get('anki', 'exporter', fallback='anki')

        exporter_dict = {
            'anki': Config.parse_anki_exporter_config,
            'file': Config.parse_file_exporter_config,
            'genanki': Config.parse_genanki_exporter_config
        }

        if exporter_type in exporter_dict:
            return exporter_dict[exporter_type](config)
        else:
            print(f'Invalid exporter name. "{exporter_type}" The following are available: {exporter_dict.keys()}')
            raise ValueError

    @staticmethod
    def parse_anki_exporter_config(config: ConfigParser) -> AnkiExporter:
        anki_default_paths = {
            "linux": lambda: os.path.expanduser("~/.local/share/Anki2/"),
            "linux2": lambda: os.path.expanduser("~/.local/share/Anki2/"),
            "darwin": lambda: os.path.expanduser("~/Library/Application Support/Anki2/"),
            "win32": lambda: os.path.join(os.getenv('APPDATA'), 'Anki2')
        }

        anki_user = config.get('exporter.anki', 'user', fallback='User 1')
        try:
            anki_path = os.path.expanduser(config.get('exporter.anki', 'path'))
        except (KeyError, NoSectionError, NoOptionError):
            anki_path = anki_default_paths[platform]()
        
        anki_deck = config.get('exporter.anki', 'deck', fallback='Vocabulary::Japanese')
        card_model = config.get('exporter.anki', 'card_model', fallback='Vocabulary Simple')

        return AnkiExporter(anki_user, anki_path, anki_deck, card_model)

    @staticmethod
    def parse_file_exporter_config(config: ConfigParser) -> FileExporter:
        output_folder = config.get('exporter.file', 'out', fallback='out')

        return FileExporter(output_folder)

    @staticmethod
    def parse_genanki_exporter_config(config: ConfigParser) -> GenankiExporter:
        anki_deck = config.get('exporter.genanki', 'deck', fallback='Vocabulary::Japanese')
        card_model = config.get('exporter.genanki', 'card_model', fallback='Vocabulary Simple')

        output_folder = config.get('exporter.genanki', 'out', fallback='out')

        return GenankiExporter(anki_deck, card_model, output_folder)