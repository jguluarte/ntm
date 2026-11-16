import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

import fixtures
from recalculate import Recalculation, parser, reporting_failures
from theme import EntryFile, Theme, UnknownEntryFile


class RecalculationTest(unittest.TestCase):
    def setUp(self):
        self.folder = self.enterContext(tempfile.TemporaryDirectory())

    def test_weighing_gives_the_documented_example_its_own_weights(self):
        options = shutil.copy(
            fixtures.casebook.OPTIONS_WITHOUT_NUMBERS, self.folder,
        )
        theme = Theme(options)
        characters = EntryFile(fixtures.casebook.CHARACTERS)
        scenes = EntryFile(fixtures.casebook.SCENES)
        recalculation = Recalculation(theme, [characters, scenes])
        recalculation.weigh_entries()
        recalculation.save_options_file()
        text = Path(options).read_text(encoding="utf-8")

        expected = textwrap.dedent("""\
            checksums: {}
            pools:
              characters:
                file: Casebook-characters.yaml
                roles: [hook, speaker]
                entries:
                  detective:
                    weight: 0.57
              shared_lines:
                file: Casebook-characters.yaml
                roles: [hook]
                entries:
                  any_time:
                    weight: 0.25
              scenes:
                file: Casebook-scenes.yaml
                roles: [hook]
                entries:
                  stakeout:
                    weight: 1.0
        """)
        self.assertEqual(expected, text)

    def test_recording_writes_each_entry_files_own_checksum(self):
        options = shutil.copy(
            fixtures.casebook.OPTIONS_WITHOUT_NUMBERS, self.folder,
        )
        theme = Theme(options)
        characters = EntryFile(fixtures.casebook.CHARACTERS)
        scenes = EntryFile(fixtures.casebook.SCENES)
        recalculation = Recalculation(theme, [characters, scenes])
        recalculation.record_checksums()
        recalculation.save_options_file()
        text = Path(options).read_text(encoding="utf-8")
        saved_fields = yaml.safe_load(text)

        expected = {
            "Casebook-characters.yaml": characters.checksum,
            "Casebook-scenes.yaml": scenes.checksum,
        }
        self.assertEqual(expected, saved_fields["checksums"])

    def test_recalculating_the_documented_example_leaves_its_pools_alone(self):
        options = shutil.copy(fixtures.casebook.OPTIONS, self.folder)
        theme = Theme(options)
        characters = EntryFile(fixtures.casebook.CHARACTERS)
        scenes = EntryFile(fixtures.casebook.SCENES)
        recalculation = Recalculation(theme, [characters, scenes])
        recalculation.weigh_entries()
        recalculation.record_checksums()
        recalculation.save_options_file()
        original_text = fixtures.casebook.OPTIONS.read_text(encoding="utf-8")
        original_fields = yaml.safe_load(original_text)
        saved_text = Path(options).read_text(encoding="utf-8")
        saved_fields = yaml.safe_load(saved_text)

        self.assertEqual(original_fields["pools"], saved_fields["pools"])

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
