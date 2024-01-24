import csv
import html
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

import genanki
import random

class VocabExporter(ABC):

    @abstractmethod
    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        pass


@dataclass
class FileExporter(VocabExporter):
    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        # Define the path to the Anki SQLite collection
        anki_path = os.path.join(os.path.expanduser('~/Library/Application Support/Anki2/User 1'), 'collection.anki2')
        col = Collection(anki_path)
        base_deck = 'Vokabeln::python-test'
        for hierarchy, l in itertools.groupby(vocabulary, lambda x: x.get_lesson_hierarchy()):
            deck_id = col.decks.id(f'{base_deck}::{level}-{language}::{"::".join(hierarchy)}')
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
    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        for group, l in itertools.groupby(vocabulary, lambda x: x.get_lesson_hierarchy()):
            vocabs = list(l)
            out_folder = f"out/excel/{level}/{language}/{group}"
            AnkiExporter.create_out_folder(out_folder)
            print(group, len(vocabs))
            with open(f'{out_folder}/cards.csv', 'w') as file:
                writer = csv.writer(file, delimiter=';')
                for vocab in vocabs:
                    writer.writerow(vocab.get_csv_row())


    def create_out_folder(out_folder):
        Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)

@dataclass
class GenankiExporter(VocabExporter):

    def parse_template_file(self, template_folder: str, card_name: str) -> dict[str, str]:
        with open(os.path.join(template_folder, card_name), 'r') as f:
            template_string = f.read()

        front, back = template_string.split('```')
        
        card = {
            'name': card_name,
            'qfmt': front,
            'afmt': back,
        }

        return card

    def create_card_model(self, template_folder: str) -> genanki.Model:
        field_names = ['sort_id', 'uid', 'kana', 'translation', 'kanjis', 'kanji_meaning', 'accent']
        fields = list(map(lambda field_name: {'name': field_name}, field_names))

        template_files = os.listdir(template_folder)
        if 'style.css' in template_files:
            template_files.remove('style.css')

            with open(os.path.join(template_folder, 'style.css'), 'r') as f:
                css = f.read()
        else:
            css = ''

        template_files.sort()

        templates = list(map(
            lambda template: self.parse_template_file(template_folder, template),
            template_files
        ))

        model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'Marugoto Vocabulary',
            fields,
            templates,
            css
        )

        return model

    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        model = self.create_card_model('templates/Marugoto Simple')
        
        decks = list()

        base_deck_name = f'Marugoto::Vocabulary::{level}-{language}'
        for hierarchy, l in itertools.groupby(vocabulary, lambda x: x.get_lesson_hierarchy()):
            deck_name = f'{base_deck_name}::{"::".join(hierarchy)}'

            deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
                deck_name
            )

            vocabs = list(l)
            for vocab in vocabs:
                # ['sort_id', 'uid', 'kana', 'translation', 'kanjis', 'kanji_meaning', 'accent']
                kana, translation = vocab.get_kana_with_translation()

                note = genanki.Note(
                    model,
                    fields=[vocab.id, vocab.id, kana, translation, vocab.get_kanji(), 'TODO', vocab.get_accent()]
                )

                deck.add_note(note)

            decks.append(deck)
        
        package = genanki.Package(decks)
        package.write_to_file('output.apkg')