import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from urllib import request

import pandas as pd
import requests


def main():
    levels = ["A1", "A2-1", "A2-2"]
    while True:
        selected_level = input(f"level ({','.join(levels)}): ").strip().upper()
        if selected_level in levels:
            break
    levels_to_exclude = [level for level in levels if level != selected_level]
    learn_ex = ",".join(levels_to_exclude)
    lesson = input("lesson: ")

    words = request_marugoto_words(learn_ex, lesson, selected_level)
    print(len(words), "words found.")
    if not words:
        return

    out_folder = f"out/{selected_level}/lesson-{lesson}"
    create_out_folder(out_folder)

    print("Translate to German")
    with open(f'{out_folder}/cards.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        for entry in words:
            audio_id: str = entry["RAWID"]
            kana: str = entry["KANA"]
            kanji = entry["KANJI"]
            romaji = entry["ROMAJI"]
            english = entry["UWRD"]
            german = input(f"{kana} {english}: ")

            audio_filename = download_marugoto_audio(audio_id, out_folder, selected_level)
            writer.writerow([kana, english, german, romaji, kanji, f"[sound:{audio_filename}]"])


def download_marugoto_audio(audio_id: str, out_folder: str, level: str) -> str:
    """
    Download a Marugoto audio file and save ot to the "audio" folder in the ``out_folder``:

    :param audio_id: audio id of the word
    :param out_folder: folder to save the mp3 in
    :param level: Marugoto level
    :return: the file name
    """
    url_level = level.replace('-', '')
    audio_url = f"https://words.marugotoweb.jp/res/keyword/audio/{url_level}W/{audio_id.replace('-', 'W_')}.mp3"
    request.urlretrieve(audio_url, f"{out_folder}/media/{audio_id}.mp3")
    return f"{audio_id}.mp3"


def create_out_folder(out_folder):
    Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)


def request_marugoto_words(learn_ex, ls, lv) -> list:
    """
    Download words from https://words.marugotoweb.jp/SearchCategoryAPI.
    Available URL parameters (with example values) are:

    * m (20) - items per page
    * p (1) - page number
    * lv (A2-2) - Marugoto level
    * ls (1) - Marugoto lesson
    * tp (1) - unknown
    * tx (act,comp) - comp=Rikai, act=Katsudoo
    * learn_ex (A1,A2-1) - exclude words of previous levels
    * ut (en) - translation language

    The resulting list of words has this shape ::

        {
          "ID": "418",
          "RAWID": "A1-0422",
          "KANA": "こんにちは",
          "KANJI": "こんにちは　",
          "ROMAJI": "konnichiwa",
          "UWRD": "Hello.",
          "ATTR": [
            {
              "level": "A1",
              "text": "act",
              "utext": "Activities",
              "topic": "1",
              "lesson": "1",
              "ulevel": "Starter (A1)"
            }
          ],
          "HS": null,
          "ROWDATA": ""
        }

    ::

    :param learn_ex: previous levels to exclude
    :param ls: lesson
    :param lv: level
    :return:　a list of words
    """
    response = requests.get(
        f'https://words.marugotoweb.jp/SearchCategoryAPI?&lv={lv}&ls={ls}&tx=act,comp&learn_ex={learn_ex}&ut=en')
    return response.json()['DATA']


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
class VocabA(Vocab):
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


def convert_lesson(lesson_string: str):
    return int(lesson_string.removesuffix("ス"))


def main_2():
    with open("config.json", "r") as f:
        config = json.load(f)

    levels: List[str] = config["levels"]
    level: str = input(f"Level [{','.join(levels)}]: ").strip().lower()
    if level not in levels:
        print(f"Level \"{level}\" not available")
        return

    urls: Dict[str, Dict[str, List[str]]] = config["urls"]

    level_index = levels.index(level)

    if level_index == 0:
        continue_anyway = input("No previous level found. continue anyway [Y/n]? ").lower() in {"", "y", "yes"}
        if not continue_anyway:
            return
        available_languages = set(urls[level].keys())
    else:
        prev_level = levels[level_index - 1]
        available_languages = set(urls[level].keys()).intersection(urls[prev_level].keys())

    language = select_language(available_languages)
    if language is None:
        return

    new_words_for_lesson = get_new_vocabulary(level, language, config)

    for word in new_words_for_lesson:
        print(word.get_main_japanese(), word.translation)
    print(len(new_words_for_lesson))


def select_language(available_languages):
    if len(available_languages) == 1:
        language = next(iter(available_languages))
        print(f"Using language \"{language}\"")
    else:
        selected_language = input(f"Select language [{','.join(available_languages)}]: ").strip().lower()
        if selected_language not in available_languages:
            print(f"Language \"{selected_language}\" not available")
            language = None
        else:
            language = selected_language

    return language


def get_new_vocabulary(level: str, language: str, config: dict):
    levels: List[str] = config["levels"]
    urls: Dict[str, Dict[str, List[str]]] = config["urls"]

    new_urls = urls[level][language]

    level_index = levels.index(level)
    old_urls = []
    prev_level = None
    if level_index != 0:
        prev_level = levels[level_index - 1]
        old_urls = urls[prev_level][language]
    return get_new_vocabulary_by_filenames(level, prev_level, new_urls, old_urls)


def get_new_vocabulary_by_filenames(level: str, prev_level: str, new_filenames, old_filenames):
    old_list = create_list_from_filenames(old_filenames, prev_level)
    new_list = create_list_from_filenames(new_filenames, level)
    new_words = get_new_words(old_list, new_list)
    new_words_for_lesson = filter_duplicates(new_words)
    return new_words_for_lesson


def create_list_from_filenames(urls, level: str) -> List[Vocab]:
    entry_list: List[Vocab] = []
    for filename in urls:
        print(f"Downloading {filename}")
        if level.startswith("a"):
            df = read_excel_a(filename)
            entry_list.extend(a_to_list(df))
        elif level.startswith("b"):
            df = read_excel_b(filename)
            entry_list.extend(b_to_list(df))
        else:
            raise Exception(f"Unable to download and parse files for level {level}")
    return entry_list


def filter_duplicates(entry_list: List[Vocab]) -> List[Vocab]:
    new_list = []
    cache = set()
    for entry in entry_list:
        core = entry.get_main_japanese().strip()
        if core in cache:
            continue
        cache.add(core)
        new_list.append(entry)
    return new_list


def get_new_words(old_list: List[Vocab], new_list: List[Vocab]):
    old_translation_dict = {entry.get_kana_with_translation() for entry in old_list}
    old_kanji_dict = {entry.get_kanji() for entry in old_list}

    def is_old(entry: Vocab):
        if entry.get_kana_with_translation() in old_translation_dict:
            return True
        if entry.get_kanji() in old_kanji_dict:
            return True
        return False

    return [entry for entry in new_list if not is_old(entry)]


def a_to_list(data_frame: pd.DataFrame):
    return [VocabA(row.lesson // 2,
                   row.translation,
                   row.lesson,
                   row.kana,
                   row.kanji,
                   row.accent,
                   row.dictionary_form,
                   row.verb_group,
                   row.word_type) for index, row in data_frame.iterrows()]


def read_excel_a(url):
    df: pd.DataFrame = pd.read_excel(url, header=1)
    df.rename(columns={
        df.columns[0]: "number",
        df.columns[1]: "kana",
        df.columns[2]: "kanji",
        df.columns[3]: "accent",
        df.columns[4]: "dictionary_form",
        df.columns[5]: "verb_group",
        df.columns[6]: "translation",
        df.columns[7]: "lesson",
        df.columns[8]: "word_type",
        df.columns[9]: "other",
    }, inplace=True)
    df["lesson"] = df["lesson"].astype(str).apply(convert_lesson)
    return df


def b_to_list(data_frame: pd.DataFrame) -> List[Vocab]:
    return [VocabB(row.topic,
                   row.translation,
                   row.part,
                   row.japanese,
                   row.pronunciation,
                   row.comment,
                   row.comment_translation) for index, row in data_frame.iterrows()]


def read_excel_b(url):
    df: pd.DataFrame = pd.read_excel(url, header=1)
    df.rename(columns={
        df.columns[0]: "number",
        df.columns[1]: "topic",
        df.columns[2]: "part",
        df.columns[3]: "japanese",
        df.columns[4]: "pronunciation",
        df.columns[5]: "translation",
        df.columns[6]: "comment",
        df.columns[7]: "comment_translation",
        df.columns[8]: "page"
    }, inplace=True)
    # df["lesson"] = df["lesson"].astype(str).apply(convert_lesson)
    return df


if __name__ == '__main__':
    main()
    # main_2()
