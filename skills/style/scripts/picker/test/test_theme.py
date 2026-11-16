import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path

import fixtures
from theme import (
    InvalidTheme, MissingHook, NoHooks, Theme, ThemeOptions, UnknownEntryFile,
)


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

        with self.assertRaises(NoHooks) as raised:
            theme.hooks_for(ThemeOptions())

        expected = "no pool in the options file gives a hook"
        self.assertEqual(expected, str(raised.exception))


class FitTest(unittest.TestCase):
    def test_an_entry_fits_only_the_reminder_types_its_type_names(self):
        theme = Theme(fixtures.EVERY_TYPE)
        hooks = theme.hooks_for(ThemeOptions.parse("weekly"))

        expected = ["scenes/any_time", "scenes/morning_or_weekly"]
        self.assertEqual(expected, hooks)

    def test_an_entry_fits_only_when_a_task_outcome_it_names_happened(self):
        theme = Theme(fixtures.EVERY_TYPE)
        hooks = theme.hooks_for(ThemeOptions.parse("evening,slipped"))

        expected = [
            "scenes/any_time", "scenes/evening", "scenes/slipped",
            "scenes/evening_slipped",
        ]
        self.assertEqual(expected, hooks)

    def test_an_entry_naming_both_kinds_needs_both(self):
        theme = Theme(fixtures.EVERY_TYPE)
        hooks = theme.hooks_for(ThemeOptions.parse("evening"))

        expected = ["scenes/any_time", "scenes/evening"]
        self.assertEqual(expected, hooks)

    def test_a_big_win_fits_only_entries_kept_for_big_win(self):
        theme = Theme(fixtures.EVERY_TYPE)
        hooks = theme.hooks_for(ThemeOptions.parse("evening,big_win"))

        expected = ["scenes/big_win", "scenes/evening_big_win"]
        self.assertEqual(expected, hooks)

    def test_on_a_big_win_an_entry_still_fits_only_its_reminder_types(self):
        theme = Theme(fixtures.EVERY_TYPE)
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

        with self.assertRaises(MissingHook) as raised:
            theme.hooks_for(ThemeOptions.parse("morning,big_win"))

        expected = "no hook fits morning,big_win"
        self.assertEqual(expected, str(raised.exception))


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        hooks = Theme(fixtures.CASEBOOK).hooks_for(ThemeOptions())

        expected = [
            "characters/detective", "shared_lines/any_time", "scenes/stakeout",
        ]
        self.assertEqual(expected, hooks)

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


class EntryFilesTest(unittest.TestCase):
    def test_the_entries_from_a_file_are_those_of_every_pool_naming_it(self):
        theme = Theme(fixtures.CASEBOOK)
        entries = theme.entries_from("Casebook-characters.yaml")

        expected = [
            "characters/detective", "shared_lines/any_time",
            "shared_lines/big_win",
        ]
        self.assertEqual(expected, entries)

    def test_a_file_no_pool_names_fails_with_unknown_entry_file(self):
        theme = Theme(fixtures.EVEN)

        with self.assertRaises(UnknownEntryFile) as raised:
            theme.entries_from("Even-scenes.yaml")

        expected = "no pool uses Even-scenes.yaml"
        self.assertEqual(expected, str(raised.exception))


class SaveTest(unittest.TestCase):
    def test_saving_writes_the_options_files_layout(self):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        options = Path(shutil.copy(fixtures.EVEN, folder))
        theme = Theme(options)
        theme.set_weight("scenes/noon", 0.5)
        theme.set_checksum("Even-scenes.yaml", "ab12")
        theme.save()
        text = options.read_text(encoding="utf-8")

        expected = textwrap.dedent("""\
            checksums:
              Even-scenes.yaml: ab12
            pools:
              scenes:
                roles: [hook]
                entries:
                  dawn:
                  noon:
                    weight: 0.5
                  dusk:
              characters:
                roles: [hook, speaker]
                entries:
                  host:
              narrators:
                roles: [speaker]
                entries:
                  chorus:
        """)
        self.assertEqual(expected, text)
