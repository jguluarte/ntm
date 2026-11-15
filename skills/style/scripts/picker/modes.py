import random

from exceptions import PickerFailed
from options import Options

OPTIONS = "--options"
SEED = "--seed"
HOOK_LINE = "hook: {}"


class HookMode:
    NAME = "hook"

    def __init__(self, flags):
        self.options = Options.load(flags.options)
        self.generator = random.Random(flags.seed)

    @staticmethod
    def add_flags(parser):
        parser.add_argument(OPTIONS, required=True)
        parser.add_argument(SEED, type=int)

    def selections(self):
        hooks = self.options.hooks()
        self._require_drawable(hooks)
        hook = self.generator.choice(hooks)
        return HOOK_LINE.format(hook.id)

    @staticmethod
    def _require_drawable(hooks):
        if not hooks:
            raise PickerFailed("the options file has no hooks")


MODES = {HookMode.NAME: HookMode}
