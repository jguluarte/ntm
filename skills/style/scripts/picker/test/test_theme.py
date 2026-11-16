import unittest
from datetime import date

import fixtures
from theme import (
    History, InvalidTheme, MissingHook, NoHookHasWeight, NoHooks, Theme,
    ThemeOptions,
)


class HooksTest(unittest.TestCase):
    def test_the_kinds_are_the_pools_giving_a_hook(self):
        theme = Theme(fixtures.EVEN)
        kinds = [kind.name for kind in theme.kind_lottery_for(ThemeOptions())]

        expected = ["scenes", "characters"]
        self.assertEqual(expected, kinds)

    def test_a_kinds_hooks_are_the_entries_of_its_pool(self):
        theme = Theme(fixtures.EVEN)
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/dawn", "scenes/noon", "scenes/dusk"]
        self.assertEqual(expected, hooks)

    def test_a_theme_whose_pools_give_no_hook_fails_with_no_hooks(self):
        theme = Theme(fixtures.SPEAKERS_ONLY)

        with self.assertRaises(NoHooks) as raised:
            theme.kind_lottery_for(ThemeOptions())

        expected = "no pool in the options file gives a hook"
        self.assertEqual(expected, str(raised.exception))


class FitTest(unittest.TestCase):
    def test_an_entry_fits_only_the_reminder_types_its_type_names(self):
        theme = Theme(fixtures.EVERY_TYPE)
        theme_options = ThemeOptions.parse("weekly")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/any_time", "scenes/morning_or_weekly"]
        self.assertEqual(expected, hooks)

    def test_an_entry_fits_only_when_a_task_outcome_it_names_happened(self):
        theme = Theme(fixtures.EVERY_TYPE)
        theme_options = ThemeOptions.parse("evening,slipped")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = [
            "scenes/any_time", "scenes/evening", "scenes/slipped",
            "scenes/evening_slipped",
        ]
        self.assertEqual(expected, hooks)

    def test_an_entry_naming_both_kinds_needs_both(self):
        theme = Theme(fixtures.EVERY_TYPE)
        theme_options = ThemeOptions.parse("evening")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/any_time", "scenes/evening"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_fits_only_entries_kept_for_big_win(self):
        theme = Theme(fixtures.EVERY_TYPE)
        theme_options = ThemeOptions.parse("evening,big_win")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/big_win", "scenes/evening_big_win"]
        self.assertEqual(expected, hooks)

    def test_on_a_big_win_an_entry_still_fits_only_its_reminder_types(self):
        theme = Theme(fixtures.EVERY_TYPE)
        theme_options = ThemeOptions.parse("morning,done,big_win")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/big_win"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_nothing_kept_for_it_fits_as_a_normal_win(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)
        theme_options = ThemeOptions.parse("evening,big_win")
        lottery = theme.hook_lottery_for(theme_options, "scenes")
        hooks = [hook.name for hook in lottery]

        expected = ["scenes/evening_done"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_with_no_normal_win_hook_fails_with_missing_hook(self):
        theme = Theme(fixtures.WITHOUT_BIG_WIN)

        with self.assertRaises(MissingHook) as raised:
            theme.kind_lottery_for(ThemeOptions.parse("morning,big_win"))

        expected = "no hook fits morning,big_win"
        self.assertEqual(expected, str(raised.exception))


class KindChanceTest(unittest.TestCase):
    def test_pools_without_a_weight_or_score_are_equally_likely(self):
        theme = Theme(fixtures.EVEN)
        lottery = theme.kind_lottery_for(ThemeOptions())
        chance_by_name = {kind.name: chance for kind, chance in lottery.items()}

        expected = {"scenes": 0.5, "characters": 0.5}
        self.assertEqual(expected, chance_by_name)

    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(fixtures.WEIGHTED)
        lottery = theme.kind_lottery_for(ThemeOptions())
        chance_by_name = {kind.name: chance for kind, chance in lottery.items()}

        total_draw_weight = 7 + 1
        expected = {
            "scenes": 3.5 * 2 ** 1 / total_draw_weight,
            "characters": 2 * 2 ** -1 / total_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)

    def test_a_kind_whose_fitting_hooks_all_weigh_0_is_left_out(self):
        theme = Theme(fixtures.WEIGHTED)
        kinds = [kind.name for kind in theme.kind_lottery_for(ThemeOptions())]

        expected = ["scenes", "characters"]
        self.assertEqual(expected, kinds)

    def test_on_a_big_win_only_kinds_keeping_a_big_win_hook_are_drawn(self):
        theme = Theme(fixtures.CASEBOOK)
        lottery = theme.kind_lottery_for(ThemeOptions.parse("big_win"))
        chance_by_name = {kind.name: chance for kind, chance in lottery.items()}

        expected = {"shared_lines": 1.0}
        self.assertEqual(expected, chance_by_name)

    def test_a_big_win_whose_hooks_weigh_0_fails_with_no_hook_has_weight(self):
        theme = Theme(fixtures.WEIGHTED)

        with self.assertRaises(NoHookHasWeight) as raised:
            theme.kind_lottery_for(ThemeOptions.parse("big_win"))

        expected = "every hook that fits big_win weighs 0"
        self.assertEqual(expected, str(raised.exception))


class HookChanceTest(unittest.TestCase):
    def test_entries_without_a_weight_or_score_are_equally_likely(self):
        theme = Theme(fixtures.EVEN)
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes")
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        expected = {
            "scenes/dawn": 1 / 3, "scenes/noon": 1 / 3, "scenes/dusk": 1 / 3,
        }
        self.assertEqual(expected, chance_by_name)

    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(fixtures.WEIGHTED)
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes")
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        total_draw_weight = 0.5 + 2 + 0
        expected = {
            "scenes/dawn": 0.5 * 2 ** 0 / total_draw_weight,
            "scenes/noon": 1 * 2 ** 1 / total_draw_weight,
            "scenes/dusk": 0 * 2 ** 0 / total_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)


class RestTest(unittest.TestCase):
    def test_a_hook_used_one_half_life_ago_draws_at_half_its_weight(self):
        theme = Theme(fixtures.EVEN)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 15))
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes", history)
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        total_rested_draw_weight = 0.5 + 1 + 1
        expected = {
            "scenes/dawn": 0.5 / total_rested_draw_weight,
            "scenes/noon": 1 / total_rested_draw_weight,
            "scenes/dusk": 1 / total_rested_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)

    def test_a_hook_used_two_half_lives_ago_draws_at_three_quarters(self):
        theme = Theme(fixtures.EVEN)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 17))
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes", history)
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        total_rested_draw_weight = 0.75 + 1 + 1
        expected = {
            "scenes/dawn": 0.75 / total_rested_draw_weight,
            "scenes/noon": 1 / total_rested_draw_weight,
            "scenes/dusk": 1 / total_rested_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)

    def test_a_hook_used_today_has_no_chance(self):
        theme = Theme(fixtures.EVEN)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 13))
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes", history)
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        total_rested_draw_weight = 0 + 1 + 1
        expected = {
            "scenes/dawn": 0 / total_rested_draw_weight,
            "scenes/noon": 1 / total_rested_draw_weight,
            "scenes/dusk": 1 / total_rested_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)

    def test_when_every_fitting_hook_was_used_today_none_rests(self):
        theme = Theme(fixtures.EVEN)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 13))
        lottery = theme.hook_lottery_for(ThemeOptions(), "characters", history)
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        expected = {"characters/host": 1.0}
        self.assertEqual(expected, chance_by_name)

    def test_a_pool_without_a_half_life_never_rests(self):
        theme = Theme(fixtures.WEIGHTED)
        history = History(fixtures.EVEN_HISTORY, date(2026, 11, 13))
        lottery = theme.hook_lottery_for(ThemeOptions(), "scenes", history)
        chance_by_name = {hook.name: chance for hook, chance in lottery.items()}

        total_draw_weight = 0.5 + 2 + 0
        expected = {
            "scenes/dawn": 0.5 / total_draw_weight,
            "scenes/noon": 2 / total_draw_weight,
            "scenes/dusk": 0 / total_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        theme = Theme(fixtures.CASEBOOK)
        kinds = [kind.name for kind in theme.kind_lottery_for(ThemeOptions())]

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

    def test_a_type_that_isnt_an_option_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_TYPE)

        options = [
            "morning", "afternoon", "evening", "weekly", "slipped", "done",
            "big_win",
        ]
        where = "$.pools.scenes.entries.dawn.type"
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

    def test_a_half_life_of_0_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.ZERO_HALF_LIFE)

        where = "$.pools.scenes.half_life_days"
        expected = f"{where}: 0 is less than or equal to the minimum of 0"
        self.assertEqual(expected, str(raised.exception))
