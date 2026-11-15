import argparse
import sys

from modes import MODES

PICK = "pick"
FAILED = "Picker FAILED: {}: {}"


class Picker:
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args

    @classmethod
    def from_args(cls, args):
        parser = argparse.ArgumentParser(prog=PICK, exit_on_error=False)
        subcommands = parser.add_subparsers(dest="mode", required=True)
        for mode in MODES.values():
            subcommand = subcommands.add_parser(mode.NAME, exit_on_error=False)
            mode.add_flags(subcommand)
        return cls(parser, args)

    def __enter__(self):
        return self

    def __exit__(self, kind, failure, traceback):
        if isinstance(failure, Exception):
            why = " ".join(str(failure).split())
            sys.exit(FAILED.format(kind.__name__, why))

    def selections(self):
        # Parsed inside the with block, so Picker reports a bad flag.
        flags = self.parser.parse_args(self.args)
        mode = MODES[flags.mode](flags)
        return mode.selections()
