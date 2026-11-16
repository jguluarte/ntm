import unittest

from theme import Lottery


class LotteryTest(unittest.TestCase):
    def test_a_chance_is_the_draw_weight_over_the_total(self):
        lottery = Lottery({"heads": 1, "tails": 3})

        expected = {"heads": 0.25, "tails": 0.75}
        self.assertEqual(expected, lottery.chance_by_candidate)

    def test_the_same_seed_draws_the_same_candidates(self):
        weights = range(1, 11)
        draw_weights = {f"candidate {weight}": weight for weight in weights}
        runs = 100

        first_lottery = Lottery(draw_weights, seed=3)
        first = [first_lottery.draw() for _ in range(runs)]

        second_lottery = Lottery(draw_weights, seed=3)
        second = [second_lottery.draw() for _ in range(runs)]

        self.assertEqual(first, second)
