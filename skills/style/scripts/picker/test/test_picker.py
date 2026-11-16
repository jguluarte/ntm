import unittest

import fixtures
from picker import Picker, chances_table, parser, reporting_failures
from theme import MissingOptions, Theme, ThemeOptions

SEED = 3
RUNS = 10
ATTEMPTS = 50


class PickTest(unittest.TestCase):
    def test_only_an_option_fitting_the_type_is_drawn(self):
        theme = Theme(fixtures.EVERY_TYPE)
        options = ThemeOptions("weekly,big_win")
        picker = Picker(theme, options)
        drawn = picker.pick()

        self.assertEqual("hook: scenes/big_win", drawn)

    def test_the_same_seed_gives_the_same_pick(self):
        first_theme = Theme(fixtures.EVEN, seed=SEED)
        first_picker = Picker(first_theme)
        first = [first_picker.pick() for _ in range(RUNS)]

        second_theme = Theme(fixtures.EVEN, seed=SEED)
        second_picker = Picker(second_theme)
        second = [second_picker.pick() for _ in range(RUNS)]

        self.assertEqual(first, second)

    def test_without_a_seed_runs_draw_different_options(self):
        theme = Theme(fixtures.EVEN)
        picker = Picker(theme)
        drawn = {picker.pick() for _ in range(ATTEMPTS)}

        self.assertGreater(len(drawn), 1)

    def test_an_option_weighing_0_is_never_drawn(self):
        theme = Theme(fixtures.WEIGHTED)
        picker = Picker(theme)
        drawn = {picker.pick() for _ in range(ATTEMPTS)}

        self.assertNotIn("hook: scenes/dusk", drawn)

    def test_a_message_no_option_fits_fails_with_missing_options(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        options = ThemeOptions("morning")
        picker = Picker(theme, options)

        with self.assertRaises(MissingOptions) as raised:
            picker.pick()

        self.assertEqual("no option fits morning", str(raised.exception))


class ChancesTableTest(unittest.TestCase):
    def test_each_fitting_option_shows_weight_score_and_rounded_chance(self):
        theme = Theme(fixtures.WEIGHTED)
        options = ThemeOptions()
        lottery = theme.lottery_for(options)
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
    def test_a_missing_options_flag_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(["hook"])

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_type_that_isnt_an_option_fails_with_unknown_option(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                ThemeOptions("night")

        expected = "Picker FAILED: UnknownOption: not an option: night"
        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                Theme(fixtures.NOT_THERE)

        why = f"[Errno 2] No such file or directory: '{fixtures.NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertEqual(expected, exited.exception.code)
