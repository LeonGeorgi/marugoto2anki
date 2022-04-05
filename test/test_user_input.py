import unittest
from unittest import mock

from util.user_input import select_language


class TestUserInput(unittest.TestCase):
    @mock.patch('util.user_input.input', create=True)
    def test_select_language(self, mocked_input):
        mocked_input.side_effect = ['de', 'en']
        self.assertEqual(select_language({'de', 'fr'}), 'de')
        self.assertEqual(select_language({'fr'}), 'fr')
        self.assertRaises(Exception, lambda: select_language({'de', 'fr'}))
