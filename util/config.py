import json
from dataclasses import dataclass


@dataclass
class Config:
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
            config = json.load(f)
        return Config(config['levels'], config['urls'])
