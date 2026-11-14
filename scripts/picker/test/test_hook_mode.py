from flags import Flags
from hook_mode import HookMode
from picker_test_case import PickerTestCase

EVEN_HOOKS = {"scenes/dawn", "scenes/noon", "scenes/dusk"}


class HookModeTest(PickerTestCase):
    def report(self, theme, *more):
        flags = Flags(HookMode, self.arguments(theme, *more))
        return HookMode(flags).report()

    def picks(self, theme, seed):
        report = self.report(theme, "--seed", str(seed))
        return dict(line.split(": ", 1) for line in report.splitlines())


class DrawTest(HookModeTest):
    def test_every_hook_can_be_drawn(self):
        seeds = range(100)
        drawn = {self.picks("Even", seed)["hook"] for seed in seeds}
        self.assertEqual(EVEN_HOOKS, drawn)

    def test_the_same_seed_draws_the_same_hook(self):
        first = [self.picks("Even", seed) for seed in range(1, 6)]
        again = [self.picks("Even", seed) for seed in range(1, 6)]
        self.assertEqual(first, again)


class FlagsTest(HookModeTest):
    def test_a_flag_the_mode_doesnt_take_fails_naming_it(self):
        why = "pick hook doesn't take --entries"
        entries = ["--entries", "Even-scenes.yaml"]
        self.assertFails(why, self.report, "Even", *entries)


class OptionsFileTest(HookModeTest):
    def test_an_options_file_that_isnt_yaml_fails_naming_it(self):
        self.themes = self.folder
        path = self.write("Dusk-options.yaml", "pools: [unclosed\n")
        self.assertFails(f"{path} isn't YAML", self.report, "Dusk")

    def test_an_options_file_that_cant_be_read_fails_naming_it(self):
        self.themes = self.folder
        path = self.folder / "Gone-options.yaml"
        self.assertFails(f"can't read {path}", self.report, "Gone")
