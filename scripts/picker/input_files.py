import yaml

from failure import PickerFailed


class TextFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, encoding="utf-8") as file:
                return file.read()
        except OSError:
            raise PickerFailed(f"can't read {self.path}") from None


class YamlFile(TextFile):
    def load(self):
        try:
            return yaml.safe_load(self.read())
        except yaml.YAMLError:
            raise PickerFailed(f"{self.path} isn't YAML") from None
