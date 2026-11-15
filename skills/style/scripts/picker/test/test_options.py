import unittest

from fixtures import EVEN, POOL_WITHOUT_GIVES, WITHOUT_POOLS
from picker import Options


class HooksTest(unittest.TestCase):
    def test_the_hooks_are_the_entries_of_pools_giving_a_hook(self):
        options = Options(EVEN)
        expected = [
            "scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host",
        ]

        hooks = options.hooks()

        self.assertEqual(expected, hooks)


class SchemaTest(unittest.TestCase):
    def test_a_file_without_pools_fails(self):
        expected = "$: 'pools' is a required property"

        with self.assertRaises(ValueError) as raised:
            Options(WITHOUT_POOLS)

        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_without_gives_fails(self):
        expected = "$.pools.scenes: 'gives' is a required property"

        with self.assertRaises(ValueError) as raised:
            Options(POOL_WITHOUT_GIVES)

        self.assertEqual(expected, str(raised.exception))
