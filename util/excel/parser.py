from pathlib import Path

import pandas as pd


class ExcelParser:

    def __init__(self, filename: Path):
        self.file = pd.ExcelFile(filename)

    def get_sheet_names(self):
        return self.file.sheet_names

    def get_all_sheets(self):
        sheets = []
        for sheet_name in self.get_sheet_names():
            pd_sheet = self.file.parse(header=None, sheet_name=sheet_name)
            sheet = _convert_sheet(pd_sheet)
            sheets.append(sheet)
        return sheets

    def get_longest_sheet(self):
        return max(self.get_all_sheets(), key=len)


def _convert_row(row: pd.Series):
    return tuple(str(value) for name, value in row.items())


def _convert_sheet(sheet):
    return list(_convert_row(row) for index, row in sheet.iterrows())
