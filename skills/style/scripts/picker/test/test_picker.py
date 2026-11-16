import unittest

import fixtures
from picker import Picker, chances_table, parser, reporting_failures
from theme import Theme


class ChancesTableTest(unittest.TestCase):
    def test_each_option_shows_weight_score_and_rounded_chance(self):
        theme = Theme(fixtures.WEIGHTED)
        lottery = theme.lottery()
        rows = chances_table(lottery).splitlines()

        expected = [
            "hook             weight  score  chance",
            "scenes/dawn         0.5      0    0.12",
            "scenes/noon           1      1    0.50",
            "scenes/dusk           0      0    0.00",
            "characters/host       3     -1    0.38",
        ]
        self.assertEqual(expected, rows)


class ReportingFailuresTest(unittest.TestCase):
    def test_a_pick_where_every_option_weighs_0_fails_naming_why(self):
        theme = Theme(fixtures.WEIGHTLESS)
        picker = Picker(theme)

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                picker.pick()

        why = "every option weighs 0"
        expected = f"Picker FAILED: MissingWeight: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                Theme(fixtures.NOT_THERE)

        why = f"[Errno 2] No such file or directory: '{fixtures.NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_missing_options_flag_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(["hook"])

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = ["hook", "--options", str(fixtures.EVEN), "--seed", "seven"]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
