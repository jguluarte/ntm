from failure import PickerFailed

PYYAML_NEEDED = "pick needs PyYAML"


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
        yaml = self._pyyaml()
        try:
            return yaml.safe_load(self.read())
        except yaml.YAMLError:
            raise PickerFailed(f"{self.path} isn't YAML") from None

    @staticmethod
    def _pyyaml():
        try:
            import yaml
        except ImportError:
            raise PickerFailed(PYYAML_NEEDED) from None
        return yaml
