import argparse
import sys

from picker import Picker, pick_text, reporting_failures
from theme import Theme


def parser():
    command_line = argparse.ArgumentParser(exit_on_error=False)
    subcommands = command_line.add_subparsers(required=True)
    subcommand = subcommands.add_parser("draw", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("--count", type=int, required=True)
    subcommand.add_argument("--seed", type=int)
    return command_line


def pick_list_text(picks):
    return "\n".join(_list_item(pick) for pick in picks)


def _list_item(pick):
    perspective_row, reference_row = pick_text(*pick).splitlines()
    return f"- {perspective_row}\n  {reference_row}"


if __name__ == "__main__":
    with reporting_failures():
        flags = parser().parse_args(sys.argv[1:])
        theme = Theme(flags.options, flags.seed)
        picker = Picker(theme)

        picks = [picker.pick() for _ in range(flags.count)]
        print(pick_list_text(picks))
