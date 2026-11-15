import argparse
import contextlib
import random
import sys

from theme import InvalidOptions, Theme, ThemeOptions


class Picker:
    def __init__(self, theme, theme_options=ThemeOptions(), seed=None):
        self.theme = theme
        self.theme_options = theme_options
        self.seed = seed

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            theme = Theme(flags.options)
            return cls(theme, flags.theme_options, flags.seed)

    def pick_hook(self):
        with self._reporting_failures():
            chances = self.theme.hook_chances_for(self.theme_options)
            hooks = list(chances)
            generator = random.Random(self.seed)
            [hook] = generator.choices(hooks, weights=chances.values())
            return f"hook: {hook}"

    @classmethod
    def _parser(cls):
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        hook = subcommands.add_parser("hook", exit_on_error=False)
        hook.add_argument("--options", required=True)
        hook.add_argument(
            "--type", dest="theme_options", type=cls._parse_theme_options,
            default=ThemeOptions(),
        )
        hook.add_argument("--seed", type=int)
        return parser

    @staticmethod
    def _parse_theme_options(text):
        try:
            return ThemeOptions.parse(text)
        except InvalidOptions as invalid:
            raise argparse.ArgumentTypeError(str(invalid)) from None

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
