import argparse
import contextlib
import sys

from theme import Theme


class Picker:
    def __init__(self, theme):
        self.theme = theme

    def pick(self):
        perspective = self.theme.draw_perspective()
        reference = self.theme.draw_reference_outside(perspective.kind)
        return perspective, reference


def parser():
    command_line = argparse.ArgumentParser(exit_on_error=False)
    subcommands = command_line.add_subparsers(required=True)
    subcommand = subcommands.add_parser("pick", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("--seed", type=int)
    subcommand.add_argument(
        "--chances", dest="shows_chances", action="store_true",
    )
    return command_line


def chances_table(lottery):
    rows = [("perspective", "weight", "score", "chance")]
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
        why = " ".join(str(failure).split())
        sys.exit(f"Picker FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    with reporting_failures():
        flags = parser().parse_args(sys.argv[1:])
        theme = Theme(flags.options, flags.seed)

        if flags.shows_chances:
            lottery = theme.perspective_lottery
            print(chances_table(lottery))

        else:
            picker = Picker(theme)
            perspective, reference = picker.pick()
            print(f"perspective: {perspective.name}")
            print(f"reference: {reference.name}")
