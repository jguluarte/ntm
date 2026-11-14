import unittest
from itertools import islice

from random_numbers import ParkMiller


class ParkMillerTest(unittest.TestCase):
    def test_the_generator_gives_park_millers_published_numbers(self):
        first_three = list(islice(ParkMiller(1), 3))
        self.assertEqual([48271, 182605794, 1291394886], first_three)
        # C++'s minstd_rand gives 399268537 as its 10000th number from seed 1.
        ten_thousandth = list(islice(ParkMiller(1), 10000))[-1]
        self.assertEqual(399268537, ten_thousandth)
