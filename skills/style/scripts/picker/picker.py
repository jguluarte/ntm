import argparse
import sys

from modes import HookMode

FAILED = "Picker FAILED: {}: {}"


class FailureLine:
    def __enter__(self):
        return self

    def __exit__(self, failure_type, failure, traceback):
        # Every failure, a bug included, is one line for the skill to read.
        if isinstance(failure, Exception):
            why = " ".join(str(failure).split())
            sys.exit(FAILED.format(failure_type.__name__, why))


class Picker:
    def __init__(self, mode):
        self.mode = mode

    @classmethod
    def from_args(cls, args):
        with FailureLine():
            flags = cls.parser().parse_args(args)
            return cls(flags.mode.from_flags(flags))

    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        HookMode.add_subcommand(subcommands)
        return parser

    def pick(self):
        with FailureLine():
            return self.mode.pick()


if __name__ == "__main__":
    args = sys.argv[1:]
    picker = Picker.from_args(args)
    selections = picker.pick()
    print(selections)
