from draw import Draw
from failure import PickerFailed
from input_files import YamlFile
from options import HOOK, Options
from random_numbers import RandomNumbers

NO_HOOKS = "the options file has no hooks"


class HookMode:
    NAME = "hook"
    REQUIRED_FLAGS = ("--options",)
    OPTIONAL_FLAGS = ("--seed",)

    def __init__(self, flags):
        self.options = Options(YamlFile(flags["--options"]).load())
        self.numbers = RandomNumbers(flags.seed)

    def report(self):
        hooks = self.options.hooks()
        self._require_drawable(hooks)
        hook = Draw(hooks).pick(next(self.numbers))
        return f"{HOOK}: {hook.id}"

    @staticmethod
    def _require_drawable(hooks):
        if not hooks:
            raise PickerFailed(NO_HOOKS)
