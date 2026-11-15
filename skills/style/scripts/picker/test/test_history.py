import unittest
from datetime import date

import fixtures
from theme import History, InvalidHistory


class HistoryTest(unittest.TestCase):
    def test_a_hooks_days_since_used_count_from_its_latest_message(self):
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        days = history.days_since_used("scenes/dawn")

        expected = 2
        self.assertEqual(expected, days)

    def test_a_hook_used_by_a_message_sent_today_was_used_0_days_ago(self):
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 13))
        days = history.days_since_used("characters/host")

        expected = 0
        self.assertEqual(expected, days)

    def test_a_hook_no_message_used_has_no_days_since_used(self):
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        days = history.days_since_used("scenes/noon")

        self.assertIsNone(days)

    def test_an_entry_without_picks_uses_nothing(self):
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        days = history.days_since_used("launch")

        self.assertIsNone(days)

    def test_without_a_file_no_message_was_sent(self):
        history = History()
        days = history.days_since_used("scenes/dawn")

        self.assertIsNone(days)

    def test_a_line_that_isnt_an_entry_fails_with_invalid_history(self):
        with self.assertRaises(InvalidHistory) as raised:
            History(fixtures.UNREADABLE_SENT_HISTORY, date(2026, 11, 15))

        line = '{"sent":"13 Nov","picks":{"hook":"scenes/dawn"}}'
        expected = f"line 2: not an entry with a sent date and time: {line}"
        self.assertEqual(expected, str(raised.exception))
