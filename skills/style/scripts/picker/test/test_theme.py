import unittest

import fixtures
from theme import (
    InvalidTheme, MissingHook, NoHookHasWeight, NoHooks, Theme, ThemeOptions,
)


class HooksTest(unittest.TestCase):
    def test_the_kinds_are_the_pools_giving_a_hook(self):
        theme = Theme(fixtures.EVEN)
        kinds = list(theme.kind_chances_for(ThemeOptions()))

        expected = ["scenes", "characters"]
        self.assertEqual(expected, kinds)

    def test_a_kinds_hooks_are_the_entries_of_its_pool(self):
        theme = Theme(fixtures.EVEN)
        hooks = list(theme.hook_chances_for(ThemeOptions(), "scenes"))

        expected = ["scenes/dawn", "scenes/noon", "scenes/dusk"]
        self.assertEqual(expected, hooks)

    def test_a_theme_whose_pools_give_no_hook_fails_with_no_hooks(self):
        theme = Theme(fixtures.SPEAKERS_ONLY)

        with self.assertRaises(NoHooks) as raised:
            theme.kind_chances_for(ThemeOptions())

        expected = "no pool in the options file gives a hook"
        self.assertEqual(expected, str(raised.exception))


class FitTest(unittest.TestCase):
    def test_an_entry_fits_only_the_reminder_types_its_when_names(self):
        theme = Theme(fixtures.EVERY_WHEN)
        theme_options = ThemeOptions.parse("weekly")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = ["scenes/any_time", "scenes/morning_or_weekly"]
        self.assertEqual(expected, hooks)

    def test_an_entry_fits_only_when_a_task_outcome_it_names_happened(self):
        theme = Theme(fixtures.EVERY_WHEN)
        theme_options = ThemeOptions.parse("evening,slipped")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = [
            "scenes/any_time", "scenes/evening", "scenes/slipped",
            "scenes/evening_slipped",
        ]
        self.assertEqual(expected, hooks)

    def test_an_entry_naming_both_kinds_needs_both(self):
        theme = Theme(fixtures.EVERY_WHEN)
        theme_options = ThemeOptions.parse("evening")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = ["scenes/any_time", "scenes/evening"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_fits_only_entries_kept_for_big_win(self):
        theme = Theme(fixtures.EVERY_WHEN)
        theme_options = ThemeOptions.parse("evening,big_win")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = ["scenes/big_win", "scenes/evening_big_win"]
        self.assertEqual(expected, hooks)

    def test_on_a_big_win_an_entry_still_fits_only_its_reminder_types(self):
        theme = Theme(fixtures.EVERY_WHEN)
        theme_options = ThemeOptions.parse("morning,done,big_win")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = ["scenes/big_win"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_nothing_kept_for_it_fits_as_a_normal_win(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        theme_options = ThemeOptions.parse("evening,big_win")
        hooks = list(theme.hook_chances_for(theme_options, "scenes"))

        expected = ["scenes/evening_done"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_no_normal_win_hook_fails_with_missing_hook(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)

        with self.assertRaises(MissingHook) as raised:
            theme.kind_chances_for(ThemeOptions.parse("morning,big_win"))

        expected = "no hook fits morning,big_win"
        self.assertEqual(expected, str(raised.exception))


class KindChanceTest(unittest.TestCase):
    def test_pools_without_a_weight_or_score_are_equally_likely(self):
        theme = Theme(fixtures.EVEN)
        chances = theme.kind_chances_for(ThemeOptions())

        expected = {"scenes": 0.5, "characters": 0.5}
        self.assertEqual(expected, chances)

    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(fixtures.WEIGHTED)
        chances = theme.kind_chances_for(ThemeOptions())

        total_draw_weight = 7 + 1
        expected = {
            "scenes": 3.5 * 2 ** 1 / total_draw_weight,
            "characters": 2 * 2 ** -1 / total_draw_weight,
        }
        self.assertEqual(expected, chances)

    def test_a_kind_whose_fitting_hooks_all_weigh_0_is_left_out(self):
        theme = Theme(fixtures.WEIGHTED)
        kinds = list(theme.kind_chances_for(ThemeOptions()))

        expected = ["scenes", "characters"]
        self.assertEqual(expected, kinds)

    def test_a_kind_with_no_hook_that_fits_is_left_out(self):
        theme = Theme(fixtures.CASEBOOK)
        chances = theme.kind_chances_for(ThemeOptions.parse("big_win"))

        expected = {"shared_lines": 1.0}
        self.assertEqual(expected, chances)

    def test_a_big_win_whose_hooks_weigh_0_fails_with_no_hook_has_weight(self):
        theme = Theme(fixtures.WEIGHTED)

        with self.assertRaises(NoHookHasWeight) as raised:
            theme.kind_chances_for(ThemeOptions.parse("big_win"))

        expected = "every hook that fits big_win weighs 0"
        self.assertEqual(expected, str(raised.exception))


class HookChanceTest(unittest.TestCase):
    def test_entries_without_a_weight_or_score_are_equally_likely(self):
        theme = Theme(fixtures.EVEN)
        chances = theme.hook_chances_for(ThemeOptions(), "scenes")

        expected = {
            "scenes/dawn": 1 / 3, "scenes/noon": 1 / 3, "scenes/dusk": 1 / 3,
        }
        self.assertEqual(expected, chances)

    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(fixtures.WEIGHTED)
        chances = theme.hook_chances_for(ThemeOptions(), "scenes")

        total_draw_weight = 0.5 + 2 + 0
        expected = {
            "scenes/dawn": 0.5 * 2 ** 0 / total_draw_weight,
            "scenes/noon": 1 * 2 ** 1 / total_draw_weight,
            "scenes/dusk": 0 * 2 ** 0 / total_draw_weight,
        }
        self.assertEqual(expected, chances)


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        theme = Theme(fixtures.CASEBOOK)
        kinds = list(theme.kind_chances_for(ThemeOptions()))

        expected = ["characters", "shared_lines", "scenes"]
        self.assertEqual(expected, kinds)

    def test_a_file_without_pools_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.WITHOUT_POOLS)

        expected = "$: 'pools' is a required property"
        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_without_roles_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.POOL_WITHOUT_ROLES)

        expected = "$.pools.scenes: 'roles' is a required property"
        self.assertEqual(expected, str(raised.exception))

    def test_a_role_that_isnt_hook_or_speaker_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_ROLE)

        why = "'hooks' is not one of ['hook', 'speaker']"
        expected = f"$.pools.scenes.roles[0]: {why}"
        self.assertEqual(expected, str(raised.exception))

    def test_a_when_that_isnt_an_option_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_WHEN)

        options = [
            "morning", "afternoon", "evening", "weekly", "slipped", "done",
            "big_win",
        ]
        where = "$.pools.scenes.entries.dawn.when"
        expected = f"{where}: 'night' is not one of {options}"
        self.assertEqual(expected, str(raised.exception))

    def test_a_negative_weight_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.NEGATIVE_WEIGHT)

        where = "$.pools.scenes.entries.dawn.weight"
        expected = f"{where}: -1 is less than the minimum of 0"
        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_weighing_0_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.WEIGHTLESS_POOL)

        where = "$.pools.scenes.weight"
        expected = f"{where}: 0 is less than or equal to the minimum of 0"
        self.assertEqual(expected, str(raised.exception))
