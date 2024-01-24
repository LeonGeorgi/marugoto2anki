from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional

from util.string_utils import convert_lesson, calculate_topic, convert_pronunciation, convert_pronunciation_to_kana


@dataclass
class Vocab(ABC):
    lesson_hierarchy: Tuple[str, ...]
    uid: str
    kanji: str
    kana: str
    translation: str
    accent: Optional[str]
    romaji: Optional[str]
    word_type: Optional[str]
    dictionary_form: Optional[str]
    verb_group: Optional[str]
    comment: Optional[str]
    comment_translation: Optional[str]
    sort_id: str

    @abstractmethod
    def get_main_japanese(self) -> str:
        pass

    def get_csv_row(self) -> Tuple:
        return (
            self.uid,
            '-'.join(self.lesson_hierarchy),
            self.kana,
            self.kanji,
            self.translation,
            self.accent,
            self.romaji,
            self.comment,
            self.comment_translation,
            self.word_type,
            self.dictionary_form,
            self.verb_group,
        )


@dataclass
class VocabB(Vocab):
    def get_main_japanese(self) -> str:
        return self.kanji

    @staticmethod
    def from_table_row(row: Tuple) -> 'VocabB':
        word_id, topic, part, japanese, raw_accent, translation, comment, comment_translation, page = row
        accent = convert_pronunciation(raw_accent)
        vocab_id = str(int(float(word_id)))
        return VocabB((topic, part),
                      vocab_id,
                      japanese.strip(),
                      convert_pronunciation_to_kana(accent).strip(),
                      translation.strip(),
                      accent.strip(),
                      None,
                      None,
                      None,
                      None,
                      comment.strip() if not comment == 'nan' else None,
                      comment_translation.strip() if not comment_translation == 'nan' else None,
                      vocab_id)


@dataclass
class VocabA1(Vocab):
    def get_main_japanese(self) -> str:
        return self.kana

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str]):
        word_id, kana, kanji, accent, romaji, translation, lesson, word_type, _ = row
        reformatted_lesson = convert_lesson(lesson)
        topic = calculate_topic(lesson)
        return VocabA1((topic, reformatted_lesson),
                       word_id.strip(),
                       kanji.strip(),
                       kana.strip(),
                       translation.strip(),
                       accent.strip(),
                       romaji.strip(),
                       word_type.strip(),
                       None,
                       None,
                       None,
                       None,
                       word_id.strip())


@dataclass
class VocabA2(Vocab):

    def get_main_japanese(self) -> str:
        return self.kana

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str, str]):
        word_id, kana, kanji, accent, dictionary_form, verb_group, translation, lesson, word_type = row[:9]
        reformatted_lesson = convert_lesson(lesson)
        topic = calculate_topic(lesson)
        return VocabA2((topic, reformatted_lesson),
                       word_id.strip(),
                       kanji.strip(),
                       kana.strip(),
                       translation.strip(),
                       accent.strip(),
                       None,
                       word_type.strip(),
                       dictionary_form.strip(),
                       verb_group.strip(),
                       None,
                       None,
                       word_id.strip())


@dataclass
class VocabA2B1(Vocab):
    kana: str
    kanji: str

    accent: str
    dictionary_form: str
    verb_group: str
    word_type: str

    def get_main_japanese(self) -> str:
        return self.kana

    @staticmethod
    def from_table_row(row: tuple[str, str, str, str, str, str, str, str, str, str]):
        word_id, kana, kanji, accent, dictionary_form, verb_group, translation, topic, word_type, _ = row
        reformatted_topic = convert_lesson(topic)
        return VocabA2B1((reformatted_topic,),
                         word_id.strip(),
                         kanji.strip(),
                         kana.strip(),
                         translation.strip(),
                         accent.strip(),
                         None,
                         word_type.strip(),
                         dictionary_form.strip(),
                         verb_group.strip(),
                         None,
                         None,
                         word_id.strip())
