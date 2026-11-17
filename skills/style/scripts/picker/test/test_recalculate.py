import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

import yaml

import fixtures
from recalculate import (
    Message, MessageHistory, Recalculation, parser, reporting_failures,
)
from theme import EntryFile, Theme, UnknownEntryFile

SEND_TIME = datetime(2026, 11, 13, 8, 45)


class RecalculationTest(unittest.TestCase):
    def test_weighing_gives_each_entry_its_weight_from_its_lines(self):
        theme = Theme(fixtures.weighing.OPTIONS)
        entry_file = EntryFile(fixtures.weighing.CHARACTERS)
        recalculation = Recalculation(theme)

        recalculation.weigh_entries([entry_file])

        self.assertEqual(0.25, theme.weight_of("characters/one_line"))
        self.assertEqual(0.5, theme.weight_of("characters/three_lines"))
        self.assertEqual(0.75, theme.weight_of("characters/nine_lines"))
        self.assertEqual(1.0, theme.weight_of("characters/no_lines"))

    def test_a_speaker_is_the_perspective_at_least_6_times_in_10(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        recalculation = Recalculation(theme)

        recalculation.work_out_speaker_rate()

        self.assertEqual(0.6, theme.speaker_rate)

    def test_speakers_with_more_of_the_weight_are_the_perspective_more(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        theme.set_weight("characters/detective", 3.0)
        recalculation = Recalculation(theme)

        recalculation.work_out_speaker_rate()

        self.assertEqual(0.75, theme.speaker_rate)

    def test_a_theme_of_only_speakers_always_has_a_speaker(self):
        theme = Theme(fixtures.SPEAKERS_ONLY)
        recalculation = Recalculation(theme)

        recalculation.work_out_speaker_rate()

        self.assertEqual(1.0, theme.speaker_rate)

    def test_a_theme_without_speakers_never_has_a_speaker(self):
        theme = Theme(fixtures.weighing.OPTIONS)
        recalculation = Recalculation(theme)

        recalculation.work_out_speaker_rate()

        self.assertEqual(0, theme.speaker_rate)

    def test_recording_gives_the_entry_file_its_own_checksum(self):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        saved_options = Path(folder) / "Weighing-options.yaml"
        theme = Theme(fixtures.weighing.OPTIONS)
        entry_file = EntryFile(fixtures.weighing.CHARACTERS)
        recalculation = Recalculation(theme)

        recalculation.record_checksums([entry_file])
        theme.save(saved_options)

        fields = yaml.safe_load(saved_options.read_text(encoding="utf-8"))
        checksum = fields["checksums"]["Weighing-characters.yaml"]
        self.assertEqual(entry_file.checksum, checksum)

    def test_an_entry_file_no_pool_uses_fails_with_unknown_entry_file(self):
        theme = Theme(fixtures.EVEN)
        characters = EntryFile(fixtures.casebook.CHARACTERS)
        scenes = EntryFile(fixtures.casebook.SCENES)
        recalculation = Recalculation(theme)

        with self.assertRaises(UnknownEntryFile) as raised:
            recalculation.weigh_entries([characters, scenes])

        expected = "no pool uses Casebook-characters.yaml"
        self.assertEqual(expected, str(raised.exception))


class ScoresTest(unittest.TestCase):
    def test_an_acted_on_message_raises_both_its_picks(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict="acted", feedback=None)
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        stakeout_score = theme.score_of("scenes/stakeout")
        self.assertAlmostEqual(0.2 + 0.1, detective_score)
        self.assertAlmostEqual(0.1 + 0.1, stakeout_score)

    def test_an_ignored_message_lowers_both_its_picks(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict="ignored", feedback=None)
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        stakeout_score = theme.score_of("scenes/stakeout")
        self.assertAlmostEqual(0.2 - 0.1, detective_score)
        self.assertAlmostEqual(0.1 - 0.1, stakeout_score)

    def test_a_message_the_user_keeps_raises_both_its_picks(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict=None, feedback="keep")
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        stakeout_score = theme.score_of("scenes/stakeout")
        self.assertAlmostEqual(0.2 + 0.25, detective_score)
        self.assertAlmostEqual(0.1 + 0.25, stakeout_score)

    def test_a_message_the_user_calls_stale_lowers_both_its_picks(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict=None, feedback="stale")
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        stakeout_score = theme.score_of("scenes/stakeout")
        self.assertAlmostEqual(0.2 - 0.5, detective_score)
        self.assertAlmostEqual(0.1 - 0.5, stakeout_score)

    def test_a_message_with_no_verdict_or_feedback_moves_nothing(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict=None, feedback=None)
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        stakeout_score = theme.score_of("scenes/stakeout")
        self.assertEqual(0.2, detective_score)
        self.assertEqual(0.1, stakeout_score)

    def test_a_pick_the_options_file_no_longer_has_is_skipped(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/fog")
        message = Message(SEND_TIME, picks, verdict="acted", feedback=None)
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message])

        detective_score = theme.score_of("characters/detective")
        self.assertAlmostEqual(0.2 + 0.1, detective_score)
        self.assertFalse(theme.has_entry("scenes/fog"))

    def test_a_score_rises_no_higher_than_1(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict="acted", feedback="keep")
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message] * 4)

        self.assertEqual(1, theme.score_of("characters/detective"))

    def test_a_score_sinks_no_lower_than_minus_2(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        picks = ("characters/detective", "scenes/stakeout")
        message = Message(SEND_TIME, picks, verdict="ignored", feedback="stale")
        recalculation = Recalculation(theme)

        recalculation.adjust_scores([message] * 4)

        self.assertEqual(-2, theme.score_of("scenes/stakeout"))

    def test_a_reference_called_stale_all_week_sinks_to_the_lowest_score(self):
        theme = Theme(fixtures.scoring.OPTIONS)
        history = MessageHistory(fixtures.scoring.MESSAGE_HISTORY)
        messages = history.sent_since(date(2026, 11, 9))
        recalculation = Recalculation(theme)

        recalculation.adjust_scores(messages)

        self.assertEqual(-2, theme.score_of("clues/badge"))

    def test_a_score_that_reached_the_highest_falls_with_a_later_message(self):
        theme = Theme(fixtures.scoring.OPTIONS)
        history = MessageHistory(fixtures.scoring.MESSAGE_HISTORY)
        messages = history.sent_since(date(2026, 11, 9))
        recalculation = Recalculation(theme)

        recalculation.adjust_scores(messages)

        self.assertAlmostEqual(1 - 0.1, theme.score_of("cast/chief"))


class MessageHistoryTest(unittest.TestCase):
    def test_the_messages_since_a_day_are_those_sent_on_or_after_it(self):
        history = MessageHistory(fixtures.scoring.MESSAGE_HISTORY)
        messages = history.sent_since(date(2026, 11, 15))

        sent = datetime(2026, 11, 15, 18, 0)
        picks = ("cast/chief", "scenes/fog")
        expected = [Message(sent, picks, verdict="ignored", feedback=None)]
        self.assertEqual(expected, messages)


class ReportingFailuresTest(unittest.TestCase):
    def test_a_failure_exits_with_one_line_naming_it(self):
        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                raise UnknownEntryFile("Casebook-characters.yaml")

        why = "no pool uses Casebook-characters.yaml"
        expected = f"Recalculation FAILED: UnknownEntryFile: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_start_without_entry_files_fails_naming_them(self):
        args = ["start", "--options", str(fixtures.casebook.OPTIONS)]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "the following arguments are required: entry_files"
        expected = f"Recalculation FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)

    def test_adjust_without_since_fails_naming_it(self):
        args = [
            "adjust",
            "--options", str(fixtures.scoring.OPTIONS),
            "--history", str(fixtures.scoring.MESSAGE_HISTORY),
        ]

        with self.assertRaises(SystemExit) as exited:
            with reporting_failures():
                parser().parse_args(args)

        why = "the following arguments are required: --since"
        expected = f"Recalculation FAILED: ArgumentError: {why}"
        self.assertEqual(expected, exited.exception.code)
