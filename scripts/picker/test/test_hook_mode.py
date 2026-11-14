import tempfile
import unittest
from pathlib import Path

from failure import PickerFailed
from flags import Flags
from hook_mode import HookMode

EVEN = Path(__file__).parent / "fixtures" / "Even-options.yaml"
EVEN_HOOKS = {"hook: scenes/dawn", "hook: scenes/noon", "hook: scenes/dusk"}


class HookModeTest(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def report(self, options, *more):
        flags = Flags(HookMode, ["--options", str(options), *more])
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
        why = "pick hook doesn't take --colour"
        self.assertFails(why, self.report, EVEN, "--colour", "red")

    def test_a_seed_that_isnt_a_whole_number_fails_saying_so(self):
        why = "--seed takes a whole number"
        self.assertFails(why, self.report, EVEN, "--seed", "seven")


class OptionsFileTest(HookModeTest):
    def test_an_options_file_that_isnt_yaml_fails_naming_it(self):
        path = self.folder / "Dusk-options.yaml"
        path.write_text("pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", self.report, path)

    def test_an_options_file_that_cant_be_read_fails_naming_it(self):
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", self.report, path)
