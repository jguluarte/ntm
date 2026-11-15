import argparse
import sys

import yaml

from exceptions import PickerFailed
from modes import MODES

PICK = "pick"
MODE = "mode"
FAILED = "Picker FAILED: {}"
FAILURES = (PickerFailed, argparse.ArgumentError, OSError, yaml.YAMLError)


class Picker:
    def __init__(self, command_line, args):
        self.command_line = command_line
        self.args = args

    @classmethod
    def from_args(cls, args):
        command_line = argparse.ArgumentParser(prog=PICK, exit_on_error=False)
        subcommands = command_line.add_subparsers(dest=MODE, required=True)
        for mode in MODES.values():
            subcommand = subcommands.add_parser(mode.NAME, exit_on_error=False)
            mode.add_flags(subcommand)
        return cls(command_line, args)

    def __enter__(self):
        return self

    def __exit__(self, kind, failure, traceback):
        if isinstance(failure, FAILURES):
            why = " ".join(str(failure).split())
            sys.exit(FAILED.format(why))

    def selections(self):
        flags = self.command_line.parse_args(self.args)
        mode = MODES[flags.mode](flags)
        return mode.selections()
