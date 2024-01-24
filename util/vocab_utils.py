from typing import List

from util.classes import Vocab


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
    old_translation_dict = {(entry.kana, entry.translation) for entry in old_list}
    old_kanji_dict = {entry.kanji for entry in old_list}

    def is_old(entry: Vocab):
        if (entry.kana, entry.translation) in old_translation_dict:
            return True
        if entry.kanji in old_kanji_dict:
            return True
        return False

    return [entry for entry in new_list if not is_old(entry)]
