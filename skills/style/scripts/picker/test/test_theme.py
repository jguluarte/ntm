import tempfile
import textwrap
import unittest
from pathlib import Path

from fixtures import baker_street, casebook, invalid_casebook
from theme import (
    InvalidTheme, MissingReference, MissingWeight, Theme, UnknownEntryFile,
)


class PerspectiveTest(unittest.TestCase):
    def test_the_perspective_is_a_speaker_at_the_speaker_rate(self):
        theme = Theme(baker_street.OPTIONS)
        lottery = theme.perspective_lottery()
        chances = lottery.chance_by_candidate.items()
        chance_by_name = {option.name: chance for option, chance in chances}

        self.assertAlmostEqual(0.4, chance_by_name["characters/detective"])
        self.assertAlmostEqual(0.6, chance_by_name["scenes/stakeout"])

    def test_the_speaker_rate_is_the_one_its_options_file_gives(self):
        theme = Theme(baker_street.OPTIONS)
        speaker_rate = theme.speaker_rate

        expected = 0.4
        self.assertEqual(expected, speaker_rate)


class ReferenceTest(unittest.TestCase):
    def test_a_reference_comes_from_outside_the_perspectives_pool(self):
        theme = Theme(baker_street.OPTIONS)
        lottery = theme.reference_lottery_outside("scenes")
        names = [option.name for option in lottery.chance_by_candidate]

        expected = ["shared_lines/any_time"]
        self.assertEqual(expected, names)

    def test_a_speakers_reference_comes_from_every_reference_pool(self):
        theme = Theme(baker_street.OPTIONS)
        lottery = theme.reference_lottery_outside("characters")
        names = [option.name for option in lottery.chance_by_candidate]

        expected = ["shared_lines/any_time", "scenes/stakeout"]
        self.assertEqual(expected, names)

    def test_a_theme_of_only_speakers_fails_with_missing_reference(self):
        theme = Theme(casebook.SPEAKERS_ONLY)

        with self.assertRaises(MissingReference) as raised:
            theme.reference_lottery_outside("narrators")

        expected = "no reference outside narrators"
        self.assertEqual(expected, str(raised.exception))


class ChanceTest(unittest.TestCase):
    def test_a_chance_is_the_weight_times_2_to_the_score_over_the_total(self):
        theme = Theme(casebook.WEIGHTED)
        lottery = theme.perspective_lottery()
        chances = lottery.chance_by_candidate.items()
        chance_by_name = {option.name: chance for option, chance in chances}

        total_draw_weight = 0.5 + 2 + 0 + 1.5
        expected = {
            "scenes/dawn": 0.5 * 2 ** 0 / total_draw_weight,
            "scenes/noon": 1 * 2 ** 1 / total_draw_weight,
            "scenes/dusk": 0 * 2 ** 0 / total_draw_weight,
            "characters/host": 3 * 2 ** -1 / total_draw_weight,
        }
        self.assertEqual(expected, chance_by_name)

    def test_every_option_weighing_0_fails_with_missing_weight(self):
        theme = Theme(casebook.WEIGHTLESS)

        with self.assertRaises(MissingWeight) as raised:
            theme.perspective_lottery()

        expected = "every option weighs 0"
        self.assertEqual(expected, str(raised.exception))


class DrawTest(unittest.TestCase):
    def test_a_draw_returns_the_only_option_weighing_above_0(self):
        theme = Theme(casebook.MOSTLY_WEIGHTLESS)
        option = theme.draw_perspective()

        expected = "scenes/dawn"
        self.assertEqual(expected, option.name)


class SchemaTest(unittest.TestCase):
    def test_a_file_with_every_field_passes(self):
        theme = Theme(baker_street.OPTIONS)
        lottery = theme.perspective_lottery()
        names = [option.name for option in lottery.chance_by_candidate]

        expected = ["characters/detective", "scenes/stakeout"]
        self.assertEqual(expected, names)

    def test_a_file_without_pools_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(invalid_casebook.WITHOUT_POOLS)

        expected = "$: 'pools' is a required property"
        self.assertEqual(expected, str(raised.exception))

    def test_a_pool_without_roles_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(invalid_casebook.POOL_WITHOUT_ROLES)

        expected = "$.pools.scenes: 'roles' is a required property"
        self.assertEqual(expected, str(raised.exception))

    def test_an_unknown_role_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(invalid_casebook.UNKNOWN_ROLE)

        roles = "['perspective', 'reference', 'speaker']"
        why = f"'perspectives' is not one of {roles}"
        expected = f"$.pools.scenes.roles[0]: {why}"
        self.assertEqual(expected, str(raised.exception))

    def test_a_negative_weight_fails(self):
        with self.assertRaises(InvalidTheme) as raised:
            Theme(invalid_casebook.NEGATIVE_WEIGHT)

        where = "$.pools.scenes.entries.dawn.weight"
        expected = f"{where}: -1 is less than the minimum of 0"
        self.assertEqual(expected, str(raised.exception))


class EntryFilesTest(unittest.TestCase):
    def test_the_entries_from_a_file_are_those_of_every_pool_naming_it(self):
        theme = Theme(baker_street.OPTIONS)
        entries = theme.entries_from("Baker-street-characters.yaml")

        expected = ["characters/detective", "shared_lines/any_time"]
        self.assertEqual(expected, entries)

    def test_a_file_no_pool_names_fails_with_unknown_entry_file(self):
        theme = Theme(casebook.EVEN)

        with self.assertRaises(UnknownEntryFile) as raised:
            theme.entries_from("Even-scenes.yaml")

        expected = "no pool uses Even-scenes.yaml"
        self.assertEqual(expected, str(raised.exception))

    def test_the_entries_in_a_role_are_those_of_every_pool_holding_it(self):
        theme = Theme(casebook.EVEN)
        entries = theme.entries_with_role("speaker")

        expected = ["characters/host", "narrators/chorus"]
        self.assertEqual(expected, entries)


class WeightsTest(unittest.TestCase):
    def test_the_weight_of_an_entry_is_the_one_its_options_file_gives(self):
        theme = Theme(baker_street.OPTIONS)
        weight = theme.weight_of("characters/detective")

        expected = 0.57
        self.assertEqual(expected, weight)


class SaveTest(unittest.TestCase):
    def test_saving_writes_the_options_files_layout(self):
        folder = self.enterContext(tempfile.TemporaryDirectory())
        saved_options = Path(folder) / "Even-options.yaml"
        theme = Theme(casebook.EVEN)
        theme.set_weight("scenes/noon", 0.5)
        theme.set_checksum("Even-scenes.yaml", "ab12")
        theme.set_speaker_rate(0.25)
        theme.save(saved_options)
        text = saved_options.read_text(encoding="utf-8")

        expected = textwrap.dedent("""\
            checksums:
              Even-scenes.yaml: ab12
            speaker_rate: 0.25
            pools:
              scenes:
                roles: [reference]
                entries:
                  dawn:
                  noon:
                    weight: 0.5
                  dusk:
              characters:
                roles: [speaker]
                entries:
                  host:
              narrators:
                roles: [speaker]
                entries:
                  chorus:
        """)
        self.assertEqual(expected, text)
