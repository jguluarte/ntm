import argparse
import contextlib
import random
import sys

from theme import Theme, ThemeOptions


class Picker:
    def __init__(self, theme, seed=None, theme_options=ThemeOptions()):
        self.theme = theme
        self.seed = seed
        self.theme_options = theme_options

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            theme = Theme(flags.options)
            theme_options = ThemeOptions.parse(flags.theme_options)
            return cls(theme, flags.seed, theme_options)

    def pick_hook(self):
        with self._reporting_failures():
            hooks = self.theme.hooks_for(self.theme_options)
            generator = random.Random(self.seed)
            return f"hook: { generator.choice(hooks) }"

    @staticmethod
    def _parser():
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        hook = subcommands.add_parser("hook", exit_on_error=False)
        hook.add_argument("--options", required=True)
        hook.add_argument("--for", dest="theme_options")
        hook.add_argument("--seed", type=int)
        return parser

    @staticmethod
    @contextlib.contextmanager
    def _reporting_failures():
        try:
            yield
        except Exception as failure:
            # Every failure, a bug included, is one line for the skill to read.
            why = " ".join(str(failure).split())
            sys.exit(f"Picker FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    args = sys.argv[1:]

    picker = Picker.from_args(args)
    selections = picker.pick_hook()

    print(selections)
