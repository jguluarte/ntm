import re
import secrets

from failure import PickerFailed

WHOLE_NUMBER = re.compile("[0-9]+")
SEED_BITS = 32


class Flags:
    def __init__(self, mode, arguments):
        self.mode = mode
        self.values = {}
        self._read(iter(arguments))
        self._require(mode.REQUIRED_FLAGS)

    def __getitem__(self, flag):
        return self.values.get(flag, "")

    @property
    def seed(self):
        text = self["--seed"]
        if not text:
            return secrets.randbits(SEED_BITS)
        if not WHOLE_NUMBER.fullmatch(text):
            raise PickerFailed("--seed takes a whole number")
        return int(text)

    def _read(self, arguments):
        for flag in arguments:
            self._require_taken(flag)
            self.values[flag] = self._value_after(flag, arguments)

    def _require_taken(self, flag):
        taken = self.mode.REQUIRED_FLAGS + self.mode.OPTIONAL_FLAGS
        if flag not in taken:
            raise PickerFailed(f"pick {self.mode.NAME} doesn't take {flag}")

    def _require(self, flags):
        for flag in flags:
            if not self[flag]:
                raise PickerFailed(f"pick {self.mode.NAME} needs {flag}")

    @staticmethod
    def _value_after(flag, arguments):
        value = next(arguments, None)
        if value is None:
            raise PickerFailed(f"{flag} needs a value")
        return value
