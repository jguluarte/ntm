import random

from exceptions import NoHooks
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
        if not hooks:
            raise NoHooks()
        hook = self.generator.choice(hooks)
        return HOOK_LINE.format(hook)


MODES = {HookMode.NAME: HookMode}
