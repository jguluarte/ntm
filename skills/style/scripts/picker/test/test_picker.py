import unittest

from fixtures import (
    EVEN, EVEN_DRAWS, EVEN_HOOKS,
    NOT_THERE, NOT_YAML, POOL_WITHOUT_GIVES, SPEAKERS_ONLY, WITHOUT_POOLS,
)
from modes import HookMode
from picker import Picker

RUNS = 50


class CommandLineTest(unittest.TestCase):
    def test_hook_takes_an_options_file_and_a_seed(self):
        args = ["hook", "--options", "Even-options.yaml", "--seed", "2"]

        mode = Picker.from_args(args).mode

        self.assertIsInstance(mode, HookMode)
        self.assertEqual("Even-options.yaml", mode.options_file)
        self.assertEqual(2, mode.seed)

    def test_the_seed_is_optional(self):
        args = ["hook", "--options", "Even-options.yaml"]

        mode = Picker.from_args(args).mode

        self.assertIsNone(mode.seed)

    def test_a_missing_options_flag_fails_naming_it(self):
        why = "the following arguments are required: --options"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(["hook"])

        self.assertEqual(expected, exited.exception.code)

    def test_a_seed_that_isnt_a_whole_number_fails_naming_it(self):
        args = ["hook", "--options", "Even-options.yaml", "--seed", "seven"]
        why = "argument --seed: invalid int value: 'seven'"
        expected = f"Picker FAILED: ArgumentError: {why}"

        with self.assertRaises(SystemExit) as exited:
            Picker.from_args(args)

        self.assertEqual(expected, exited.exception.code)


class PickFailureTest(unittest.TestCase):
    def test_a_pool_without_gives_fails_naming_gives(self):
        picker = Picker(HookMode(options_file=POOL_WITHOUT_GIVES))
        why = "$.pools.scenes: 'gives' is a required property"
        expected = f"Picker FAILED: ValueError: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick()

        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_without_pools_fails_naming_pools(self):
        picker = Picker(HookMode(options_file=WITHOUT_POOLS))
        why = "$: 'pools' is a required property"
        expected = f"Picker FAILED: ValueError: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick()

        self.assertEqual(expected, exited.exception.code)

    def test_only_speaker_pools_fails_saying_no_pool_gives_a_hook(self):
        picker = Picker(HookMode(options_file=SPEAKERS_ONLY))
        why = "no pool in the options file gives a hook"
        expected = f"Picker FAILED: ValueError: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick()

        self.assertEqual(expected, exited.exception.code)

    def test_an_options_file_that_isnt_there_fails_naming_it(self):
        picker = Picker(HookMode(options_file=NOT_THERE))
        why = f"[Errno 2] No such file or directory: '{NOT_THERE}'"
        expected = f"Picker FAILED: FileNotFoundError: {why}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick()

        self.assertEqual(expected, exited.exception.code)

    def test_text_that_isnt_yaml_fails_on_one_line(self):
        picker = Picker(HookMode(options_file=NOT_YAML))
        why = "mapping values are not allowed here"
        where = f'in "{NOT_YAML}", line 1, column 9'
        expected = f"Picker FAILED: ScannerError: {why} {where}"

        with self.assertRaises(SystemExit) as exited:
            picker.pick()

        self.assertEqual(expected, exited.exception.code)


class HookDrawTest(unittest.TestCase):
    def test_each_seed_draws_its_declared_hook(self):
        drawn = {}
        for seed in EVEN_DRAWS:
            picker = Picker(HookMode(options_file=EVEN, seed=seed))
            drawn[seed] = picker.pick()

        self.assertEqual(EVEN_DRAWS, drawn)

    def test_the_declared_draws_reach_every_hook(self):
        lines = EVEN_DRAWS.values()
        reached = {line.removeprefix("hook: ") for line in lines}

        self.assertEqual(set(EVEN_HOOKS), reached)

    def test_without_a_seed_runs_draw_different_hooks(self):
        picker = Picker(HookMode(options_file=EVEN))

        drawn = {picker.pick() for _ in range(RUNS)}

        self.assertGreater(len(drawn), 1)
