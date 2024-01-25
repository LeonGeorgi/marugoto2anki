import os

from anki.collection import Collection

from util.config import Config
from util.string_utils import generate_kanji_translation


def main():
    config = Config.parse_file("config.ini")
    anki_path = os.path.join(config.anki_path, config.anki_user, 'collection.anki2')

    with open('kanji_keywords.txt') as f:
        kanji_lines = f.read().splitlines()
    kanji_dict = {kanji[0]: kanji[1] for kanji in (line.split(" ", 1) for line in kanji_lines)}

    col = Collection(str(anki_path))

    kanji_note_types = []
    for model in col.models.all():
        field_names = {field['name'] for field in model['flds']}
        if "kanjis" in field_names and "kanji_meaning" in field_names:
            kanji_note_types.append(model['name'])

    print(f"Found note types with kanji and kanji_meaning fields: {kanji_note_types}")

    for note_type in kanji_note_types:
        for cid in col.find_notes(f'"note:{note_type}"'):
            note = col.get_note(cid)
            kanji = note['kanjis']
            kanji_meaning = note['kanji_meaning']
            if kanji and not kanji_meaning:
                kanji_translation = generate_kanji_translation(kanji, kanji_dict)
                if kanji_translation != kanji:
                    print(f"{kanji} -> {kanji_translation}")
                    note['kanji_meaning'] = kanji_translation
                    col.update_note(note)
    col.save()
    col.close()


if __name__ == '__main__':
    main()
