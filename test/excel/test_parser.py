import unittest

from util.excel.parser import ExcelParser


class ExcelParserTest(unittest.TestCase):

    def test_get_sheet_names(self):
        parser = ExcelParser('resources/intermediate1_vocabulary_list_en_excel.xlsx')
        self.assertEqual(parser.get_sheet_names(), ['語彙トピック1-9（英語）', '指示の表現（英語）'])

        parser = ExcelParser('resources/elementary1_activities_vocabulary_index_de.xlsx')
        self.assertEqual(parser.get_sheet_names(), ['初級1 かつどう 語彙index'])

    def test_get_all_sheets(self):
        parser = ExcelParser('excel/4_sheets.xlsx')
        all_sheets = parser.get_all_sheets()
        self.assertEqual(len(all_sheets), 4)

        first_sheet = all_sheets[0]
        self.assertEqual(len(first_sheet), 7)
        self.assertEqual(len(first_sheet[2]), 1)
        self.assertEqual(first_sheet[2][0], '3')

    def test_get_longest_sheet(self):
        parser = ExcelParser('excel/4_sheets.xlsx')
        longest_sheet = parser.get_longest_sheet()
        self.assertEqual(len(longest_sheet), 23)
        self.assertEqual(len(longest_sheet[2]), 2)
        self.assertEqual(longest_sheet[2][1], '4')


if __name__ == '__main__':
    unittest.main()
