import unittest

import fixtures
from theme import InvalidTheme, Theme


class HooksTest(unittest.TestCase):
    def test_the_hooks_are_the_entries_of_pools_giving_a_hook(self):
        theme = Theme(fixtures.EVEN)

        expected = [
            "scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host",
        ]

        hooks = theme.hooks()

        self.assertEqual(expected, hooks)


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        expected = [
            "characters/detective", "shared_lines/any_time",
            "shared_lines/big_win", "scenes/stakeout",
        ]

        hooks = Theme(fixtures.CASEBOOK).hooks()

        self.assertEqual(expected, hooks)

    def test_a_file_without_pools_fails(self):
        expected = "$: 'pools' is a required property"

        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.WITHOUT_POOLS)

        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_without_roles_fails(self):
        expected = "$.pools.scenes: 'roles' is a required property"

        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.POOL_WITHOUT_ROLES)

        self.assertEqual(expected, str(raised.exception))

    def test_a_role_that_isnt_hook_or_speaker_fails(self):
        why = "'hooks' is not one of ['hook', 'speaker']"
        expected = f"$.pools.scenes.roles[0]: {why}"

        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_ROLE)

        self.assertEqual(expected, str(raised.exception))

    def test_a_when_that_isnt_an_occasion_fails(self):
        occasions = [
            "morning", "afternoon", "evening", "weekly", "slipped", "done",
            "big_win",
        ]
        where = "$.pools.scenes.entries.dawn.when"
        expected = f"{where}: 'night' is not one of {occasions}"

        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_WHEN)

        self.assertEqual(expected, str(raised.exception))
