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
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            theme = Theme(flags.options)
            entry_files = [EntryFile(path) for path in flags.entry_files]
            return cls(theme, entry_files)

    def start(self):
        with self._reporting_failures():
            printed = [
                self._recount(entry_file) for entry_file in self.entry_files
            ]
            self.theme.save()
            return "\n".join(printed)

    def _recount(self, entry_file):
        line_counts = entry_file.line_counts
        for entry_name in self.theme.entries_from(entry_file.name):
            if entry_name in line_counts:
                weight = self._weight_for(line_counts[entry_name])
                self.theme.set_weight(entry_name, weight)

        self.theme.set_checksum(entry_file.name, entry_file.checksum)
        return f"recounted: {entry_file.name}"

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

    @staticmethod
    @contextlib.contextmanager
    def _reporting_failures():
        try:
            yield
        except Exception as failure:
            # Every failure, a bug included, is one line for the skill to read.
            why = " ".join(str(failure).split())
            sys.exit(
                f"Recalculation FAILED: { type(failure).__name__ }: {why}"
            )


if __name__ == "__main__":
    args = sys.argv[1:]

    recalculation = Recalculation.from_args(args)
    printed = recalculation.start()

    print(printed)
