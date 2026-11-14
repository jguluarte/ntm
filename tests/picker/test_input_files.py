import sys
from unittest import mock

from input_files import PYYAML_NEEDED, YamlFile
from picker_test import PickerTest

OPTIONS = """\
    pools:
      scenes:
        gives: [hook]
    """


class YamlFileTest(PickerTest):
    def test_a_yaml_file_loads_as_its_data(self):
        options = YamlFile(self.write("Dusk-options.yaml", OPTIONS))
        expected = {"pools": {"scenes": {"gives": ["hook"]}}}
        self.assertEqual(expected, options.load())

    def test_a_file_that_isnt_yaml_fails_in_one_line(self):
        path = self.write("Dusk-options.yaml", "pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", YamlFile(path).load)

    def test_a_file_that_cant_be_read_fails_in_one_line(self):
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", YamlFile(path).load)

    def test_without_pyyaml_it_fails_in_one_line(self):
        options = YamlFile(self.write("Dusk-options.yaml", OPTIONS))
        with mock.patch.dict(sys.modules, {"yaml": None}):
            self.assertFails(PYYAML_NEEDED, options.load)
