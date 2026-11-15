import unittest

import fixtures
from theme import InvalidTheme, MissingHook, NoHooks, Theme, ThemeOptions


def hooks_fitting(options, text):
    return Theme(options).hooks_for(ThemeOptions.parse(text))


class HooksTest(unittest.TestCase):
    def test_the_hooks_are_the_entries_of_pools_giving_a_hook(self):
        theme = Theme(fixtures.EVEN)
        hooks = theme.hooks_for(ThemeOptions())

        expected = [
            "scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host",
        ]
        self.assertEqual(expected, hooks)

    def test_a_theme_whose_pools_give_no_hook_fails_with_no_hooks(self):
        theme = Theme(fixtures.SPEAKERS_ONLY)

        expected = "no pool in the options file gives a hook"
        with self.assertRaises(NoHooks) as raised:
            theme.hooks_for(ThemeOptions())
        self.assertEqual(expected, str(raised.exception))


class FitTest(unittest.TestCase):
    def test_an_entry_fits_only_the_reminder_types_its_when_names(self):
        theme = Theme(fixtures.EVERY_WHEN)
        hooks = theme.hooks_for(ThemeOptions.parse("weekly"))

        expected = ["scenes/any_time", "scenes/morning_or_weekly"]
        self.assertEqual(expected, hooks)

    def test_an_entry_fits_only_when_a_task_outcome_it_names_happened(self):
        theme = Theme(fixtures.EVERY_WHEN)
        hooks = theme.hooks_for(ThemeOptions.parse("evening,slipped"))

        expected = [
            "scenes/any_time", "scenes/evening", "scenes/slipped",
            "scenes/evening_slipped",
        ]
        self.assertEqual(expected, hooks)

    def test_an_entry_naming_both_kinds_needs_both(self):
        theme = Theme(fixtures.EVERY_WHEN)
        hooks = theme.hooks_for(ThemeOptions.parse("evening"))

        expected = ["scenes/any_time", "scenes/evening"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_fits_only_entries_kept_for_big_win(self):
        theme = Theme(fixtures.EVERY_WHEN)
        hooks = theme.hooks_for(ThemeOptions.parse("evening,big_win"))

        expected = ["scenes/big_win", "scenes/evening_big_win"]
        self.assertEqual(expected, hooks)

    def test_on_a_big_win_an_entry_still_fits_only_its_reminder_types(self):
        theme = Theme(fixtures.EVERY_WHEN)
        hooks = theme.hooks_for(ThemeOptions.parse("morning,done,big_win"))

        expected = ["scenes/big_win"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_nothing_kept_for_it_fits_as_a_normal_win(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        hooks = theme.hooks_for(ThemeOptions.parse("evening,big_win"))

        expected = ["scenes/evening_done"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_no_normal_win_hook_fails_with_missing_hook(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)

        expected = "no hook fits morning,big_win"
        with self.assertRaises(MissingHook) as raised:
            theme.hooks_for(ThemeOptions.parse("morning,big_win"))
        self.assertEqual(expected, str(raised.exception))


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        hooks = Theme(fixtures.CASEBOOK).hooks_for(ThemeOptions())

        expected = [
            "characters/detective", "shared_lines/any_time", "scenes/stakeout",
        ]
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

    def test_a_when_that_isnt_an_option_fails(self):
        options = [
            "morning", "afternoon", "evening", "weekly", "slipped", "done",
            "big_win",
        ]
        where = "$.pools.scenes.entries.dawn.when"
        expected = f"{where}: 'night' is not one of {options}"
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_WHEN)
        self.assertEqual(expected, str(raised.exception))


class CompleteThemesTest(unittest.TestCase):
    def test_each_complete_theme_offers_the_hooks_that_fit_a_message(self):
        messages = [
            (fixtures.CASEBOOK, "morning,slipped"),
            (fixtures.CASEBOOK, "evening,big_win"),
            (fixtures.ORCHARD, "evening,slipped"),
            (fixtures.ORCHARD, "morning,big_win"),
        ]
        hooks = {
            f"{options.parent.name}: {text}": hooks_fitting(options, text)
            for options, text in messages
        }

        expected = {
            "Casebook: morning,slipped": [
                "characters/detective", "shared_lines/any_time",
                "scenes/stakeout",
            ],
            "Casebook: evening,big_win": ["shared_lines/big_win"],
            "Orchard: evening,slipped": [
                "growers/elder", "growers/twins", "growers/beekeeper",
                "growers/scarecrow",
            ],
            "Orchard: morning,big_win": [
                "growers/elder", "growers/twins", "growers/beekeeper",
                "growers/scarecrow",
            ],
        }
        self.assertEqual(expected, hooks)
