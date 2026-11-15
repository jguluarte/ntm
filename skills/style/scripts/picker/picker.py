import argparse
import contextlib
import random
import sys
from pathlib import Path

import jsonschema
import yaml

SKILLS_PATH = Path(__file__).parents[3]
OPTIONS_SCHEMA = (
    SKILLS_PATH / "theme-builder" / "references" / "options.schema.yaml"
)

POOLS_BY_KIND = "pools"
ROLES = "roles"
ENTRIES_BY_SLUG = "entries"
WHEN = "when"
HOOK_ROLE = "hook"

REMINDERS = frozenset({"morning", "afternoon", "evening", "weekly"})
HAPPENINGS = frozenset({"slipped", "done", "big_win"})
BIG_WIN = "big_win"
DONE = "done"


class InvalidOptions(ValueError):
    def __init__(self, where, why):
        super().__init__(f"{where}: {why}")


class NoHooks(ValueError):
    def __init__(self):
        super().__init__("no pool in the options file gives a hook")


class NoHookFits(ValueError):
    def __init__(self, occasions):
        listed = ", ".join(sorted(occasions))
        super().__init__(f"no hook fits the occasions {listed}")


class UnknownOccasion(argparse.ArgumentTypeError):
    def __init__(self, unknown):
        listed = ", ".join(sorted(unknown))
        super().__init__(f"not an occasion: {listed}")


class MoreThanOneReminder(argparse.ArgumentTypeError):
    def __init__(self, reminders):
        listed = ", ".join(sorted(reminders))
        super().__init__(f"more than one reminder: {listed}")


class Options:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        self._pools = fields[POOLS_BY_KIND]

    def hooks(self, occasions):
        entries_by_hook = self._entries_by_hook()
        if not entries_by_hook:
            raise NoHooks()

        hooks = self._hooks_fitting(entries_by_hook, occasions)
        if not hooks and BIG_WIN in occasions:
            normal_win = (occasions - {BIG_WIN}) | {DONE}
            hooks = self._hooks_fitting(entries_by_hook, normal_win)
        if not hooks:
            raise NoHookFits(occasions)

        return hooks

    @classmethod
    def _hooks_fitting(cls, entries_by_hook, occasions):
        hooks = []
        for hook, entry in entries_by_hook.items():
            if cls._fits(entry, occasions):
                hooks.append(hook)
        return hooks

    def _entries_by_hook(self):
        entries_by_hook = {}
        for kind, pool in self._pools.items():
            if HOOK_ROLE not in pool[ROLES]:
                continue
            for slug, entry in pool[ENTRIES_BY_SLUG].items():
                entries_by_hook[f"{kind}/{slug}"] = entry
        return entries_by_hook

    @classmethod
    def _fits(cls, entry, occasions):
        when = cls._when(entry)
        if BIG_WIN in occasions and BIG_WIN not in when:
            return False

        reminders = when & REMINDERS
        happenings = when & HAPPENINGS
        reminder_fits = not reminders or bool(reminders & occasions)
        happening_fits = not happenings or bool(happenings & occasions)
        return reminder_fits and happening_fits

    @staticmethod
    def _when(entry):
        when = (entry or {}).get(WHEN, [])
        if isinstance(when, str):
            return frozenset([when])

        return frozenset(when)

    @staticmethod
    def _load(path):
        with open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    def _validate(cls, fields):
        try:
            jsonschema.validate(fields, cls._load(OPTIONS_SCHEMA))
        except jsonschema.ValidationError as error:
            raise InvalidOptions(error.json_path, error.message) from None


class Picker:
    def __init__(self, options, seed=None, occasions=frozenset()):
        self.options = options
        self.seed = seed
        self.occasions = occasions

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            return cls(Options(flags.options), flags.seed, flags.occasions)

    def pick_hook(self):
        with self._reporting_failures():
            hooks = self.options.hooks(self.occasions)
            generator = random.Random(self.seed)
            return f"hook: { generator.choice(hooks) }"

    @classmethod
    def _parser(cls):
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        hook = subcommands.add_parser("hook", exit_on_error=False)
        hook.add_argument("--options", required=True)
        hook.add_argument(
            "--occasions", type=cls._parse_occasions, default=frozenset()
        )
        hook.add_argument("--seed", type=int)
        return parser

    @staticmethod
    def _parse_occasions(listed):
        occasions = frozenset(listed.split(","))

        unknown = occasions - REMINDERS - HAPPENINGS
        if unknown:
            raise UnknownOccasion(unknown)

        reminders = occasions & REMINDERS
        if len(reminders) > 1:
            raise MoreThanOneReminder(reminders)

        return occasions

    @staticmethod
    @contextlib.contextmanager
    def _reporting_failures():
        try:
            yield
        except Exception as failure:
            # Every failure, a bug included, is one line for the skill to read.
            why = " ".join(str(failure).split())
            sys.exit(f"Picker FAILED: { type(failure).__name__ }: {why}")


if __name__ == "__main__":
    args = sys.argv[1:]

    picker = Picker.from_args(args)
    selections = picker.pick_hook()

    print(selections)
