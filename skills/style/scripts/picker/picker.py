import argparse
import contextlib
import sys

from theme import Theme, ThemeOptions


class Picker:
    def __init__(self, theme, options=ThemeOptions()):
        self.theme = theme
        self.options = options

    def pick(self):
        option = self.theme.draw_from(self.options)
        return f"hook: {option.name}"


def parser():
    flags_parser = argparse.ArgumentParser(exit_on_error=False)
    subcommands = flags_parser.add_subparsers(required=True)
    subcommand = subcommands.add_parser("hook", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("--type", default="")
    subcommand.add_argument("--seed", type=int)
    subcommand.add_argument("--chances", action="store_true")
    return flags_parser


def chances_table(lottery):
    rows = [("hook", "weight", "score", "chance")]
    for option, chance in lottery.chance_by_candidate.items():
        weight = f"{option.weight:g}"
        score = f"{option.score:g}"
        rounded_chance = f"{chance:.2f}"
        rows.append((option.name, weight, score, rounded_chance))

    return _table(rows)


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


@contextlib.contextmanager
def reporting_failures():
    try:
        yield
    except Exception as failure:
        # Every failure, a bug included, is one line for the skill to read.
        why = " ".join(str(failure).split())
        sys.exit(f"Picker FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    with reporting_failures():
        flags = parser().parse_args()
        theme = Theme(flags.options, flags.seed)
        options = ThemeOptions(flags.type)

        if flags.chances:
            lottery = theme.lottery_for(options)
            print(chances_table(lottery))

        else:
            picker = Picker(theme, options)
            print(picker.pick())
