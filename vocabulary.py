from pathlib import Path

import requests
from urllib import request
import csv

if __name__ == '__main__':
    level = input("level (A2-1): ")
    if level.strip() == "":
        level = "A2-1"

    lesson = input("lesson: ")

    response = requests.get(
        f'https://words.marugotoweb.jp/SearchCategoryAPI?&lv={level}&ls={lesson}&tx=act,comp&learn_ex=A1&ut=en')
    out_folder = f"out/{level}/lesson-{lesson}"
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    Path(f"{out_folder}/audio/").mkdir(parents=True, exist_ok=True)
    print(len(response.json()["DATA"]), "words found.")
    print("Translate to German")
    with open(f'{out_folder}/cards.csv', 'w') as f1:
        writer = csv.writer(f1, delimiter=';')
        for entry in response.json()["DATA"]:
            audio_id: str = entry["RAWID"]
            kana: str = entry["KANA"]
            kanji = entry["KANJI"]
            romaji = entry["ROMAJI"]
            english = entry["UWRD"]
            german = input(f"{kana} {english}: ")

            audio_url = f"https://words.marugotoweb.jp/res/keyword/audio/A21W/{audio_id.replace('-', 'W_')}.mp3"
            target_dir = "~/Library/Application Support/Anki2/Benutzer 1/collection.media/"
            request.urlretrieve(audio_url, f"{out_folder}/audio/{audio_id}.mp3")
            writer.writerow([kana, english, german, romaji, kanji, f"[sound:{audio_id}.mp3]"])
