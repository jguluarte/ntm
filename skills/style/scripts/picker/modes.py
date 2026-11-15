import random

from options import Options

OPTIONS = "--options"
SEED = "--seed"
HOOK_LINE = "hook: {}"
NO_HOOKS = "no pool in the options file gives a hook"


class HookMode:
    NAME = "hook"

    def __init__(self, options_file, seed=None):
        self.options_file = options_file
        self.seed = seed

    @classmethod
    def add_subcommand(cls, subcommands):
        subcommand = subcommands.add_parser(cls.NAME, exit_on_error=False)
        subcommand.add_argument(OPTIONS, required=True)
        subcommand.add_argument(SEED, type=int)
        subcommand.set_defaults(mode=cls)

    @classmethod
    def from_flags(cls, flags):
        return cls(flags.options, flags.seed)

    def pick(self):
        options = Options.load(self.options_file)
        hooks = options.hooks()
        if not hooks:
            raise ValueError(NO_HOOKS)
        generator = random.Random(self.seed)
        hook = generator.choice(hooks)
        return HOOK_LINE.format(hook)
