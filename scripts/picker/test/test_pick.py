import subprocess
import sys
from pathlib import Path

from picker_test_case import PickerTestCase

PICK = Path(__file__).parents[1] / "pick"


class PickTest(PickerTestCase):
    def pick(self, *arguments):
        argv = [sys.executable, str(PICK), *arguments]
        return subprocess.run(argv, capture_output=True, text=True, check=False)

    def test_a_pick_prints_the_hook(self):
        arguments = self.arguments("Even", "--seed", "1")
        printed = self.pick("hook", *arguments).stdout.splitlines()
        names = [line.split(": ")[0] for line in printed]
        self.assertEqual(["hook"], names)

    def test_a_failure_prints_one_line_on_stderr_and_exits_1(self):
        ran = self.pick("hook")
        expected = (1, "Picker FAILED: pick hook needs --options\n")
        self.assertEqual(expected, (ran.returncode, ran.stderr))

    def test_an_unknown_mode_fails_naming_the_modes(self):
        usage = "usage: pick hook, as README.md beside it says"
        self.assertEqual(f"Picker FAILED: {usage}\n", self.pick("hooks").stderr)
