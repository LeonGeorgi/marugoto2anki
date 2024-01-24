def convert_lesson(lesson_string: str) -> str:
    print(lesson_string)
    return str(int(lesson_string.removesuffix("ス")))


def calculate_topic(lesson: str):
    converted_lesson = convert_lesson(lesson)
    return str((int(converted_lesson) + 1) // 2)


def convert_pronunciation(pronunciation: str) -> str:
    return pronunciation.replace('7', '￢').replace('0', '￣')


def convert_pronunciation_to_kana(pronunciation: str) -> str:
    return pronunciation.replace('￢', '').replace('￣', '')


def generate_kanji_translation(kanji: str, kanji_dict: dict[str, str]):
    kanji_translation = ""
    for index, symbol in enumerate(kanji):
        if symbol in kanji_dict:
            kanji_translation += f" {symbol}[{kanji_dict[symbol]}]"
        else:
            kanji_translation += symbol
    return kanji_translation
