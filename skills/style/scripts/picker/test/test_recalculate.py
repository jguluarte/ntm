import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import fixtures
from recalculate import Recalculation
from theme import EntryFile, Theme


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


class CommandLineTest(unittest.TestCase):
    def test_start_reads_the_options_file_and_each_entry_file(self):
        args = make_start_args(
            fixtures.CASEBOOK, fixtures.CASEBOOK_CHARACTERS,
            fixtures.CASEBOOK_SCENES,
        )
        recalculation = Recalculation.from_args(args)
        names = [entry_file.name for entry_file in recalculation.entry_files]

        expected = ["Casebook-characters.yaml", "Casebook-scenes.yaml"]
        self.assertEqual(expected, names)

    def test_start_without_entry_files_fails_naming_them(self):
        args = make_start_args(fixtures.CASEBOOK)

        with self.assertRaises(SystemExit) as exited:
            Recalculation.from_args(args)

        why = "the following arguments are required: entry_files"
        expected = f"Recalculation FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)


class StartTest(unittest.TestCase):
    def setUp(self):
        self.entry_files = [
            EntryFile(fixtures.CASEBOOK_CHARACTERS),
            EntryFile(fixtures.CASEBOOK_SCENES),
        ]

    def copy_of(self, options):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        return Path(shutil.copy(options, folder))

    def start(self, options):
        return Recalculation(Theme(options), self.entry_files).start()

    def test_start_gives_the_documented_example_its_own_weights(self):
        options = self.copy_of(fixtures.WITHOUT_NUMBERS)
        self.start(options)
        weights = read_weights(options)

        expected = {
            "characters/detective": 0.57,
            "shared_lines/any_time": 0.25,
            "shared_lines/big_win": 0.25,
            "scenes/stakeout": 1.0,
        }
        self.assertEqual(expected, weights)

    def test_start_writes_each_entry_files_checksum(self):
        options = self.copy_of(fixtures.WITHOUT_NUMBERS)
        self.start(options)
        checksums = read_fields(options)["checksums"]

        expected = {
            entry_file.name: entry_file.checksum
            for entry_file in self.entry_files
        }
        self.assertEqual(expected, checksums)

    def test_start_keeps_every_value_it_doesnt_compute(self):
        options = self.copy_of(fixtures.CASEBOOK)
        self.start(options)
        pools = read_fields(options)["pools"]

        expected = read_fields(fixtures.CASEBOOK)["pools"]
        self.assertEqual(expected, pools)

    def test_start_prints_each_file_it_recounted(self):
        options = self.copy_of(fixtures.WITHOUT_NUMBERS)
        printed = self.start(options)

        expected = (
            "recounted: Casebook-characters.yaml\n"
            "recounted: Casebook-scenes.yaml"
        )
        self.assertEqual(expected, printed)

    def test_an_entry_file_no_pool_uses_fails_in_one_line(self):
        options = self.copy_of(fixtures.EVEN)

        with self.assertRaises(SystemExit) as exited:
            self.start(options)

        why = "no pool uses Casebook-characters.yaml"
        expected = f"Recalculation FAILED: UnknownEntryFile: {why}"
        self.assertEqual(expected, exited.exception.code)
