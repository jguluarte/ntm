import unittest

from fixtures import baker_street
from pick_list import parser, pick_list_text
from picker import Picker, reporting_failures
from test_picker import seeded_theme

COUNT = 4


class PickListTextTest(unittest.TestCase):
    def test_the_picks_show_as_a_list_in_the_order_drawn(self):
        theme = seeded_theme(baker_street.OPTIONS)
        picker = Picker(theme)
        picks = [picker.pick() for _ in range(COUNT)]
        rows = pick_list_text(picks).splitlines()

        expected = [
            "- perspective: characters/detective",
            "  reference: scenes/stakeout",
            "- perspective: scenes/stakeout",
            "  reference: shared_lines/any_time",
            "- perspective: scenes/stakeout",
            "  reference: shared_lines/any_time",
            "- perspective: characters/detective",
            "  reference: scenes/stakeout",
        ]
        self.assertEqual(expected, rows)


class ReportingFailuresTest(unittest.TestCase):
    def test_a_missing_options_flag_fails_naming_it(self):
        args = ["draw", "--count", str(COUNT)]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
