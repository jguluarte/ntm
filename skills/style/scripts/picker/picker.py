import argparse
import contextlib
import random
import sys
from pathlib import Path

import jsonschema
import yaml

SCHEMA = Path(__file__).with_name("options.schema.yaml")
POOLS = "pools"
GIVES = "gives"
ENTRIES = "entries"
HOOK = "hook"
OPTIONS = "--options"
SEED = "--seed"
HOOK_LINE = "hook: {}"
NO_HOOKS = "no pool in the options file gives a hook"
FAILED = "Picker FAILED: {}: {}"


class Options:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        self._pools = fields[POOLS]

    def hooks(self):
        hooks = []
        for kind, pool in self._pools.items():
            if HOOK in pool[GIVES]:
                hooks.extend(f"{kind}/{slug}" for slug in pool[ENTRIES])
        if not hooks:
            raise ValueError(NO_HOOKS)
        return hooks

    @staticmethod
    def _load(path):
        with open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    def _validate(cls, fields):
        try:
            jsonschema.validate(fields, cls._load(SCHEMA))
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
        hook = subcommands.add_parser(HOOK, exit_on_error=False)
        hook.add_argument(OPTIONS, required=True)
        hook.add_argument(SEED, type=int)
        return parser

    @staticmethod
    @contextlib.contextmanager
    def _reporting_failures():
        try:
            yield
        except Exception as failure:
            # Every failure, a bug included, is one line for the skill to read.
            why = " ".join(str(failure).split())
            sys.exit(FAILED.format(type(failure).__name__, why))


if __name__ == "__main__":
    args = sys.argv[1:]
    picker = Picker.from_args(args)
    selections = picker.pick_hook()
    print(selections)
