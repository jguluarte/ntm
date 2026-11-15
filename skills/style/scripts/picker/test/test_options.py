import unittest

import yaml

import fixtures
from picker import (
    HAPPENINGS, OPTIONS_SCHEMA, REMINDERS, InvalidOptions, Options,
)


class HooksTest(unittest.TestCase):
    def test_the_hooks_are_the_entries_of_pools_giving_a_hook(self):
        options = Options(fixtures.EVEN)

        expected = [
            "scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host",
        ]

        hooks = options.hooks(set())

        self.assertEqual(expected, hooks)


class FitTest(unittest.TestCase):
    def test_an_entry_fits_only_the_reminders_its_when_names(self):
        options = Options(fixtures.EVERY_WHEN)

        expected = ["scenes/any_time", "scenes/morning_or_weekly"]

        hooks = options.hooks({"weekly"})

        self.assertEqual(expected, hooks)

    def test_an_entry_fits_only_when_a_thing_it_names_happened(self):
        options = Options(fixtures.EVERY_WHEN)

        expected = [
            "scenes/any_time", "scenes/evening", "scenes/slipped",
            "scenes/evening_slipped",
        ]

        hooks = options.hooks({"evening", "slipped"})

        self.assertEqual(expected, hooks)

    def test_an_entry_naming_both_kinds_needs_both(self):
        options = Options(fixtures.EVERY_WHEN)

        expected = ["scenes/any_time", "scenes/evening"]

        hooks = options.hooks({"evening"})

        self.assertEqual(expected, hooks)

    def test_a_big_win_fits_only_entries_kept_for_big_win(self):
        options = Options(fixtures.EVERY_WHEN)

        expected = ["scenes/big_win", "scenes/evening_big_win"]

        hooks = options.hooks({"evening", "big_win"})

        self.assertEqual(expected, hooks)

    def test_on_a_big_win_an_entry_still_fits_only_its_reminders(self):
        options = Options(fixtures.EVERY_WHEN)

        expected = ["scenes/big_win"]

        hooks = options.hooks({"morning", "done", "big_win"})

        self.assertEqual(expected, hooks)


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        expected = [
            "characters/detective", "shared_lines/any_time", "scenes/stakeout",
        ]

        hooks = Options(fixtures.CASEBOOK).hooks(set())

        self.assertEqual(expected, hooks)

    def test_the_picker_and_the_schema_list_the_same_occasions(self):
        schema = yaml.safe_load(OPTIONS_SCHEMA.read_text(encoding="utf-8"))

        expected = set(schema["$defs"]["occasion"]["enum"])

        occasions = REMINDERS | HAPPENINGS

        self.assertEqual(expected, occasions)

    def test_a_file_without_pools_fails(self):
        expected = "$: 'pools' is a required property"

        with self.assertRaises(InvalidOptions) as raised:
            Options(fixtures.WITHOUT_POOLS)

        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_without_roles_fails(self):
        expected = "$.pools.scenes: 'roles' is a required property"

        with self.assertRaises(InvalidOptions) as raised:
            Options(fixtures.POOL_WITHOUT_ROLES)

        self.assertEqual(expected, str(raised.exception))

    def test_a_role_that_isnt_hook_or_speaker_fails(self):
        why = "'hooks' is not one of ['hook', 'speaker']"
        expected = f"$.pools.scenes.roles[0]: {why}"

        with self.assertRaises(InvalidOptions) as raised:
            Options(fixtures.UNKNOWN_ROLE)

        self.assertEqual(expected, str(raised.exception))

    def test_a_when_that_isnt_an_occasion_fails(self):
        occasions = [
            "morning", "afternoon", "evening", "weekly", "slipped", "done",
            "big_win",
        ]
        where = "$.pools.scenes.entries.dawn.when"
        expected = f"{where}: 'night' is not one of {occasions}"

        with self.assertRaises(InvalidOptions) as raised:
            Options(fixtures.UNKNOWN_WHEN)

        self.assertEqual(expected, str(raised.exception))
