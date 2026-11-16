import unittest

from theme import Lottery


class LotteryTest(unittest.TestCase):
    def test_a_chance_is_the_draw_weight_over_the_total(self):
        lottery = Lottery({"heads": 1, "tails": 3})

        expected = {"heads": 0.25, "tails": 0.75}
        self.assertEqual(expected, lottery.chance_by_candidate)

    def test_the_same_seed_draws_the_same_candidates(self):
        first_lottery = Lottery({"heads": 1, "tails": 3}, seed=3)
        first = [first_lottery.draw() for _ in range(4)]
        second_lottery = Lottery({"heads": 1, "tails": 3}, seed=3)
        second = [second_lottery.draw() for _ in range(4)]

        self.assertEqual(first, second)
