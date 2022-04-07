import unittest

from util.classes import VocabA2, VocabA1, VocabA2B1


class ClassesTest(unittest.TestCase):
    def test_parse_row_a1(self):
        vocab_card = VocabA1.from_table_row(('52', 'いま', 'いま', 'い￢ま', 'ima', 'now', '3ス', '01 名詞', '訳語修正'))
        expected_card = VocabA1('52', '2', 'now', '3', 'いま', 'いま', 'い￢ま', 'ima', '01 名詞')
        self.assertEqual(expected_card, vocab_card)

    def test_parse_row_a2(self):
        vocab_card = VocabA2.from_table_row((
            '11',
            'あがります',
            '(上がります)',
            'あがりま￢す',
            'あがる',
            '1',
            'steigen',
            '4',
            '02 動詞',
            'comment'
        ))
        expected_card = VocabA2('11', '2', 'steigen', '4', 'あがります', '(上がります)', 'あがりま￢す', 'あがる', '1', '02 動詞')
        self.assertEqual(expected_card, vocab_card)

    def test_parse_row_a2b1(self):
        vocab_card = VocabA2B1.from_table_row((
            '280',
            'かかります(じかんが)',
            'かかります（時間が）',
            'かかりま￢す',
            'かかる',
            '1',
            'dauern',
            '2',
            '02 動詞',
            '漢字表記加筆（時間）20180330'
        ))

        expected_card = VocabA2B1('280', '2', 'dauern', 'かかります(じかんが)', 'かかります（時間が）', 'かかりま￢す', 'かかる', '1', '02 動詞')
        self.assertEqual(expected_card, vocab_card)


if __name__ == '__main__':
    unittest.main()
