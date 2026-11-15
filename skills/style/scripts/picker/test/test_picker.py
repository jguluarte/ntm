import unittest

import fixtures
from picker import Options, Picker


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

        self.assertEqual("hook: scenes/dawn", drawn)

    def test_the_seed_is_optional(self):
        args = make_picker_args(fixtures.EVEN)

        picker = Picker.from_args(args)

        self.assertIsNone(picker.seed)

    def test_a_missing_options_flag_fails_naming_it(self):
        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(["hook"])

        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = make_picker_args(fixtures.EVEN, seed="seven")

        why = "argument --seed: invalid int value: 'seven'"
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
        options = Options(fixtures.EVEN)

        expected = {
            0: "hook: characters/host",
            1: "hook: scenes/noon",
            2: "hook: scenes/dawn",
            3: "hook: scenes/noon",
            4: "hook: scenes/noon",
            5: "hook: scenes/dusk",
        }

        drawn = {seed: Picker(options, seed).pick_hook() for seed in expected}

        self.assertEqual(expected, drawn)

    def test_without_a_seed_runs_draw_different_hooks(self):
        picker = Picker(Options(fixtures.EVEN))

        attempts = 50
        drawn = {
            picker.pick_hook() for _ in range(attempts)
        }

        self.assertGreater(len(drawn), 1)

    def test_only_speaker_pools_fails_saying_no_pool_gives_a_hook(self):
        picker = Picker(Options(fixtures.SPEAKERS_ONLY))

        why = "no pool in the options file gives a hook"
        expected = f"Picker FAILED: NoHooks: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick_hook()

        self.assertEqual(expected, exited.exception.code)
