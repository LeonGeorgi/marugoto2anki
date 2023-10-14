import csv
import itertools
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from util.classes import Vocab

sys.path.append("anki")
import anki
from anki.storage import Collection


class VocabExporter(ABC):

    @abstractmethod
    def export_vocabulary(self):
        pass


@dataclass
class FileExporter(VocabExporter):
    vocabulary: list[Vocab]
    level: str
    language: str

    def export_vocabulary(self):
        # Define the path to the Anki SQLite collection
        anki_path = os.path.join(os.path.expanduser('~/Library/Application Support/Anki2/User 1'), 'collection.anki2')
        col = Collection(anki_path)
        base_deck = 'Vokabeln::python-test'
        for hierarchy, l in itertools.groupby(self.vocabulary, lambda x: x.get_lesson_hierarchy()):
            deck_id = col.decks.id(f'{base_deck}::{self.level}-{self.language}::{"::".join(hierarchy)}')
            # deck = col.decks.get(deck_id)
            vocabs = list(l)
            print(hierarchy, len(vocabs))
            for vocab in vocabs:
                note = anki.notes.Note(col, model=col.models.by_name('Vocabulary Simple'))
                note['kanjis'] = vocab.get_kanji()
                kana, translation = vocab.get_kana_with_translation()
                note['kana'] = kana
                # note['type'] = ''
                note['translation'] = translation
                note['kanji_meaning'] = 'TODO'
                # note['sound'] = ''
                note['accent'] = vocab.get_accent()
                note['sort_id'] = vocab.id
                note['uid'] = vocab.id
                col.addNote(note)
                # Die Karte dem neuen Deck zuweisen
                card_1 = note.cards()[0]
                card_2 = note.cards()[1]

                card_1.did = deck_id
                card_2.did = deck_id

                card_1.flush()
                card_2.flush()

        col.save()
        col.close()


@dataclass
class AnkiExporter(VocabExporter):
    vocabulary: list[Vocab]
    level: str
    language: str

    def export_vocabulary(self):
        for group, l in itertools.groupby(self.vocabulary, lambda x: x.get_lesson_hierarchy()):
            vocabs = list(l)
            out_folder = f"out/excel/{self.level}/{self.language}/{group}"
            create_out_folder(out_folder)
            print(group, len(vocabs))
            with open(f'{out_folder}/cards.csv', 'w') as file:
                writer = csv.writer(file, delimiter=';')
                for vocab in vocabs:
                    writer.writerow(vocab.get_csv_row())


def create_out_folder(out_folder):
    Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)
