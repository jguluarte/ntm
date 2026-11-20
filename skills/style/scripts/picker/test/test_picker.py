import unittest

from fixtures import casebook
from picker import (
    Picker, chances_table, parser, pick_text, reporting_failures,
)
from theme import Theme

SEED = 3
RUNS = 10


def seeded_theme(theme):
    return Theme(theme, seed=SEED)


class PickTest(unittest.TestCase):
    def test_the_same_seed_gives_the_same_picks(self):
        first_theme = seeded_theme(casebook.EVEN)
        first_picker = Picker(first_theme)
        second_theme = seeded_theme(casebook.EVEN)
        second_picker = Picker(second_theme)

        first = [first_picker.pick() for _ in range(RUNS)]
        second = [second_picker.pick() for _ in range(RUNS)]

        self.assertEqual(first, second)

    def test_each_pick_draws_again(self):
        theme = seeded_theme(casebook.EVEN)
        picker = Picker(theme)

        picks = {picker.pick() for _ in range(RUNS)}

        self.assertGreater(len(picks), 1)


class PickTextTest(unittest.TestCase):
    def test_a_pick_shows_its_perspective_and_then_its_reference(self):
        theme = Theme(casebook.ONE_OF_EACH)
        picker = Picker(theme)
        perspective, reference = picker.pick()
        rows = pick_text(perspective, reference).splitlines()

        expected = ["perspective: characters/host", "reference: scenes/dawn"]
        self.assertEqual(expected, rows)


class ChancesTableTest(unittest.TestCase):
    def test_each_perspective_shows_weight_score_and_rounded_chance(self):
        theme = Theme(casebook.WEIGHTED)
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
        theme = Theme(casebook.WEIGHTLESS)
        picker = Picker(theme)

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                picker.pick()

        why = "every option weighs 0"
        expected = f"Picker FAILED: MissingWeight: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_missing_options_flag_fails_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(["pick"])

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
