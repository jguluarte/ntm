import tempfile
import textwrap
import unittest
from pathlib import Path

from failure import PickerFailed

FIXTURES = Path(__file__).parent / "fixtures"


class PickerTestCase(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.themes = FIXTURES

    def write(self, name, text):
        path = self.folder / name
        path.write_text(textwrap.dedent(text))
        return path

    def arguments(self, theme, *more):
        options = self.themes / f"{theme}-options.yaml"
        return ["--options", str(options), *more]

    def assertFails(self, why, action, *arguments):
        with self.assertRaises(PickerFailed) as failure:
            action(*arguments)
        self.assertEqual(why, str(failure.exception))
