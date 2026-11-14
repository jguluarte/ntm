import tempfile
import unittest
from pathlib import Path

from command_line import CommandLine
from even_theme import EVEN, EVEN_HOOKS
from failure import PickerFailed
from hook_mode import HookMode


class HookModeTest(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def report(self, options, *more):
        arguments = ["hook", "--options", str(options), *more]
        flags = CommandLine.for_modes([HookMode]).parse_args(arguments)
        return HookMode(flags).report()

    def drawn(self, seed):
        return self.report(EVEN, "--seed", str(seed))

    def assertFails(self, why, action, *arguments):
        with self.assertRaises(PickerFailed) as failure:
            action(*arguments)
        self.assertEqual(why, str(failure.exception))


class DrawTest(HookModeTest):
    def test_every_hook_can_be_drawn(self):
        drawn = {self.drawn(seed) for seed in range(100)}
        self.assertEqual(EVEN_HOOKS, drawn)

    def test_the_same_seed_draws_the_same_hook(self):
        first = [self.drawn(seed) for seed in range(5)]
        again = [self.drawn(seed) for seed in range(5)]
        self.assertEqual(first, again)


class FlagsTest(HookModeTest):
    def test_a_flag_the_mode_doesnt_take_fails_naming_it(self):
        why = "unrecognized arguments: --colour red"
        self.assertFails(why, self.report, EVEN, "--colour", "red")

    def test_a_seed_that_isnt_a_whole_number_fails_saying_so(self):
        why = "argument --seed: invalid int value: 'seven'"
        self.assertFails(why, self.report, EVEN, "--seed", "seven")


class OptionsFileTest(HookModeTest):
    def test_an_options_file_that_isnt_yaml_fails_naming_it(self):
        path = self.folder / "Dusk-options.yaml"
        path.write_text("pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", self.report, path)

    def test_an_options_file_that_cant_be_read_fails_naming_it(self):
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", self.report, path)
