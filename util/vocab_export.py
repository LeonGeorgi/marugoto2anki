import csv
import itertools
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from util.classes import Vocab
from util.config import Config
from util.string_utils import convert_pronunciation_to_kana, generate_kanji_translation

sys.path.append("anki")
import anki
from anki.storage import Collection


class VocabExporter(ABC):
    @abstractmethod
    def export_vocabulary(self):
        pass


@dataclass
class AnkiExporter(VocabExporter):
    vocabulary: list[Vocab]
    level: str
    language: str

    config: Config

    def export_vocabulary(self):
        # Define the path to the Anki SQLite collection
        anki_path = os.path.join(self.config.anki_path, self.config.anki_user, 'collection.anki2')

        with open('kanji_keywords.txt') as f:
            kanji_lines = f.read().splitlines()
        kanji_dict = {kanji[0]: kanji[1] for kanji in (line.split(" ", 1) for line in kanji_lines)}

        col = Collection(anki_path)
        base_deck = self.config.anki_deck
        for hierarchy, l in itertools.groupby(self.vocabulary, lambda x: x.lesson_hierarchy):
            deck_id = col.decks.id(f'{base_deck}::{self.level}-{self.language}::{"::".join(hierarchy)}')
            vocabs = list(l)
            print(hierarchy, len(vocabs))
            for vocab in vocabs:
                vocab: Vocab
                note = anki.notes.Note(col, model=col.models.by_name(self.config.card_model))
                note['uid'] = vocab.uid
                note['kanjis'] = vocab.kanji
                note['kana'] = vocab.kana
                note['translation'] = vocab.translation
                note['sort_id'] = vocab.sort_id
                if vocab.accent:
                    note['accent'] = vocab.accent
                if vocab.word_type:
                    note['type'] = vocab.word_type
                # TODO: note['sound'] = …
                kanji_meaning = generate_kanji_translation(vocab.kanji, kanji_dict)
                if kanji_meaning != vocab.kanji:
                    note['kanji_meaning'] = kanji_meaning
                print(note.fields)
                col.addNote(note)
                for card in note.cards():
                    card.did = deck_id
                    card.flush()

        col.save()
        col.close()


@dataclass
class FileExporter(VocabExporter):
    vocabulary: list[Vocab]
    level: str
    language: str

    def export_vocabulary(self):
        for hierarchy, l in itertools.groupby(self.vocabulary, lambda x: x.lesson_hierarchy):
            vocabs = list(l)
            out_folder = f"out/excel/{self.level}/{self.language}/{'-'.join(hierarchy)}"
            create_out_folder(out_folder)
            print(hierarchy, len(vocabs))
            with open(f'{out_folder}/cards.csv', 'w') as file:
                writer = csv.writer(file, delimiter=';')
                for vocab in vocabs:
                    writer.writerow(vocab.get_csv_row())


def create_out_folder(out_folder):
    Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)
