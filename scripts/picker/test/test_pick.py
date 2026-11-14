import subprocess
import sys
import unittest
from pathlib import Path

from even_theme import EVEN, EVEN_HOOKS

PICK = Path(__file__).parents[1] / "pick"


class PickTest(unittest.TestCase):
    def pick(self, *arguments):
        argv = [sys.executable, str(PICK), *arguments]
        return subprocess.run(argv, capture_output=True, text=True, check=False)

    def test_a_pick_prints_one_of_the_hooks(self):
        ran = self.pick("hook", "--options", str(EVEN), "--seed", "1")
        self.assertIn(ran.stdout.rstrip("\n"), EVEN_HOOKS)

    def test_a_failure_prints_one_line_on_stderr_and_exits_1(self):
        ran = self.pick("hook")
        why = "the following arguments are required: --options"
        expected = (1, f"Picker FAILED: {why}\n")
        self.assertEqual(expected, (ran.returncode, ran.stderr))

    def test_an_unknown_mode_fails_naming_the_modes(self):
        why = "argument mode: invalid choice: 'hooks' (choose from 'hook')"
        self.assertEqual(f"Picker FAILED: {why}\n", self.pick("hooks").stderr)
