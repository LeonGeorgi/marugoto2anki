from dataclasses import dataclass
from pathlib import Path

import requests
from urllib import request
import csv


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
    request.urlretrieve(audio_url, f"{out_folder}/audio/{audio_id}.mp3")
    return f"{audio_id}.mp3"


def create_out_folder(out_folder):
    Path(f"{out_folder}/audio/").mkdir(parents=True, exist_ok=True)


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


if __name__ == '__main__':
    main()
