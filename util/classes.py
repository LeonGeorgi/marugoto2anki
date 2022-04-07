from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional

from util.string_utils import convert_lesson, calculate_topic


@dataclass
class Vocab(ABC):
    id: str
    topic: str
    translation: str

    @abstractmethod
    def get_kana_with_translation(self) -> Tuple[str, str]:
        pass

    @abstractmethod
    def get_kanji(self) -> str:
        pass

    @abstractmethod
    def get_main_japanese(self) -> str:
        pass

    @abstractmethod
    def get_lesson_name(self) -> str:
        pass

    @abstractmethod
    def get_csv_row(self) -> Tuple:
        pass


@dataclass
class VocabB(Vocab):
    part: str
    japanese: str
    pronunciation: str
    comment: Optional[str]
    comment_translation: Optional[str]

    def get_kana_with_translation(self) -> Tuple[str, str]:
        return self.japanese.strip(), self.translation.strip()

    def get_kanji(self) -> str:
        return self.japanese.strip()

    def get_main_japanese(self) -> str:
        return self.japanese

    def get_lesson_name(self) -> str:
        return f"{self.topic}-{self.part}"


@dataclass
class VocabA1(Vocab):
    def get_csv_row(self) -> Tuple:
        # TODO
        pass

    lesson: str

    kana: str
    kanji: str
    accent: str
    romaji: str

    word_type: str

    def get_kana_with_translation(self) -> Tuple[str, str]:
        return self.kana.strip(), self.translation.strip()

    def get_kanji(self) -> str:
        return self.kanji.strip()

    def get_main_japanese(self) -> str:
        return self.kana

    def get_lesson_name(self) -> str:
        return f"{self.topic}-{self.lesson}"

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str]):
        card_id, kana, kanji, accent, romaji, translation, lesson, word_type, _ = row
        reformatted_lesson = convert_lesson(lesson)
        topic = calculate_topic(lesson)
        return VocabA1(card_id, topic, translation, reformatted_lesson, kana, kanji, accent, romaji, word_type)


@dataclass
class VocabA2(Vocab):
    lesson: str

    kana: str
    kanji: str

    accent: str
    dictionary_form: str
    verb_group: str
    word_type: str

    def get_kana_with_translation(self) -> Tuple[str, str]:
        return self.kana.strip(), self.translation.strip()

    def get_kanji(self) -> str:
        return self.kanji.strip()

    def get_main_japanese(self) -> str:
        return self.kana

    def get_lesson_name(self) -> str:
        return f"{self.topic}-{self.lesson}"

    def get_csv_row(self) -> Tuple:
        return (
            self.id,
            self.topic,
            self.lesson,
            self.kana,
            self.kanji if self.kanji != self.kana else "",
            self.translation,
            self.accent,
            self.verb_group,
            self.dictionary_form,
            self.word_type
        )

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str, str]):
        word_id, kana, kanji, accent, dictionary_form, verb_group, translation, lesson, word_type, _ = row
        reformatted_lesson = convert_lesson(lesson)
        topic = calculate_topic(lesson)
        return VocabA2(word_id, topic, translation, reformatted_lesson, kana, kanji, accent, dictionary_form, verb_group, word_type)


@dataclass
class VocabA2B1(Vocab):
    kana: str
    kanji: str

    accent: str
    dictionary_form: str
    verb_group: str
    word_type: str

    def get_kana_with_translation(self) -> Tuple[str, str]:
        return self.kana.strip(), self.translation.strip()

    def get_kanji(self) -> str:
        return self.kanji.strip()

    def get_main_japanese(self) -> str:
        return self.kana

    def get_lesson_name(self) -> str:
        return f"{self.topic}"

    def get_csv_row(self) -> Tuple:
        return (
            self.id,
            self.topic,
            '',
            self.kana,
            self.kanji if self.kanji != self.kana else "",
            self.translation,
            self.accent,
            self.verb_group,
            self.dictionary_form,
            self.word_type
        )

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str, str]):
        word_id, kana, kanji, accent, dictionary_form, verb_group, translation, topic, word_type, _ = row
        reformatted_topic = convert_lesson(topic)
        return VocabA2B1(word_id, reformatted_topic, translation, kana, kanji, accent, dictionary_form, verb_group, word_type)
