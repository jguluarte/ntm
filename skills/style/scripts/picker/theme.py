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
HOOK_ROLE = "hook"


class InvalidTheme(ValueError):
    def __init__(self, where, why):
        super().__init__(f"{where}: {why}")


class NoHooks(ValueError):
    def __init__(self):
        super().__init__("no pool in the options file gives a hook")


class Theme:
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
            raise InvalidTheme(error.json_path, error.message) from None
