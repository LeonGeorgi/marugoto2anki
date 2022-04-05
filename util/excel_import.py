from typing import List

import pandas as pd

from util.classes import VocabA1, VocabA2, Vocab, VocabB
from util.string_utils import convert_lesson


def get_vocab_list_by_filenames(urls: list[str], level: str) -> List[Vocab]:
    entry_list: List[Vocab] = []
    for filename in urls:
        print(f"Downloading {filename}")
        if level.startswith("a1"):
            df = read_excel_a1(filename)
            entry_list.extend(a1_to_list(df))
        elif level.startswith("a2"):
            df = read_excel_a2(filename)
            entry_list.extend(a2_to_list(df))
        elif level.startswith("b"):
            df = read_excel_b(filename)
            entry_list.extend(b_to_list(df))
        else:
            raise Exception(f"Unable to download and parse files for level {level}")
    return entry_list


def read_excel_a1(url):
    df: pd.DataFrame = pd.read_excel(url, header=1)
    df.rename(columns={
        df.columns[0]: "id",
        df.columns[1]: "kana",
        df.columns[2]: "kanji",
        df.columns[3]: "accent",
        df.columns[4]: "romaji",
        df.columns[5]: "translation",
        df.columns[6]: "lesson",
        df.columns[7]: "word_type",
        df.columns[8]: "other",
    }, inplace=True)
    df["lesson"] = df["lesson"].astype(str).apply(convert_lesson)
    return df


def read_excel_a2(url):
    file_instance = pd.ExcelFile(url)
    df: pd.DataFrame = file_instance.parse(header=1, sheet_name=file_instance.sheet_names[0])
    # df: pd.DataFrame = pd.read_excel(url, header=1, sheet_name=)
    df.rename(columns={
        df.columns[0]: "id",
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


def read_excel_b(url):
    df: pd.DataFrame = pd.read_excel(url, header=1)
    df.rename(columns={
        df.columns[0]: "id",
        df.columns[1]: "topic",
        df.columns[2]: "part",
        df.columns[3]: "japanese",
        df.columns[4]: "pronunciation",
        df.columns[5]: "translation",
        df.columns[6]: "comment",
        df.columns[7]: "comment_translation",
        df.columns[8]: "page"
    }, inplace=True)
    return df


def a1_to_list(data_frame: pd.DataFrame):
    return [VocabA1(row.id,
                    str((row.lesson + 1) // 2),
                    row.translation,
                    row.lesson,
                    row.kana,
                    row.kanji,
                    row.accent,
                    row.romaji,
                    row.word_type) for index, row in data_frame.iterrows()]


def a2_to_list(data_frame: pd.DataFrame):
    return [VocabA2(str(row.id),
                    str((row.lesson + 1) // 2),
                    row.translation.strip(),
                    str(row.lesson).strip(),
                    row.kana.strip(),
                    row.kanji.strip(),
                    row.accent.strip(),
                    str(row.dictionary_form).strip(),
                    str(row.verb_group).strip(),
                    row.word_type.strip()) for index, row in data_frame.iterrows()]


def b_to_list(data_frame: pd.DataFrame) -> List[Vocab]:
    return [VocabB(row.id,
                   row.topic,
                   row.translation,
                   row.part,
                   row.japanese,
                   row.pronunciation,
                   row.comment,
                   row.comment_translation) for index, row in data_frame.iterrows()]
