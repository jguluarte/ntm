import random

from failure import PickerFailed
from options import Options
from yaml_file import YamlFile

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
    def add_flags(parser):
        parser.add_argument(OPTIONS, required=True)
        parser.add_argument(SEED, type=int)

    def report(self):
        hooks = self.options.hooks()
        self._require_drawable(hooks)
        hook = self.generator.choice(hooks)
        return HOOK_LINE.format(hook.id)

    @staticmethod
    def _require_drawable(hooks):
        if not hooks:
            raise PickerFailed(NO_HOOKS)
