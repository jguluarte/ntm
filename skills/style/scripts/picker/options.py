from pathlib import Path

import jsonschema
import yaml

SCHEMA = Path(__file__).with_name("options.schema.yaml")
POOLS = "pools"
GIVES = "gives"
ENTRIES = "entries"
HOOK = "hook"
NO_HOOKS = "no pool in the options file gives a hook"


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
