import argparse

from failure import PickerFailed


class CommandLine(argparse.ArgumentParser):
    @classmethod
    def for_modes(cls, modes):
        command_line = cls(prog="pick")
        subcommands = command_line.add_subparsers(dest="mode", required=True)
        for mode in modes:
            mode.add_flags(subcommands.add_parser(mode.NAME))
        return command_line

    def error(self, message):
        raise PickerFailed(message)
