from dataclasses import dataclass
from typing import List

from util.classes import Vocab
from util.config import Urls
from util.excel_import import get_vocab_list_by_filenames
from util.vocab_utils import get_new_words, filter_duplicates


@dataclass
class VocabService:
    level: str
    language: str
    level_urls: Urls

    def retrieve_vocabulary(self):
        new_words_for_lesson: List[Vocab] = self.get_new_vocabulary()
        new_words_sorted: List[Vocab] = sorted(new_words_for_lesson, key=lambda x: x.lesson_hierarchy)
        return new_words_sorted

    def get_new_vocabulary(self):
        new_urls = self.level_urls.get_urls(self.level, self.language)
        previous_level = self.level_urls.get_previous_level(self.level)

        previous_level_urls: list[str] = []
        if previous_level is not None:
            previous_level_urls = self.level_urls.get_urls(previous_level, self.language)

        return self.get_new_vocabulary_by_filenames(previous_level, new_urls, previous_level_urls)

    def get_new_vocabulary_by_filenames(self, prev_level: str, new_filenames: list[str],
                                        old_filenames: list[str]):
        vocabs_for_previous_level = get_vocab_list_by_filenames(old_filenames, prev_level)
        vocabs_for_selected_level = get_vocab_list_by_filenames(new_filenames, self.level)
        new_vocabs = get_new_words(vocabs_for_previous_level, vocabs_for_selected_level)
        new_words_without_duplicates = filter_duplicates(new_vocabs)
        return new_words_without_duplicates
