import csv
import itertools
from pathlib import Path
from typing import List
from urllib import request

import requests
from PIL import Image


def hint_to_gif(kanji_id, hints, filename):
    if Path(filename).exists():
        return
    images: List[Image] = []
    for i in range(hints):
        number = i + 1
        image = Image.open(
            request.urlopen(f"https://a2.marugotoweb.jp/en/kanji/data/detail/images/hints/{kanji_id}/{number}.png"))
        images.append(image)
    img, *imgs = images
    img.save(
        fp=f"{filename}",
        format="GIF",
        append_images=imgs,
        save_all=True,
        duration=2000,
        loop=0
    )


def download_video(video_id, filename):
    if Path(filename).exists():
        return
    request.urlretrieve(
        f"https://a2.marugotoweb.jp/en/kanji/data/detail/video/{video_id}.mp4",
        f"{filename}"
    )


def download_audio(sound_id, filename):
    if Path(filename).exists():
        return
    request.urlretrieve(
        f"https://a2.marugotoweb.jp/en/kanji/data/detail/audio/{sound_id}.mp3",
        f"{filename}"
    )
    pass


if __name__ == '__main__':
    # hint_to_gif(1, 5, "out/kanji")
    # download_video(2, "a2kanji_0002", "out/kanji")

    kanji_url = "https://a2.marugotoweb.jp/en/kanji/data/list/kanji.json"
    kanji_response = requests.get(kanji_url)
    kanji_list: list = kanji_response.json()
    kanji_dict = {entry["id"]: entry for entry in kanji_list}
    kanji_download = set()


    def get_kanji(id):
        kanji = kanji_dict[id]
        if id not in kanji_download:
            kanji_download.add(id)
            print("Downloading", kanji)
            hint_to_gif(kanji["id"], kanji["hint"], f"out/kanji/media/a2kanji_{kanji['id']}_hint.gif")
            download_video(kanji["video"], f"out/kanji/media/{kanji['video']}.mp4")
        return kanji


    detail_url = "https://a2.marugotoweb.jp/en/kanji/data/detail/detail.json"
    detail_response = requests.get(detail_url)
    detail_list: list = detail_response.json()["examples"]
    detail_list.sort(key=lambda x: x["lesson"])
    grouped = itertools.groupby(detail_list, lambda x: x["lesson"])
    Path("out/kanji/media/").mkdir(parents=True, exist_ok=True)

    selected_lesson = input("lesson: ")

    for lesson, vocabs in grouped:
        if str(lesson) != selected_lesson:
            continue

        with open(f'out/kanji/lesson_{lesson}.csv', 'w') as f1:
            writer = csv.writer(f1, delimiter=';')
            for vocab in vocabs:
                # print(vocab)
                sound_id: str = vocab["sound"]
                audio = ""
                if sound_id.strip() != "":
                    sound_filename = f"kanji_audio_{sound_id}.mp3"
                    download_audio(sound_id, f"out/kanji/media/{sound_filename}")
                    audio = f"[sound:{sound_filename}]"

                kanji_id = vocab["kanjiId"]
                kanji = get_kanji(kanji_id)
                hint_name = f"a2kanji_{kanji['id']}_hint.gif"
                video_name = f"{kanji['video']}.mp4"
                ja = vocab["ja"]
                kana = vocab["ja_kana"]
                en = vocab["native"]
                de = input(f"{ja} {kana} {en}: ")
                phonetic = vocab["phonetic"]
                hint = f'{hint_name}'
                animation = f'{video_name}'
                writer.writerow([ja, en, de, kana, phonetic, audio, hint, animation])
    # with open(f'{out_folder}/cards.csv', 'w') as f1:
    #    writer = csv.writer(f1, delimiter=';')
    # for vocab in list_response.json()["vocabularies"]:
    #    print(vocab)
