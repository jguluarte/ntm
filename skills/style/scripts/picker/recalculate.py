import argparse
import contextlib
import sys

from theme import PERSPECTIVE_ROLE, SPEAKER_ROLE, EntryFile, Theme

LINES_AT_HALF_WEIGHT = 3
LEAST_SPEAKER_RATE = 0.6


class Recalculation:
    def __init__(self, theme, entry_files):
        self.theme = theme
        self.entry_files = entry_files

    def weigh_entries(self):
        for entry_file in self.entry_files:
            self._weigh_entries_from(entry_file)

    def work_out_speaker_rate(self):
        speakers = self._total_weight_of(SPEAKER_ROLE)
        other_perspectives = self._total_weight_of(PERSPECTIVE_ROLE)
        speaker_rate = self._speaker_rate_for(speakers, other_perspectives)
        self.theme.set_speaker_rate(speaker_rate)

    def record_checksums(self):
        for entry_file in self.entry_files:
            self.theme.set_checksum(entry_file.name, entry_file.checksum)

    def save_options_file(self):
        self.theme.save(self.theme.path)

    def _weigh_entries_from(self, entry_file):
        line_counts = entry_file.line_counts
        for entry_name in self.theme.entries_from(entry_file.name):
            if entry_name in line_counts:
                weight = self._weight_for(line_counts[entry_name])
                self.theme.set_weight(entry_name, weight)

    def _total_weight_of(self, role):
        entry_names = self.theme.entries_with_role(role)
        return sum(self.theme.weight_of(name) for name in entry_names)

    @staticmethod
    def _weight_for(line_count):
        if not line_count:
            return 1.0

        return round(line_count / (line_count + LINES_AT_HALF_WEIGHT), 2)

    @staticmethod
    def _speaker_rate_for(speakers, other_perspectives):
        if not speakers:
            return 0

        share = speakers / (speakers + other_perspectives)
        return round(max(share, LEAST_SPEAKER_RATE), 2)


def parser():
    command_line = argparse.ArgumentParser(exit_on_error=False)
    subcommands = command_line.add_subparsers(required=True)
    subcommand = subcommands.add_parser("start", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("entry_files", nargs="+")
    return command_line


@contextlib.contextmanager
def reporting_failures():
    try:
        yield
    except Exception as failure:
        why = " ".join(str(failure).split())
        sys.exit(f"Recalculation FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    with reporting_failures():
        flags = parser().parse_args(sys.argv[1:])
        theme = Theme(flags.options)
        entry_files = [EntryFile(path) for path in flags.entry_files]
        recalculation = Recalculation(theme, entry_files)

        recalculation.weigh_entries()
        recalculation.work_out_speaker_rate()
        recalculation.record_checksums()
        recalculation.save_options_file()
        print(f"saved: {theme.path}")
