import unittest

import yaml

from theme import (
    OPTIONS_SCHEMA, MoreThanOneReminderType, ReminderType, TaskOutcome,
    ThemeOptions, UnknownThemeOption,
)


class ParseTest(unittest.TestCase):
    def test_a_reminder_type_and_task_outcomes_parse_into_one_combination(self):
        task_outcomes = frozenset({TaskOutcome.SLIPPED, TaskOutcome.BIG_WIN})
        expected = ThemeOptions(ReminderType.EVENING, task_outcomes)

        theme_options = ThemeOptions.parse("evening,slipped,big_win")

        self.assertEqual(expected, theme_options)

    def test_a_value_that_isnt_an_option_fails_with_unknown_theme_option(self):
        expected = "not an option: night"

        with self.assertRaises(UnknownThemeOption) as raised:
            ThemeOptions.parse("evening,night")

        self.assertEqual(expected, str(raised.exception))

    def test_two_reminder_types_fail_with_more_than_one_reminder_type(self):
        expected = "more than one reminder type: evening, morning"

        with self.assertRaises(MoreThanOneReminderType) as raised:
            ThemeOptions.parse("morning,evening")

        self.assertEqual(expected, str(raised.exception))

    def test_the_options_are_the_ones_the_schema_lists_for_when(self):
        schema = yaml.safe_load(OPTIONS_SCHEMA.read_text(encoding="utf-8"))

        expected = set(schema["$defs"]["occasion"]["enum"])

        options = {option.value for option in [*ReminderType, *TaskOutcome]}

        self.assertEqual(expected, options)


class NormalWinTest(unittest.TestCase):
    def test_a_big_win_as_a_normal_win_has_done_in_place_of_big_win(self):
        expected = ThemeOptions.parse("evening,slipped,done")

        theme_options = ThemeOptions.parse("evening,slipped,big_win")

        self.assertEqual(expected, theme_options.as_normal_win())
