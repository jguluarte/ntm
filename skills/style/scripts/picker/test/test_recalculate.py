import unittest

import fixtures
from recalculate import Recalculation, parser, reporting_failures
from theme import EntryFile, Theme, UnknownEntryFile


class RecalculationTest(unittest.TestCase):
    def test_weighing_gives_each_entry_its_weight_from_its_lines(self):
        theme = Theme(fixtures.weighing.OPTIONS)
        entry_file = EntryFile(fixtures.weighing.CHARACTERS)
        recalculation = Recalculation(theme, [entry_file])

        recalculation.weigh_entries()

        self.assertEqual(0.25, theme.weight_of("characters/one_line"))
        self.assertEqual(0.5, theme.weight_of("characters/three_lines"))
        self.assertEqual(0.75, theme.weight_of("characters/nine_lines"))
        self.assertEqual(1.0, theme.weight_of("characters/no_lines"))

    def test_recording_gives_each_entry_its_line_counts(self):
        theme = Theme(fixtures.weighing.OPTIONS)
        entry_file = EntryFile(fixtures.weighing.CHARACTERS)
        recalculation = Recalculation(theme, [entry_file])

        recalculation.record_line_counts()

        line_counts = {
            entry_name: theme.line_counts_of(entry_name)
            for entry_name in theme.entries_from(entry_file.name)
        }
        expected = {
            "characters/one_line": {"lines": 1},
            "characters/three_lines": {"lines": 2, "riffs": 1},
            "characters/nine_lines": {"lines": 9},
            "characters/no_lines": {},
        }
        self.assertEqual(expected, line_counts)

    def test_recording_gives_the_entry_file_its_own_checksum(self):
        theme = Theme(fixtures.weighing.OPTIONS)
        entry_file = EntryFile(fixtures.weighing.CHARACTERS)
        recalculation = Recalculation(theme, [entry_file])

        recalculation.record_checksums()

        checksum = theme.checksum_of("Weighing-characters.yaml")
        self.assertEqual(entry_file.checksum, checksum)

    def test_an_entry_file_no_pool_uses_fails_with_unknown_entry_file(self):
        theme = Theme(fixtures.EVEN)
        characters = EntryFile(fixtures.casebook.CHARACTERS)
        scenes = EntryFile(fixtures.casebook.SCENES)
        recalculation = Recalculation(theme, [characters, scenes])

        with self.assertRaises(UnknownEntryFile) as raised:
            recalculation.weigh_entries()

        expected = "no pool uses Casebook-characters.yaml"
        self.assertEqual(expected, str(raised.exception))


class ReportingFailuresTest(unittest.TestCase):
    def test_a_failure_exits_with_one_line_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                raise UnknownEntryFile("Casebook-characters.yaml")

        why = "no pool uses Casebook-characters.yaml"
        expected = f"Recalculation FAILED: UnknownEntryFile: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_start_without_entry_files_fails_naming_them(self):
        args = ["start", "--options", str(fixtures.casebook.OPTIONS)]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "the following arguments are required: entry_files"
        expected = f"Recalculation FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
