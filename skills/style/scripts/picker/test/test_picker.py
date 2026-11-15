import unittest
from datetime import date

import fixtures
from picker import Picker
from theme import History, Theme, ThemeOptions


def make_picker_args(options, **flags):
    args = ["hook", "--options", str(options)]

    for name, value in flags.items():
        args += [f"--{name}", str(value)]

    return args


class CommandLineTest(unittest.TestCase):
    def test_hook_draws_from_the_options_file_with_the_seed(self):
        args = make_picker_args(fixtures.EVEN, seed=2)
        picker = Picker.from_args(args)
        drawn = picker.pick_hook()

        self.assertEqual("hook: characters/host", drawn)

    def test_hook_draws_only_hooks_fitting_the_type(self):
        args = make_picker_args(fixtures.EVERY_TYPE, type="weekly,big_win")
        picker = Picker.from_args(args)
        drawn = picker.pick_hook()

        self.assertEqual("hook: scenes/big_win", drawn)

    def test_a_history_changes_which_hook_the_seed_draws(self):
        without_history = make_picker_args(fixtures.EVEN, seed=32)
        with_history = make_picker_args(
            fixtures.EVEN, seed=32, history=fixtures.EVEN_HISTORY,
            today="2026-11-15",
        )
        drawn = {
            "without history": Picker.from_args(without_history).pick_hook(),
            "with history": Picker.from_args(with_history).pick_hook(),
        }

        expected = {
            "without history": "hook: scenes/dawn",
            "with history": "hook: scenes/noon",
        }
        self.assertEqual(expected, drawn)

    def test_the_seed_is_optional(self):
        args = make_picker_args(fixtures.EVEN)
        picker = Picker.from_args(args)

        self.assertIsNone(picker.seed)

    def test_the_type_is_optional(self):
        args = make_picker_args(fixtures.EVEN)
        picker = Picker.from_args(args)

        self.assertEqual(ThemeOptions(), picker.theme_options)

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

    def test_a_type_that_isnt_a_valid_combination_fails_naming_it(self):
        args = make_picker_args(fixtures.EVEN, type="morning,evening")

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = "argument --type: more than one reminder type: evening, morning"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_history_without_today_fails_naming_both_flags(self):
        args = make_picker_args(fixtures.EVEN, history=fixtures.EVEN_HISTORY)

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = "--history needs --today"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_a_today_that_isnt_a_date_fails_naming_it(self):
        args = make_picker_args(
            fixtures.EVEN, history=fixtures.EVEN_HISTORY, today="15 Nov",
        )

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = "argument --today: not a date as YYYY-MM-DD: 15 Nov"
        expected = f"Picker FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        args = make_picker_args(fixtures.NOT_THERE)

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        why = f"[Errno 2] No such file or directory: '{fixtures.NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertEqual(expected, exited.exception.code)


class PickHookTest(unittest.TestCase):
    def test_each_seed_draws_its_declared_hook(self):
        theme = Theme(fixtures.EVEN)
        drawn = {
            seed: Picker(theme, seed=seed).pick_hook() for seed in range(6)
        }

        expected = {
            0: "hook: characters/host",
            1: "hook: scenes/dusk",
            2: "hook: characters/host",
            3: "hook: scenes/noon",
            4: "hook: scenes/dawn",
            5: "hook: characters/host",
        }
        self.assertEqual(expected, drawn)

    def test_without_a_seed_runs_draw_different_hooks(self):
        picker = Picker(Theme(fixtures.EVEN))

        attempts = 50
        drawn = {
            picker.pick_hook() for _ in range(attempts)
        }

        self.assertGreater(len(drawn), 1)

    def test_a_hook_weighing_0_is_never_drawn(self):
        theme = Theme(fixtures.WEIGHTED)
        drawn = {Picker(theme, seed=seed).pick_hook() for seed in range(50)}

        expected = {
            "hook: scenes/dawn", "hook: scenes/noon", "hook: characters/host",
        }
        self.assertEqual(expected, drawn)

    def test_a_message_no_hook_fits_fails_with_missing_hook(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        picker = Picker(theme, ThemeOptions.parse("morning"))

        with self.assertRaises(SystemExit) as exited:
            picker.pick_hook()

        why = "no hook fits morning"
        expected = f"Picker FAILED: MissingHook: {why}"
        self.assertEqual(expected, exited.exception.code)


class ChancesTableTest(unittest.TestCase):
    def test_the_documented_example_shows_the_documented_chances(self):
        picker = Picker(Theme(fixtures.WEIGHTED))
        rows = picker.chances_table().splitlines()

        expected = [
            "kind        chance",
            "scenes        0.88",
            "characters    0.13",
            "",
            "hook             chance in kind",
            "scenes/dawn                0.20",
            "scenes/noon                0.80",
            "scenes/dusk                0.00",
            "characters/host            1.00",
        ]
        self.assertEqual(expected, rows)

    def test_the_documented_rest_example_shows_the_documented_chances(self):
        theme = Theme(fixtures.EVEN)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        picker = Picker(theme, history=history)
        rows = picker.chances_table().splitlines()

        expected = [
            "kind        chance",
            "scenes        0.50",
            "characters    0.50",
            "",
            "hook             days since used  chance in kind",
            "scenes/dawn                    2            0.20",
            "scenes/noon                never            0.40",
            "scenes/dusk                never            0.40",
            "characters/host                2            1.00",
        ]
        self.assertEqual(expected, rows)

    def test_without_a_history_no_table_shows_days_since_used(self):
        picker = Picker(Theme(fixtures.EVEN))
        kind_table, hook_table = picker.chances_table().split("\n\n")
        shown = {
            "kind table": "days since used" in kind_table,
            "hook table": "days since used" in hook_table,
        }

        expected = {"kind table": False, "hook table": False}
        self.assertEqual(expected, shown)

    def test_with_a_history_only_the_hook_table_shows_days_since_used(self):
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        picker = Picker(Theme(fixtures.EVEN), history=history)
        kind_table, hook_table = picker.chances_table().split("\n\n")
        shown = {
            "kind table": "days since used" in kind_table,
            "hook table": "days since used" in hook_table,
        }

        expected = {"kind table": False, "hook table": True}
        self.assertEqual(expected, shown)

    def test_chances_where_every_fitting_hook_weighs_0_fail_naming_why(self):
        theme = Theme(fixtures.WEIGHTED)
        picker = Picker(theme, ThemeOptions.parse("big_win"))

        with self.assertRaises(SystemExit) as exited:
            picker.chances_table()

        why = "every hook that fits big_win weighs 0"
        expected = f"Picker FAILED: NoHookHasWeight: {why}"
        self.assertEqual(expected, exited.exception.code)
