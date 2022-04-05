import csv
import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from util.classes import Vocab


class VocabExporter(ABC):

    @abstractmethod
    def export_vocabulary(self):
        pass


@dataclass
class FileExporter(VocabExporter):
    vocabulary: list[Vocab]
    level: str

    def export_vocabulary(self):
        for group, l in itertools.groupby(self.vocabulary, lambda x: x.get_lesson_name()):
            out_folder = f"out/excel/{self.level}/{group}"
            create_out_folder(out_folder)
            with open(f'{out_folder}/cards.csv', 'w') as file:
                writer = csv.writer(file, delimiter=';')
                for vocab in l:
                    writer.writerow(vocab.get_csv_row())
            print(group, len(list(l)))


def create_out_folder(out_folder):
    Path(f"{out_folder}/media/").mkdir(parents=True, exist_ok=True)
