import unittest

from fixtures import baker_street
from theme import EntryFile


class EntryFileTest(unittest.TestCase):
    def test_each_entry_counts_its_lines_and_riffs(self):
        entry_file = EntryFile(baker_street.CHARACTERS)

        expected = {
            "characters/detective": 4,
            "shared_lines/any_time": 1,
        }
        self.assertEqual(expected, entry_file.line_counts)
