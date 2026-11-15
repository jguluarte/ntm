import tempfile
import unittest
from pathlib import Path

from fixtures import EVEN, EVEN_DRAWS, EVEN_HOOKS, SHAPELESS, SILENT
from picker import Picker


class PickerTestCase(unittest.TestCase):
    def pick(self, *args):
        with Picker.from_args(args) as picker:
            return picker.selections()

    def assertFails(self, line, *args):
        with self.assertRaises(SystemExit) as exited:
            self.pick(*args)
        self.assertEqual(line, exited.exception.code)


class HookDrawTest(PickerTestCase):
    EVEN_HOOK_LINES = {f"hook: {hook}" for hook in EVEN_HOOKS}

    def drawn(self, seed):
        return self.pick("hook", "--options", str(EVEN), "--seed", str(seed))

    def test_each_seed_draws_its_declared_hook(self):
        drawn = {seed: self.drawn(seed) for seed in EVEN_DRAWS}
        self.assertEqual(EVEN_DRAWS, drawn)

    def test_the_declared_draws_reach_every_hook(self):
        self.assertEqual(self.EVEN_HOOK_LINES, set(EVEN_DRAWS.values()))

    def test_without_a_seed_each_run_draws_afresh(self):
        drawn = {self.pick("hook", "--options", str(EVEN)) for _ in range(50)}
        self.assertEqual(set(), drawn - self.EVEN_HOOK_LINES)
        self.assertGreater(len(drawn), 1)


class FailureTest(PickerTestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def test_a_theme_without_hooks_fails_saying_so(self):
        why = "no pool in the options file gives a hook"
        line = f"Picker FAILED: NoHooks: {why}"
        self.assertFails(line, "hook", "--options", str(SILENT))

    def test_an_options_file_without_pools_fails(self):
        line = "Picker FAILED: KeyError: 'pools'"
        self.assertFails(line, "hook", "--options", str(SHAPELESS))

    def test_a_missing_options_flag_fails(self):
        why = "the following arguments are required: --options"
        line = f"Picker FAILED: ArgumentError: {why}"
        self.assertFails(line, "hook")

    def test_an_options_file_that_isnt_there_fails(self):
        path = self.folder / "Gone-options.yaml"
        why = f"[Errno 2] No such file or directory: '{path}'"
        line = f"Picker FAILED: FileNotFoundError: {why}"
        self.assertFails(line, "hook", "--options", str(path))

    def test_text_that_isnt_yaml_fails_on_one_line(self):
        path = self.folder / "Broken-options.yaml"
        path.write_text("pools: a: b\n")
        why = "mapping values are not allowed here"
        where = f'in "{path}", line 1, column 9'
        line = f"Picker FAILED: ScannerError: {why} {where}"
        self.assertFails(line, "hook", "--options", str(path))
