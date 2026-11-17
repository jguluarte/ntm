import unittest

import fixtures
from picker import (
    Picker, chances_table, parser, pick_text, reporting_failures,
)
from theme import Theme

SEED = 3
RUNS = 10


class PickTest(unittest.TestCase):
    def test_the_same_seed_gives_the_same_picks(self):
        first_theme = Theme(fixtures.EVEN, seed=SEED)
        first_picker = Picker(first_theme)
        second_theme = Theme(fixtures.EVEN, seed=SEED)
        second_picker = Picker(second_theme)

        first = [first_picker.pick() for _ in range(RUNS)]
        second = [second_picker.pick() for _ in range(RUNS)]

        self.assertEqual(first, second)

    def test_each_pick_draws_again(self):
        theme = Theme(fixtures.EVEN, seed=SEED)
        picker = Picker(theme)

        picks = {picker.pick() for _ in range(RUNS)}

        self.assertGreater(len(picks), 1)


class PickTextTest(unittest.TestCase):
    def test_a_pick_shows_its_perspective_and_then_its_reference(self):
        theme = Theme(fixtures.casebook.OPTIONS, seed=SEED)
        picker = Picker(theme)
        perspective, reference = picker.pick()
        rows = pick_text(perspective, reference).splitlines()

        expected = [
            "perspective: characters/detective",
            "reference: scenes/stakeout",
        ]
        self.assertEqual(expected, rows)


class ChancesTableTest(unittest.TestCase):
    def test_each_perspective_shows_weight_score_rest_and_rounded_chance(self):
        days_since_use = {"scenes/noon": 0}
        theme = Theme(fixtures.WEIGHTED, days_since_use=days_since_use)
        lottery = theme.perspective_lottery()
        rows = chances_table(lottery).splitlines()

        expected = [
            "perspective      weight  score  rest  chance",
            "scenes/dawn         0.5      0  0.00    0.20",
            "scenes/noon           1      1  2.00    0.20",
            "scenes/dusk           0      0  0.00    0.00",
            "characters/host       3     -1  0.00    0.60",
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

    def test_missing_flags_fail_naming_each_required_one(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(["pick"])

        required = "--options, --history, --now"
        why = f"the following arguments are required: {required}"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = ["pick", "--options", str(fixtures.EVEN), "--seed", "seven"]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
