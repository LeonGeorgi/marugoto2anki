import csv
import html
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

import genanki
import random

class VocabExporter(ABC):
    @abstractmethod
    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        pass


@dataclass
class AnkiExporter(VocabExporter):
    config: Config

    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        # Define the path to the Anki SQLite collection
        anki_path = os.path.join(self.config.anki_path, self.config.anki_user, 'collection.anki2')

        with open('kanji_keywords.txt') as f:
            kanji_lines = f.read().splitlines()
        kanji_dict = {kanji[0]: kanji[1] for kanji in (line.split(" ", 1) for line in kanji_lines)}

        col = Collection(anki_path)
        base_deck = self.config.anki_deck
        for hierarchy, l in itertools.groupby(vocabulary, lambda x: x.lesson_hierarchy):
            deck_id = col.decks.id(f'{base_deck}::{level}-{language}::{"::".join(hierarchy)}')
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
    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        for hierarchy, l in itertools.groupby(vocabulary, lambda x: x.lesson_hierarchy):
            vocabs = list(l)
            out_folder = f"out/excel/{level}/{language}/{'-'.join(hierarchy)}"
            FileExporter.create_out_folder(out_folder)
            print(hierarchy, len(vocabs))
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