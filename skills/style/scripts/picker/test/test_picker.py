import unittest

import fixtures
from picker import Picker
from theme import Theme, ThemeOptions


def make_picker_args(options, *flags):
    return ["hook", "--options", str(options), *flags]


class CommandLineTest(unittest.TestCase):
    def test_hook_draws_from_the_options_file_with_the_seed(self):
        args = make_picker_args(fixtures.EVEN, "--seed", "2")

        picker = Picker.from_args(args)
        drawn = picker.pick_hook()

        self.assertEqual("hook: scenes/dawn", drawn)

    def test_hook_draws_only_hooks_fitting_the_theme_options(self):
        args = make_picker_args(fixtures.EVERY_WHEN, "--for", "weekly,big_win")

        picker = Picker.from_args(args)
        drawn = picker.pick_hook()

        self.assertEqual("hook: scenes/big_win", drawn)

    def test_the_seed_is_optional(self):
        args = make_picker_args(fixtures.EVEN)

        picker = Picker.from_args(args)

        self.assertIsNone(picker.seed)

    def test_the_theme_options_are_optional(self):
        args = make_picker_args(fixtures.EVEN)

        picker = Picker.from_args(args)

        self.assertEqual(ThemeOptions(), picker.theme_options)

    def test_a_missing_options_flag_fails_naming_it(self):
        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(["hook"])

        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = make_picker_args(fixtures.EVEN, "--seed", "seven")

        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        self.assertEqual(expected, exited.exception.code)

    def test_a_for_that_isnt_a_valid_combination_fails_naming_it(self):
        args = make_picker_args(fixtures.EVEN, "--for", "morning,evening")

        why = "argument --for: more than one reminder type: evening, morning"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        args = make_picker_args(fixtures.NOT_THERE)

        why = f"[Errno 2] No such file or directory: '{fixtures.NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        self.assertEqual(expected, exited.exception.code)


class PickHookTest(unittest.TestCase):
    def test_each_seed_draws_its_declared_hook(self):
        theme = Theme(fixtures.EVEN)

        expected = {
            0: "hook: characters/host",
            1: "hook: scenes/noon",
            2: "hook: scenes/dawn",
            3: "hook: scenes/noon",
            4: "hook: scenes/noon",
            5: "hook: scenes/dusk",
        }

        drawn = {
            seed: Picker(theme, seed=seed).pick_hook() for seed in expected
        }

        self.assertEqual(expected, drawn)

    def test_without_a_seed_runs_draw_different_hooks(self):
        picker = Picker(Theme(fixtures.EVEN))

        attempts = 50
        drawn = {
            picker.pick_hook() for _ in range(attempts)
        }

        self.assertGreater(len(drawn), 1)

    def test_a_message_no_hook_fits_fails_naming_its_options(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        picker = Picker(theme, ThemeOptions.parse("morning"))

        why = "no hook fits morning"
        expected = f"Picker FAILED: MissingHook: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick_hook()

        self.assertEqual(expected, exited.exception.code)
