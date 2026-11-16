import argparse
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import fixtures
from recalculate import Recalculation, reporting_failures
from theme import EntryFile, Theme, UnknownEntryFile


def make_start_args(options, *entry_files):
    args = ["start", "--options", str(options)]
    return args + [str(entry_file) for entry_file in entry_files]


def read_fields(options):
    return yaml.safe_load(options.read_text(encoding="utf-8"))


def read_weights(options):
    pools_by_kind = read_fields(options)["pools"]
    return {
        f"{kind}/{slug}": entry["weight"]
        for kind, pool in pools_by_kind.items()
        for slug, entry in pool["entries"].items()
    }


def read_checksums(options):
    return read_fields(options)["checksums"]


class CommandLineTest(unittest.TestCase):
    def test_start_reads_each_entry_file_it_is_given(self):
        args = make_start_args(
            fixtures.casebook.OPTIONS, fixtures.casebook.CHARACTERS,
            fixtures.casebook.SCENES,
        )
        recalculation = Recalculation.from_args(args)
        names = [entry_file.name for entry_file in recalculation.entry_files]

        expected = ["Casebook-characters.yaml", "Casebook-scenes.yaml"]
        self.assertEqual(expected, names)

    def test_start_without_entry_files_fails_naming_them(self):
        args = make_start_args(fixtures.casebook.OPTIONS)

        with self.assertRaises(argparse.ArgumentError) as raised:
            Recalculation.from_args(args)

        expected = "the following arguments are required: entry_files"
        self.assertEqual(expected, str(raised.exception))


class RecalculationTest(unittest.TestCase):
    def setUp(self):
        self.characters = EntryFile(fixtures.casebook.CHARACTERS)
        self.scenes = EntryFile(fixtures.casebook.SCENES)

    def copy_of(self, options):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        return Path(shutil.copy(options, folder))

    def recalculation_of(self, options):
        return Recalculation(Theme(options), [self.characters, self.scenes])

    def test_weighing_gives_the_documented_example_its_own_weights(self):
        options = self.copy_of(fixtures.casebook.OPTIONS_WITHOUT_NUMBERS)
        recalculation = self.recalculation_of(options)
        recalculation.weigh_entries()
        recalculation.save_options_file()

        expected = {
            "characters/detective": 0.57,
            "shared_lines/any_time": 0.25,
            "scenes/stakeout": 1.0,
        }
        self.assertEqual(expected, read_weights(options))

    def test_recording_writes_each_entry_files_own_checksum(self):
        options = self.copy_of(fixtures.casebook.OPTIONS_WITHOUT_NUMBERS)
        recalculation = self.recalculation_of(options)
        recalculation.record_checksums()
        recalculation.save_options_file()

        expected = {
            "Casebook-characters.yaml": self.characters.checksum,
            "Casebook-scenes.yaml": self.scenes.checksum,
        }
        self.assertEqual(expected, read_checksums(options))

    def test_recalculating_the_documented_example_leaves_its_pools_alone(self):
        options = self.copy_of(fixtures.casebook.OPTIONS)
        recalculation = self.recalculation_of(options)
        recalculation.weigh_entries()
        recalculation.record_checksums()
        recalculation.save_options_file()

        expected = read_fields(fixtures.casebook.OPTIONS)["pools"]
        self.assertEqual(expected, read_fields(options)["pools"])

    def test_an_entry_file_no_pool_uses_fails_with_unknown_entry_file(self):
        recalculation = self.recalculation_of(fixtures.EVEN)

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
