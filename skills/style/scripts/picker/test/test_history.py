import unittest
from datetime import datetime

import fixtures
from theme import History


class HistoryTest(unittest.TestCase):
    def test_each_piece_counts_the_days_since_its_newest_use(self):
        history = History(fixtures.casebook.MESSAGE_HISTORY)
        now = datetime.fromisoformat("2026-11-14 08:45")

        expected = {
            "characters/detective": 0.5,
            "scenes/stakeout": 0.5,
            "shared_lines/any_time": 3.0,
        }
        self.assertEqual(expected, history.days_since_use(now))
