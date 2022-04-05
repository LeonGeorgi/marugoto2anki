import csv
import itertools
import json
from pathlib import Path
from typing import List, Dict

from util.classes import Vocab
from util.excel_import import read_excel_a1, read_excel_a2, read_excel_b, a1_to_list, a2_to_list, b_to_list
from util.user_input import determine_level, determine_language
from util.vocab_generation import filter_duplicates, get_new_words


def create_out_folder(out_folder):
    Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)


def main():
    config = load_config()
    level, levels = determine_level(config["levels"])
    language = determine_language(config, level, levels)
    new_words_sorted = retreive_vocabulary(config, language, level)
    write_vocabulary(level, new_words_sorted)


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def write_vocabulary(level, new_words_sorted):
    for group, l in itertools.groupby(new_words_sorted, lambda x: x.get_lesson_name()):
        out_folder = f"out/excel/{level}/{group}"
        create_out_folder(out_folder)
        with open(f'{out_folder}/cards.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';')
            for vocab in l:
                writer.writerow(vocab.get_csv_row())
        print(group, len(list(l)))


def retreive_vocabulary(config, language, level):
    new_words_for_lesson: List[Vocab] = get_new_vocabulary(level, language, config)
    new_words_sorted: List[Vocab] = sorted(new_words_for_lesson, key=lambda x: x.get_lesson_name())
    return new_words_sorted


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


if __name__ == '__main__':
    main()
    # print(a1_to_list(read_excel_a1("starter_activities_vocabulary_index_en.xlsx")))
