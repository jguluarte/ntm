import random

from draw import Draw
from failure import PickerFailed
from input_files import YamlFile
from options import Options

OPTIONS = "--options"
SEED = "--seed"
HOOK_LINE = "hook: {}"
NO_HOOKS = "the options file has no hooks"


class HookMode:
    NAME = "hook"

    def __init__(self, flags):
        self.options = Options(YamlFile(flags.options).load())
        self.generator = random.Random(flags.seed)

    @staticmethod
    def add_flags(flags):
        flags.add_argument(OPTIONS, required=True)
        flags.add_argument(SEED, type=int)

    def report(self):
        hooks = self.options.hooks()
        self._require_drawable(hooks)
        hook = Draw(hooks).pick(self.generator.random())
        return HOOK_LINE.format(hook.id)

    @staticmethod
    def _require_drawable(hooks):
        if not hooks:
            raise PickerFailed(NO_HOOKS)
