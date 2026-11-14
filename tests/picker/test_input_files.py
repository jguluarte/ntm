import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from failure import PickerFailed
from input_files import PYYAML_NEEDED, YamlFile

OPTIONS = """\
    pools:
      scenes:
        gives: [hook]
    """


class YamlFileTest(unittest.TestCase):
    def setUp(self):
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def write(self, name, text):
        path = self.folder / name
        path.write_text(textwrap.dedent(text))
        return path

    def assertFails(self, why, action):
        with self.assertRaises(PickerFailed) as failure:
            action()
        self.assertEqual(why, str(failure.exception))

    def test_a_yaml_file_loads_as_its_data(self):
        options = YamlFile(self.write("Dusk-options.yaml", OPTIONS))
        expected = {"pools": {"scenes": {"gives": ["hook"]}}}
        self.assertEqual(expected, options.load())

    def test_a_file_that_isnt_yaml_fails_naming_it(self):
        path = self.write("Dusk-options.yaml", "pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", YamlFile(path).load)

    def test_a_file_that_cant_be_read_fails_naming_it(self):
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", YamlFile(path).load)

    def test_without_pyyaml_it_fails_saying_so(self):
        options = YamlFile(self.write("Dusk-options.yaml", OPTIONS))
        with mock.patch.dict(sys.modules, {"yaml": None}):
            self.assertFails(PYYAML_NEEDED, options.load)
