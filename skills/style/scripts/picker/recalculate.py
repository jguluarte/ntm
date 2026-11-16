import argparse
import contextlib
import sys

from theme import EntryFile, Theme

LINES_AT_HALF_WEIGHT = 3


class Recalculation:
    def __init__(self, theme, entry_files):
        self.theme = theme
        self.entry_files = entry_files

    @classmethod
    def from_args(cls, args):
        flags = cls._parser().parse_args(args)
        theme = Theme(flags.options)
        entry_files = [EntryFile(path) for path in flags.entry_files]
        return cls(theme, entry_files)

    def weigh_entries(self):
        for entry_file in self.entry_files:
            self._weigh_entries_from(entry_file)

    def record_checksums(self):
        for entry_file in self.entry_files:
            self.theme.set_checksum(entry_file.name, entry_file.checksum)

    def save_options_file(self):
        self.theme.save()

    def _weigh_entries_from(self, entry_file):
        line_counts = entry_file.line_counts
        for entry_name in self.theme.entries_from(entry_file.name):
            if entry_name in line_counts:
                weight = self._weight_for(line_counts[entry_name])
                self.theme.set_weight(entry_name, weight)

    @staticmethod
    def _weight_for(line_count):
        if not line_count:
            return 1.0

        return round(line_count / (line_count + LINES_AT_HALF_WEIGHT), 2)

    @staticmethod
    def _parser():
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        start = subcommands.add_parser("start", exit_on_error=False)
        start.add_argument("--options", required=True)
        start.add_argument("entry_files", nargs="+")
        return parser


@contextlib.contextmanager
def reporting_failures():
    try:
        yield
    except Exception as failure:
        why = " ".join(str(failure).split())
        sys.exit(f"Recalculation FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    with reporting_failures():
        recalculation = Recalculation.from_args(sys.argv[1:])
        recalculation.weigh_entries()
        recalculation.record_checksums()
        recalculation.save_options_file()

    print(f"saved: {recalculation.theme.path}")
