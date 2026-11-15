import random

from exceptions import NoHooks
from options import Options

OPTIONS = "--options"
SEED = "--seed"
HOOK_LINE = "hook: {}"


class HookMode:
    NAME = "hook"

    def __init__(self, options, generator):
        self.options = options
        self.generator = generator

    @classmethod
    def add_subcommand(cls, subcommands):
        subcommand = subcommands.add_parser(cls.NAME, exit_on_error=False)
        subcommand.add_argument(OPTIONS, required=True)
        subcommand.add_argument(SEED, type=int)
        subcommand.set_defaults(mode=cls)

    @classmethod
    def from_flags(cls, flags):
        options = Options.load(flags.options)
        return cls(options, random.Random(flags.seed))

    def selections(self):
        hooks = self.options.hooks()
        if not hooks:
            raise NoHooks()
        hook = self.generator.choice(hooks)
        return HOOK_LINE.format(hook)
