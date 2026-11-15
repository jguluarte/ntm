import unittest

import yaml

from theme import (
    OPTIONS_SCHEMA, MoreThanOneReminderType, ReminderType, TaskOutcome,
    ThemeOptions, UnknownOption,
)


class ParseTest(unittest.TestCase):
    def test_a_reminder_type_and_task_outcomes_parse_into_one_combination(self):
        theme_options = ThemeOptions.parse("evening,slipped,big_win")

        task_outcomes = frozenset({TaskOutcome.SLIPPED, TaskOutcome.BIG_WIN})
        expected = ThemeOptions(ReminderType.EVENING, task_outcomes)

        self.assertEqual(expected, theme_options)

    def test_a_value_that_isnt_an_option_fails_with_unknown_option(self):
        with self.assertRaises(UnknownOption) as raised:
            ThemeOptions.parse("evening,night")

        expected = "not an option: night"
        self.assertEqual(expected, str(raised.exception))

    def test_two_reminder_types_fail_with_more_than_one_reminder_type(self):
        with self.assertRaises(MoreThanOneReminderType) as raised:
            ThemeOptions.parse("morning,evening")

        expected = "more than one reminder type: evening, morning"
        self.assertEqual(expected, str(raised.exception))

    def test_the_options_are_the_ones_the_schema_lists_for_type(self):
        schema = yaml.safe_load(OPTIONS_SCHEMA.read_text(encoding="utf-8"))
        options = {option.value for option in [*ReminderType, *TaskOutcome]}

        expected = set(schema["$defs"]["reminder_type_or_task_outcome"]["enum"])
        self.assertEqual(expected, options)
