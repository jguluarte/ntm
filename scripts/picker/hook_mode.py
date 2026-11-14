import random
import re

from draw import Draw
from failure import PickerFailed
from input_files import YamlFile
from options import HOOK, Options

NO_HOOKS = "the options file has no hooks"
WHOLE_NUMBER = re.compile("[0-9]+")


class HookMode:
    NAME = "hook"
    REQUIRED_FLAGS = ("--options",)
    OPTIONAL_FLAGS = ("--seed",)

    def __init__(self, flags):
        self.options = Options(YamlFile(flags["--options"]).load())
        self.random = self._seeded(flags["--seed"])

    def report(self):
        hooks = self.options.hooks()
        self._require_drawable(hooks)
        hook = Draw(hooks).pick(self.random.random())
        return f"{HOOK}: {hook.id}"

    @staticmethod
    def _seeded(seed):
        if seed and not WHOLE_NUMBER.fullmatch(seed):
            raise PickerFailed("--seed takes a whole number")
        return random.Random(int(seed) if seed else None)

    @staticmethod
    def _require_drawable(hooks):
        if not hooks:
            raise PickerFailed(NO_HOOKS)
