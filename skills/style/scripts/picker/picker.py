import argparse
import contextlib
import random
import sys
from decimal import ROUND_HALF_UP, Decimal

from theme import InvalidOptions, Theme, ThemeOptions


class Picker:
    def __init__(
            self, theme, theme_options=ThemeOptions(), seed=None,
            shows_chances=False):
        self.theme = theme
        self.theme_options = theme_options
        self.seed = seed
        self.shows_chances = shows_chances

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            theme = Theme(flags.options)
            return cls(
                theme, flags.theme_options, flags.seed, flags.shows_chances,
            )

    def pick_hook(self):
        with self._reporting_failures():
            chances = self.theme.lottery_for(self.theme_options)
            hooks = list(chances)
            generator = random.Random(self.seed)
            [hook] = generator.choices(hooks, weights=chances.values())
            return f"hook: {hook.name}"

    def chances_table(self):
        with self._reporting_failures():
            chances = self.theme.lottery_for(self.theme_options)

            rows = [("hook", "weight", "score", "chance")]
            for hook, chance in chances.items():
                weight, score = f"{hook.weight:g}", f"{hook.score:g}"
                rounded_chance = self._to_hundredths(chance)
                rows.append((hook.name, weight, score, rounded_chance))

            return self._table(rows)

    @staticmethod
    def _table(rows):
        widths = [max(len(cell) for cell in column) for column in zip(*rows)]
        lines = []
        for name, *numbers in rows:
            cells = [name.ljust(widths[0])]
            for number, width in zip(numbers, widths[1:]):
                cells.append(number.rjust(width))

            lines.append("  ".join(cells))

        return "\n".join(lines)

    @staticmethod
    def _to_hundredths(chance):
        hundredth = Decimal("0.01")
        rounded = Decimal(chance).quantize(hundredth, rounding=ROUND_HALF_UP)
        return str(rounded)

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
        hook.add_argument(
            "--chances", dest="shows_chances", action="store_true",
        )
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
    if picker.shows_chances:
        print(picker.chances_table())

    else:
        print(picker.pick_hook())
