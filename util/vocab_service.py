import csv
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List

from util.classes import Vocab
from util.config import Config
from util.excel_import import get_vocab_list_by_filenames
from util.vocab_generation import get_new_words, filter_duplicates


@dataclass
class VocabService:
    level: str
    language: str
    config: Config

    def retrieve_and_write_vocabulary(self):
        new_words_sorted = self.retrieve_vocabulary()
        self.write_vocabulary(new_words_sorted)

    def retrieve_vocabulary(self):
        new_words_for_lesson: List[Vocab] = self.get_new_vocabulary()
        new_words_sorted: List[Vocab] = sorted(new_words_for_lesson, key=lambda x: x.get_lesson_name())
        return new_words_sorted

    def get_new_vocabulary(self):
        new_urls = self.config.get_urls(self.level, self.language)
        previous_level = self.config.get_previous_level(self.level)

        old_urls: list[str] = []
        if previous_level is not None:
            old_urls = self.config.get_urls(previous_level, self.language)

        return self.get_new_vocabulary_by_filenames(previous_level, new_urls, old_urls)

    def get_new_vocabulary_by_filenames(self, prev_level: str, new_filenames: list[str],
                                        old_filenames: list[str]):
        vocabs_for_previous_level = get_vocab_list_by_filenames(old_filenames, prev_level)
        vocabs_for_selected_level = get_vocab_list_by_filenames(new_filenames, self.level)
        new_vocabs = get_new_words(vocabs_for_previous_level, vocabs_for_selected_level)
        new_words_without_duplicates = filter_duplicates(new_vocabs)
        return new_words_without_duplicates

    def write_vocabulary(self, new_words_sorted):
        for group, l in itertools.groupby(new_words_sorted, lambda x: x.get_lesson_name()):
            out_folder = f"out/excel/{self.level}/{group}"
            VocabService.create_out_folder(out_folder)
            with open(f'{out_folder}/cards.csv', 'w') as file:
                writer = csv.writer(file, delimiter=';')
                for vocab in l:
                    writer.writerow(vocab.get_csv_row())
            print(group, len(list(l)))

    @staticmethod
    def create_out_folder(out_folder):
        Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)
