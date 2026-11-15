import argparse
import contextlib
import random
import sys
from pathlib import Path

import jsonschema
import yaml

SKILLS = Path(__file__).parents[3]
OPTIONS_SCHEMA = SKILLS / "theme-builder" / "references" / "options.schema.yaml"

POOLS_BY_KIND = "pools"
ROLES = "roles"
ENTRIES_BY_SLUG = "entries"
HOOK_ROLE = "hook"

HOOK_LINE = "hook: {}"
FAILURE_LINE = "Picker FAILED: {}: {}"


class NoHooks(ValueError):
    def __init__(self):
        super().__init__("no pool in the options file gives a hook")


class Options:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        self._pools = fields[POOLS_BY_KIND]

    def hooks(self):
        hooks = []
        for kind, pool in self._pools.items():
            if HOOK_ROLE in pool[ROLES]:
                hooks.extend(f"{kind}/{slug}" for slug in pool[ENTRIES_BY_SLUG])
        if not hooks:
            raise NoHooks()
        return hooks

    @staticmethod
    def _load(path):
        with open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    def _validate(cls, fields):
        try:
            jsonschema.validate(fields, cls._load(OPTIONS_SCHEMA))
        except jsonschema.ValidationError as error:
            raise ValueError(f"{error.json_path}: {error.message}") from None


class Picker:
    def __init__(self, options, seed=None):
        self.options = options
        self.seed = seed

    @classmethod
    def from_args(cls, args):
        with cls._reporting_failures():
            flags = cls._parser().parse_args(args)
            return cls(Options(flags.options), flags.seed)

    def pick_hook(self):
        with self._reporting_failures():
            hooks = self.options.hooks()
            generator = random.Random(self.seed)
            return HOOK_LINE.format(generator.choice(hooks))

    @staticmethod
    def _parser():
        parser = argparse.ArgumentParser(exit_on_error=False)
        subcommands = parser.add_subparsers(required=True)
        hook = subcommands.add_parser("hook", exit_on_error=False)
        hook.add_argument("--options", required=True)
        hook.add_argument("--seed", type=int)
        return parser

    @staticmethod
    @contextlib.contextmanager
    def _reporting_failures():
        try:
            yield
        except Exception as failure:
            # Every failure, a bug included, is one line for the skill to read.
            why = " ".join(str(failure).split())
            sys.exit(FAILURE_LINE.format(type(failure).__name__, why))


if __name__ == "__main__":
    args = sys.argv[1:]

    picker = Picker.from_args(args)
    selections = picker.pick_hook()

    print(selections)
