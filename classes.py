from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Vocab(ABC):
    topic: int
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


@dataclass
class VocabB(Vocab):
    part: int
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


@dataclass
class VocabA1(Vocab):
    lesson: int

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


@dataclass
class VocabA2(Vocab):
    lesson: int

    kana: str
    kanji: str

    accent: str
    dictionary_form: Optional[str]
    verb_group: Optional[int]
    word_type: str

    def get_kana_with_translation(self) -> Tuple[str, str]:
        return self.kana.strip(), self.translation.strip()

    def get_kanji(self) -> str:
        return self.kanji.strip()

    def get_main_japanese(self) -> str:
        return self.kana
