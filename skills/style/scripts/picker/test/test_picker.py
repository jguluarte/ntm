import unittest

import fixtures
from picker import Picker
from theme import Theme


def make_picker_args(options, **flags):
    args = ["hook", "--options", str(options)]

    for name, value in flags.items():
        args += [f"--{name}", str(value)]

    return args


class CommandLineTest(unittest.TestCase):
    def test_the_seed_is_optional(self):
        args = make_picker_args(fixtures.EVEN)
        picker = Picker.from_args(args)

        self.assertIsNone(picker.theme.seed)

    def test_the_seed_flag_sets_the_themes_seed(self):
        args = make_picker_args(fixtures.EVEN, seed=3)
        picker = Picker.from_args(args)

        self.assertEqual(3, picker.theme.seed)

    def test_the_chances_flag_sets_shows_chances(self):
        args = make_picker_args(fixtures.EVEN) + ["--chances"]
        picker = Picker.from_args(args)

        self.assertTrue(picker.shows_chances)

    def test_the_chances_flag_is_optional(self):
        args = make_picker_args(fixtures.EVEN)
        picker = Picker.from_args(args)

        self.assertFalse(picker.shows_chances)

    def test_a_missing_options_flag_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(["hook"])

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = make_picker_args(fixtures.EVEN, seed="seven")

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        args = make_picker_args(fixtures.NOT_THERE)

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = f"[Errno 2] No such file or directory: '{fixtures.NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertEqual(expected, exited.exception.code)


class PickTest(unittest.TestCase):
    def test_the_same_seed_gives_the_same_pick(self):
        seed = 3
        runs = 10

        first_theme = Theme(fixtures.EVEN, seed)
        first_picker = Picker(first_theme)
        first = [first_picker.pick() for _ in range(runs)]

        second_theme = Theme(fixtures.EVEN, seed)
        second_picker = Picker(second_theme)
        second = [second_picker.pick() for _ in range(runs)]

        self.assertEqual(first, second)

    def test_without_a_seed_runs_draw_different_options(self):
        theme = Theme(fixtures.EVEN)
        picker = Picker(theme)

        attempts = 50
        drawn = {picker.pick() for _ in range(attempts)}

        self.assertGreater(len(drawn), 1)

    def test_an_option_weighing_0_is_never_drawn(self):
        theme = Theme(fixtures.WEIGHTED)
        picker = Picker(theme)

        attempts = 50
        drawn = {picker.pick() for _ in range(attempts)}

        self.assertNotIn("hook: scenes/dusk", drawn)


class ChancesTableTest(unittest.TestCase):
    def test_each_option_shows_weight_score_and_rounded_chance(self):
        theme = Theme(fixtures.WEIGHTED)
        picker = Picker(theme)
        rows = picker.chances_table().splitlines()

        expected = [
            "hook             weight  score  chance",
            "scenes/dawn         0.5      0    0.12",
            "scenes/noon           1      1    0.50",
            "scenes/dusk           0      0    0.00",
            "characters/host       3     -1    0.38",
        ]
        self.assertEqual(expected, rows)

    def test_chances_where_every_option_weighs_0_fail_naming_why(self):
        theme = Theme(fixtures.WEIGHTLESS)
        picker = Picker(theme)

        with self.assertRaises(SystemExit) as exited:
            picker.chances_table()

        why = "every option weighs 0"
        expected = f"Picker FAILED: MissingWeight: {why}"
        self.assertEqual(expected, exited.exception.code)
