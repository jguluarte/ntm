import unittest

import fixtures
from theme import EntryFile


class EntryFileTest(unittest.TestCase):
    def test_each_entry_counts_its_lines_and_riffs(self):
        entry_file = EntryFile(fixtures.casebook.CHARACTERS)

        expected = {
            "characters/detective": {"lines": 3, "riffs": 1},
            "shared_lines/any_time": {"lines": 1},
        }
        self.assertEqual(expected, entry_file.line_counts)

    def test_the_checksum_is_the_sha256_of_the_files_bytes(self):
        entry_file = EntryFile(fixtures.casebook.SCENES)

        expected = (
            "4afb4bce8e58bfced5bfd26c0efc1847793791a497f115de11b2a30d6d03ed94"
        )
        self.assertEqual(expected, entry_file.checksum)
