import unittest

from fixtures import baker_street, casebook
from picker import Picker, pick_text, reporting_failures
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
        theme = seeded_theme(baker_street.OPTIONS)
        picker = Picker(theme)
        perspective, reference = picker.pick()
        rows = pick_text(perspective, reference).splitlines()

        expected = [
            "perspective: characters/detective",
            "reference: scenes/stakeout",
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
