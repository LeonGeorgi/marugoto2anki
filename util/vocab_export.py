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

    def create_model_fields(self, fields: list[str]) -> list[dict[str, str]]:
        model_fields = list()

        for field in fields:
            model_fields.append(
                {'name': field}
            )

        return model_fields

    def create_model_template(self, name: str, front: str, back: str) -> dict[str, str]:
        return {
            'name': name,
            'qfmt': front,
            'afmt': back,
        }

    def create_model_templates(self) -> list[dict[str, str]]:
        # TODO: Create from template
        # Should be pretty easy but currently incorrect templates

        templates = list()

        # Templates adapted from template folder to represent files from "FileExporter"
        templates.append(self.create_model_template(
            'Card 1',
            '<span class="question">{{translation}}</span>',
            '{{FrontSide}}<hr id=answer><div class="kana"><span class="answer">{{kana}}</span></div><hr>{{kanjis}}'
        ))

        templates.append(self.create_model_template(
            'Card 2',
            '<div class="kana"><span class="question">{{kana}}</span></div>',
            '{{FrontSide}}<hr id=answer><span class="answer">{{translation}}</span><br>{{kanjis}}'
        ))

        return templates

    def create_card_model(self) -> genanki.Model:
        fields = self.create_model_fields(['sort_id', 'uid', 'kana', 'translation', 'kanjis', 'kanji_meaning', 'accent'])

        templates = self.create_model_templates()

        with open('templates/Marugoto Vocabulary/style.css', 'r') as f:
            css = f.read()

        model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'Marugoto Vocabulary',
            fields,
            templates,
            css
        )

        return model

    def export_vocabulary(self, vocabulary: list[Vocab], level: str, language: str):
        model = self.create_card_model()
        
        decks = list()

        base_deck_name = f'Marugoto::{level}-{language}'
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