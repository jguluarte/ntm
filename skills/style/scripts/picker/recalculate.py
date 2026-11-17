import argparse
import contextlib
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from theme import PERSPECTIVE_ROLE, SPEAKER_ROLE, EntryFile, Theme

LINES_AT_HALF_WEIGHT = 3
LEAST_SPEAKER_RATE = 0.6
SCORE_CHANGE_BY_VERDICT = {"acted": 0.1, "ignored": -0.1}
SCORE_CHANGE_BY_FEEDBACK = {"keep": 0.25, "stale": -0.5}
LOWEST_SCORE = -2
HIGHEST_SCORE = 1

SENT = "sent"
PICKS = "picks"
VERDICT = "verdict"
FEEDBACK = "feedback"


class Recalculation:
    def __init__(self, theme):
        self.theme = theme

    def weigh_entries(self, entry_files):
        for entry_file in entry_files:
            self._weigh_entries_from(entry_file)

    def work_out_speaker_rate(self):
        speakers = self._total_weight_of(SPEAKER_ROLE)
        other_perspectives = self._total_weight_of(PERSPECTIVE_ROLE)
        speaker_rate = self._speaker_rate_for(speakers, other_perspectives)
        self.theme.set_speaker_rate(speaker_rate)

    def record_checksums(self, entry_files):
        for entry_file in entry_files:
            self.theme.set_checksum(entry_file.name, entry_file.checksum)

    def adjust_scores(self, messages):
        for message in messages:
            self._adjust_scores_from(message)

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

    def _adjust_scores_from(self, message):
        score_change = self._score_change_for(message)
        for entry_name in message.picks:
            if self.theme.has_entry(entry_name):
                score = self.theme.score_of(entry_name) + score_change
                self.theme.set_score(entry_name, self._bounded(score))

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

    @staticmethod
    def _score_change_for(message):
        verdict_change = SCORE_CHANGE_BY_VERDICT.get(message.verdict, 0)
        feedback_change = SCORE_CHANGE_BY_FEEDBACK.get(message.feedback, 0)
        return verdict_change + feedback_change

    @staticmethod
    def _bounded(score):
        bounded_score = min(max(score, LOWEST_SCORE), HIGHEST_SCORE)
        return round(bounded_score, 2)


@dataclass(frozen=True)
class Message:
    sent: datetime
    picks: tuple
    verdict: str | None
    feedback: str | None

    @classmethod
    def from_line(cls, line):
        fields = json.loads(line)
        sent = datetime.fromisoformat(fields[SENT])
        picks = tuple(fields[PICKS].values())
        return cls(sent, picks, fields.get(VERDICT), fields.get(FEEDBACK))


class MessageHistory:
    def __init__(self, path):
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        messages = [Message.from_line(line) for line in lines if line]
        self._messages = sorted(messages, key=lambda message: message.sent)

    def sent_since(self, day):
        return [
            message for message in self._messages if message.sent.date() >= day
        ]


def parser():
    command_line = argparse.ArgumentParser(exit_on_error=False)
    subcommands = command_line.add_subparsers(dest="command", required=True)
    subcommand = subcommands.add_parser("start", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("entry_files", nargs="+")

    subcommand = subcommands.add_parser("adjust", exit_on_error=False)
    subcommand.add_argument("--options", required=True)
    subcommand.add_argument("--history", required=True)
    subcommand.add_argument("--since", type=date.fromisoformat, required=True)
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
        recalculation = Recalculation(theme)

        if flags.command == "start":
            entry_files = [EntryFile(path) for path in flags.entry_files]

            recalculation.weigh_entries(entry_files)
            recalculation.work_out_speaker_rate()
            recalculation.record_checksums(entry_files)

        else:
            history = MessageHistory(flags.history)
            messages = history.sent_since(flags.since)

            recalculation.adjust_scores(messages)

        recalculation.save_options_file()
        print(f"saved: {theme.path}")
