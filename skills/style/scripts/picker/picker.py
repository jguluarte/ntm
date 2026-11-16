import argparse
import contextlib
import random
import sys
from datetime import date

from theme import History, InvalidOptions, Theme, ThemeOptions


class Picker:
    def __init__(
            self, theme, theme_options=ThemeOptions(), history=History(),
            seed=None, shows_chances=False):
        self.theme = theme
        self.theme_options = theme_options
        self.history = history
        self.seed = seed
        self.shows_chances = shows_chances

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            if flags.history and not flags.today:
                raise argparse.ArgumentError(None, "--history needs --today")

            theme = Theme(flags.options)
            history = History(flags.history, flags.today)
            return cls(
                theme, flags.theme_options, history, flags.seed,
                flags.shows_chances,
            )

    def pick_hook(self):
        with self._reporting_failures():
            generator = random.Random(self.seed)
            kind_lottery = self.theme.kind_lottery_for(self.theme_options)
            kind = self._draw(generator, kind_lottery)
            hook_lottery = self.theme.hook_lottery_for(
                self.theme_options, kind, self.history,
            )
            hook = self._draw(generator, hook_lottery)
            return f"hook: {hook.name}"

    def chances_table(self):
        with self._reporting_failures():
            kind_lottery = self.theme.kind_lottery_for(self.theme_options)
            hook_chances = {}
            for kind in kind_lottery:
                hook_chances.update(
                    self.theme.hook_lottery_for(
                        self.theme_options, kind, self.history,
                    ),
                )

            kind_rows = self._chance_rows("kind", "chance", kind_lottery)
            hook_rows = self._chance_rows(
                "hook", "chance in kind", hook_chances,
            )
            return f"{ self._table(kind_rows) }\n\n{ self._table(hook_rows) }"

    @staticmethod
    def _draw(generator, lottery):
        candidates = list(lottery)
        [drawn] = generator.choices(candidates, weights=lottery.values())
        return drawn

    @staticmethod
    def _chance_rows(name_heading, chance_heading, chances):
        rows = [(name_heading, "weight", "score", chance_heading)]
        for candidate, chance in chances.items():
            weight = f"{candidate.weight:g}"
            score = f"{candidate.score:g}"
            rounded_chance = f"{chance:.2f}"
            rows.append((candidate.name, weight, score, rounded_chance))

        return rows

    @staticmethod
    def _table(rows):
        widths = [max(len(cell) for cell in column) for column in zip(*rows)]
        name_width, *cell_widths = widths
        lines = []
        for name, *cells in rows:
            right_aligned = map(str.rjust, cells, cell_widths)
            lines.append("  ".join([name.ljust(name_width), *right_aligned]))

        return "\n".join(lines)

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
        hook.add_argument("--history")
        hook.add_argument("--today", type=cls._parse_date)
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
    def _parse_date(text):
        try:
            return date.fromisoformat(text)
        except ValueError:
            why = f"not a date as YYYY-MM-DD: {text}"
            raise argparse.ArgumentTypeError(why) from None

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
