import argparse
import contextlib
import sys

from theme import Lottery, Theme, ThemeOptions


class Picker:
    def __init__(
            self, theme, options=ThemeOptions(), seed=None,
            shows_chances=False):
        self.theme = theme
        self.options = options
        self.seed = seed
        self.shows_chances = shows_chances

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            theme = Theme(flags.options)
            options = ThemeOptions(flags.type)
            return cls(theme, options, flags.seed, flags.shows_chances)

    def pick_option(self):
        with self._reporting_failures():
            Lottery.set_seed(self.seed)
            lottery = self.theme.lottery_for(self.options)
            option = lottery.draw()
            return f"hook: {option.name}"

    def chances_table(self):
        with self._reporting_failures():
            lottery = self.theme.lottery_for(self.options)

            rows = [("hook", "weight", "score", "chance")]
            for option, chance in lottery.chance_by_candidate.items():
                weight = f"{option.weight:g}"
                score = f"{option.score:g}"
                rounded_chance = f"{chance:.2f}"
                rows.append((option.name, weight, score, rounded_chance))

            return self._table(rows)

    @staticmethod
    def _table(rows):
        widths = [max(len(cell) for cell in column) for column in zip(*rows)]
        name_width, *cell_widths = widths
        lines = []
        for name, *cells in rows:
            right_aligned = [
                cell.rjust(width) for cell, width in zip(cells, cell_widths)
            ]
            lines.append("  ".join([name.ljust(name_width), *right_aligned]))

        return "\n".join(lines)

    @staticmethod
    def _parser():
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        subcommand = subcommands.add_parser("hook", exit_on_error=False)
        subcommand.add_argument("--options", required=True)
        subcommand.add_argument("--type", default="")
        subcommand.add_argument("--seed", type=int)
        subcommand.add_argument(
            "--chances", dest="shows_chances", action="store_true",
        )
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
    if picker.shows_chances:
        print(picker.chances_table())

    else:
        print(picker.pick_option())
