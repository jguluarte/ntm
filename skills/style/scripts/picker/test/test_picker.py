import tempfile
import unittest
from pathlib import Path

import fixtures
from picker import (
    Picker, chances_table, parser, pick_text, reporting_failures,
)
from theme import Theme

SEED = 3
RUNS = 10


class PickTest(unittest.TestCase):
    def test_the_same_seed_gives_the_same_picks(self):
        first_theme = Theme(fixtures.casebook.EVEN, seed=SEED)
        first_picker = Picker(first_theme)
        second_theme = Theme(fixtures.casebook.EVEN, seed=SEED)
        second_picker = Picker(second_theme)

        first = [first_picker.pick() for _ in range(RUNS)]
        second = [second_picker.pick() for _ in range(RUNS)]

        self.assertEqual(first, second)

    def test_each_pick_draws_again(self):
        theme = Theme(fixtures.casebook.EVEN, seed=SEED)
        picker = Picker(theme)

        picks = {picker.pick() for _ in range(RUNS)}

        self.assertGreater(len(picks), 1)


class PickTextTest(unittest.TestCase):
    def test_a_pick_shows_its_perspective_and_then_its_reference(self):
        theme = Theme(fixtures.baker_street.OPTIONS, seed=SEED)
        picker = Picker(theme)
        perspective, reference = picker.pick()
        rows = pick_text(perspective, reference).splitlines()

        expected = [
            "perspective: characters/detective",
            "reference: scenes/stakeout",
        ]
        self.assertEqual(expected, rows)


class ChancesTableTest(unittest.TestCase):
    def test_each_perspective_shows_weight_score_and_rounded_chance(self):
        theme = Theme(fixtures.casebook.WEIGHTED)
        lottery = theme.perspective_lottery()
        rows = chances_table(lottery).splitlines()

        expected = [
            "perspective      weight  score  chance",
            "scenes/dawn         0.5      0    0.12",
            "scenes/noon           1      1    0.50",
            "scenes/dusk           0      0    0.00",
            "characters/host       3     -1    0.38",
        ]
        self.assertEqual(expected, rows)


class ReportingFailuresTest(unittest.TestCase):
    def test_a_pick_where_every_option_weighs_0_fails_naming_why(self):
        theme = Theme(fixtures.casebook.WEIGHTLESS)
        picker = Picker(theme)

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                picker.pick()

        why = "every option weighs 0"
        expected = f"Picker FAILED: MissingWeight: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        missing_options = Path(folder) / "Missing-options.yaml"

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                Theme(missing_options)

        why = f"[Errno 2] No such file or directory: '{missing_options}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_missing_options_flag_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(["pick"])

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = [
            "pick",
            "--options", str(fixtures.casebook.EVEN),
            "--seed", "seven",
        ]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
