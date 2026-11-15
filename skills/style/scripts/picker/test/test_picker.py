import tempfile
import unittest
from pathlib import Path

from fixtures import EVEN, EVEN_HOOKS
from picker import Picker


class PickerTestCase(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def pick(self, *args):
        with Picker.from_args(args) as picker:
            return picker.selections()

    def pick_hook(self, options, *flags):
        return self.pick("hook", "--options", str(options), *flags)

    def drawn(self, seed):
        return self.pick_hook(EVEN, "--seed", str(seed))

    def assertFails(self, why, pick, *args):
        with self.assertRaises(SystemExit) as exited:
            pick(*args)
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
    def test_an_unknown_mode_fails_naming_the_modes(self):
        why = "argument mode: invalid choice: 'hooks' (choose from 'hook')"
        self.assertFails(why, self.pick, "hooks")

    def test_a_flag_the_mode_doesnt_take_fails_naming_it(self):
        why = "unrecognized arguments: --colour red"
        self.assertFails(why, self.pick_hook, EVEN, "--colour", "red")

    def test_a_seed_that_isnt_a_whole_number_fails_saying_so(self):
        why = "argument --seed: invalid int value: 'seven'"
        self.assertFails(why, self.pick_hook, EVEN, "--seed", "seven")


class OptionsFileTest(PickerTestCase):
    def options_file(self, text):
        path = self.folder / "Dusk-options.yaml"
        path.write_text(text)
        return path

    def test_an_options_file_that_cant_be_read_fails_naming_it(self):
        path = self.folder / "Gone-options.yaml"
        why = f"[Errno 2] No such file or directory: '{path}'"
        self.assertFails(why, self.pick_hook, path)

    def test_an_options_file_that_isnt_yaml_fails_naming_it(self):
        path = self.options_file("pools: a: b\n")
        where = f'in "{path}", line 1, column 9'
        why = f"mapping values are not allowed here {where}"
        self.assertFails(why, self.pick_hook, path)

    def test_an_options_file_without_pools_fails_saying_so(self):
        path = self.options_file("theme: Dusk\n")
        why = "the options file has no pools"
        self.assertFails(why, self.pick_hook, path)

    def test_a_pool_without_entries_fails_naming_it(self):
        path = self.options_file("pools:\n  scenes:\n    gives: [hook]\n")
        why = "pool scenes needs gives and entries"
        self.assertFails(why, self.pick_hook, path)

    def test_an_options_file_without_hooks_fails_saying_so(self):
        path = self.options_file("pools:\n  cast: {gives: [], entries: {}}\n")
        why = "the options file has no hooks"
        self.assertFails(why, self.pick_hook, path)
