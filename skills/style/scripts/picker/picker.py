import argparse
import sys

from modes import HookMode

FAILED = "Picker FAILED: {}: {}"


class Picker:
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args

    @classmethod
    def from_args(cls, args):
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        HookMode.add_subcommand(subcommands)
        return cls(parser, args)

    def __enter__(self):
        return self

    def __exit__(self, failure_type, failure, traceback):
        # Every failure, a bug included, is one line for the skill to read.
        if isinstance(failure, Exception):
            why = " ".join(str(failure).split())
            sys.exit(FAILED.format(failure_type.__name__, why))

    def selections(self):
        # Parsed inside the with block, so Picker reports a bad flag.
        flags = self.parser.parse_args(self.args)
        mode = flags.mode.from_flags(flags)
        return mode.pick()


if __name__ == "__main__":
    args = sys.argv[1:]
    with Picker.from_args(args) as picker:
        selections = picker.selections()
        print(selections)
