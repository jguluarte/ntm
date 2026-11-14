import tempfile
import textwrap
import unittest
from pathlib import Path

from failure import PickerFailed


class PickerTest(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def write(self, name, text):
        path = self.folder / name
        path.write_text(textwrap.dedent(text))
        return path

    def assertFails(self, why, action, *arguments):
        with self.assertRaises(PickerFailed) as failure:
            action(*arguments)
        self.assertEqual(why, str(failure.exception))
