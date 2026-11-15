import tempfile
import unittest
from pathlib import Path

from even_theme import EVEN, EVEN_HOOKS
from picker import Picker


class PickerTestCase(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def hook(self, options, *more):
        args = ["hook", "--options", str(options), *more]
        with Picker.from_args(args) as picker:
            return picker.selections()

    def drawn(self, seed):
        return self.hook(EVEN, "--seed", str(seed))

    def assertFails(self, why, *hook_args):
        with self.assertRaises(SystemExit) as exited:
            self.hook(*hook_args)
        self.assertEqual(f"Picker FAILED: {why}", exited.exception.code)


class DrawTest(PickerTestCase):
    def test_every_hook_can_be_drawn(self):
        drawn = {self.drawn(seed) for seed in range(100)}
        self.assertEqual(EVEN_HOOKS, drawn)

    def test_the_same_seed_draws_the_same_hook(self):
        first = [self.drawn(seed) for seed in range(5)]
        again = [self.drawn(seed) for seed in range(5)]
        self.assertEqual(first, again)


class CommandLineTest(PickerTestCase):
    def test_a_flag_the_mode_doesnt_take_fails_naming_it(self):
        why = "unrecognized arguments: --colour red"
        self.assertFails(why, EVEN, "--colour", "red")

    def test_a_seed_that_isnt_a_whole_number_fails_saying_so(self):
        why = "argument --seed: invalid int value: 'seven'"
        self.assertFails(why, EVEN, "--seed", "seven")


class OptionsFileTest(PickerTestCase):
    def test_an_options_file_that_isnt_yaml_fails_naming_it(self):
        path = self.folder / "Dusk-options.yaml"
        path.write_text("pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", path)

    def test_an_options_file_that_cant_be_read_fails_naming_it(self):
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", path)
