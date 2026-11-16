import tempfile
import textwrap
import unittest
from pathlib import Path

import fixtures
from theme import InvalidTheme, MissingWeight, Theme, UnknownEntryFile


class OptionsTest(unittest.TestCase):
    def test_the_options_are_every_entry_but_those_of_speaker_only_pools(self):
        theme = Theme(fixtures.EVEN)
        lottery = theme.lottery()

        expected = [
            "scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host",
        ]
        self.assertEqual(expected, lottery.names)

    def test_a_theme_with_only_speaker_pools_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.SPEAKERS_ONLY)

        expected = "$.pools: no options found"
        self.assertEqual(expected, str(raised.exception))


class ChanceTest(unittest.TestCase):
    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(fixtures.WEIGHTED)
        lottery = theme.lottery()

        total_draw_weight = 0.5 + 2 + 0 + 1.5
        expected = {
            "scenes/dawn": 0.5 * 2 ** 0 / total_draw_weight,
            "scenes/noon": 1 * 2 ** 1 / total_draw_weight,
            "scenes/dusk": 0 * 2 ** 0 / total_draw_weight,
            "characters/host": 3 * 2 ** -1 / total_draw_weight,
        }
        self.assertEqual(expected, lottery.chance_by_name)

    def test_every_option_weighing_0_fails_with_missing_weight(self):
        theme = Theme(fixtures.WEIGHTLESS)

        with self.assertRaises(MissingWeight) as raised:
            theme.lottery()

        expected = "every option weighs 0"
        self.assertEqual(expected, str(raised.exception))


class DrawTest(unittest.TestCase):
    def test_a_draw_returns_the_only_option_weighing_above_0(self):
        theme = Theme(fixtures.MOSTLY_WEIGHTLESS)
        option = theme.draw()

        expected = "scenes/dawn"
        self.assertEqual(expected, option.name)


class SchemaTest(unittest.TestCase):
    def test_the_documented_example_passes(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        lottery = theme.lottery()

        expected = [
            "characters/detective", "shared_lines/any_time", "scenes/stakeout",
        ]
        self.assertEqual(expected, lottery.names)

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

    def test_an_unknown_role_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.UNKNOWN_ROLE)

        why = "'hooks' is not one of ['hook', 'speaker']"
        expected = f"$.pools.scenes.roles[0]: {why}"
        self.assertEqual(expected, str(raised.exception))

    def test_a_negative_weight_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(fixtures.NEGATIVE_WEIGHT)

        where = "$.pools.scenes.entries.dawn.weight"
        expected = f"{where}: -1 is less than the minimum of 0"
        self.assertEqual(expected, str(raised.exception))


class EntryFilesTest(unittest.TestCase):
    def test_the_entries_from_a_file_are_those_of_every_pool_naming_it(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        entries = theme.entries_from("Casebook-characters.yaml")

        expected = ["characters/detective", "shared_lines/any_time"]
        self.assertEqual(expected, entries)

    def test_a_file_no_pool_names_fails_with_unknown_entry_file(self):
        theme = Theme(fixtures.EVEN)

        with self.assertRaises(UnknownEntryFile) as raised:
            theme.entries_from("Even-scenes.yaml")

        expected = "no pool uses Even-scenes.yaml"
        self.assertEqual(expected, str(raised.exception))


class WeightsAndChecksumsTest(unittest.TestCase):
    def test_the_weight_of_an_entry_is_the_one_its_options_file_gives(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        weight = theme.weight_of("characters/detective")

        expected = 0.57
        self.assertEqual(expected, weight)

    def test_the_checksum_of_a_file_is_the_one_its_options_file_gives(self):
        theme = Theme(fixtures.casebook.OPTIONS)
        checksum = theme.checksum_of("Casebook-characters.yaml")

        expected = "9f86d081884c7d65..."
        self.assertEqual(expected, checksum)


class SaveTest(unittest.TestCase):
    def test_saving_writes_the_options_files_layout(self):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        saved_options = Path(folder) / "Even-options.yaml"
        theme = Theme(fixtures.EVEN)
        theme.set_weight("scenes/noon", 0.5)
        theme.set_checksum("Even-scenes.yaml", "ab12")
        theme.save(saved_options)
        text = saved_options.read_text(encoding="utf-8")

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
