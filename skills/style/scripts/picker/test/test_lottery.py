import unittest

from theme import Lottery


class LotteryTest(unittest.TestCase):
    def test_a_chance_is_the_draw_weight_over_the_total(self):
        lottery = Lottery({"heads": 1, "tails": 3})

        expected = {"heads": 0.25, "tails": 0.75}
        self.assertEqual(expected, lottery.chance_by_candidate)

    def test_the_same_seed_draws_the_same_candidates(self):
        lottery = Lottery({"heads": 1, "tails": 3})

        Lottery.set_seed(3)
        first = [lottery.draw() for _ in range(4)]
        Lottery.set_seed(3)
        second = [lottery.draw() for _ in range(4)]

        self.assertEqual(first, second)
