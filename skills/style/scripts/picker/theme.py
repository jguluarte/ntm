import enum
from dataclasses import dataclass
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


class ReminderType(enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    WEEKLY = "weekly"


class TaskOutcome(enum.Enum):
    SLIPPED = "slipped"
    DONE = "done"
    BIG_WIN = "big_win"


class InvalidTheme(ValueError):
    def __init__(self, where, why):
        super().__init__(f"{where}: {why}")


class InvalidThemeOptions(ValueError):
    def __init__(self, why, values):
        listed = ", ".join(sorted(values))
        super().__init__(f"{why}: {listed}")


class MissingHook(ValueError):
    pass


@dataclass(frozen=True)
class ThemeOptions:
    reminder_type: ReminderType = None
    task_outcomes: frozenset = frozenset()

    @classmethod
    def parse(cls, listed):
        values = set(listed.split(",")) if listed else set()
        reminder_types = {each for each in ReminderType if each.value in values}
        task_outcomes = {each for each in TaskOutcome if each.value in values}

        known = {each.value for each in reminder_types | task_outcomes}
        unknown = values - known
        if unknown:
            raise InvalidThemeOptions("not an option", unknown)

        if len(reminder_types) > 1:
            named = {each.value for each in reminder_types}
            raise InvalidThemeOptions("more than one reminder type", named)

        reminder_type = reminder_types.pop() if reminder_types else None
        return cls(reminder_type, frozenset(task_outcomes))

    @property
    def is_big_win(self):
        return TaskOutcome.BIG_WIN in self.task_outcomes

    def as_normal_win(self):
        without_big_win = self.task_outcomes - {TaskOutcome.BIG_WIN}
        task_outcomes = without_big_win | {TaskOutcome.DONE}
        return ThemeOptions(self.reminder_type, task_outcomes)

    def __str__(self):
        values = sorted(each.value for each in self.task_outcomes)
        if self.reminder_type:
            values.insert(0, self.reminder_type.value)
        return ",".join(values)


@dataclass(frozen=True)
class _KeptFor:
    reminder_types: frozenset
    task_outcomes: frozenset

    @classmethod
    def read(cls, entry):
        when = (entry or {}).get(WHEN, [])
        values = {when} if isinstance(when, str) else set(when)
        reminder_types = {each for each in ReminderType if each.value in values}
        task_outcomes = {each for each in TaskOutcome if each.value in values}
        return cls(frozenset(reminder_types), frozenset(task_outcomes))

    @property
    def is_big_win(self):
        return TaskOutcome.BIG_WIN in self.task_outcomes

    def fits(self, theme_options):
        if theme_options.is_big_win and not self.is_big_win:
            return False

        reminder_type = theme_options.reminder_type
        if self.reminder_types and reminder_type not in self.reminder_types:
            return False

        task_outcomes = theme_options.task_outcomes
        if self.task_outcomes and self.task_outcomes.isdisjoint(task_outcomes):
            return False

        return True


class Theme:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        self._kept_for_by_hook = self._read_hooks(fields[POOLS_BY_KIND])

    def hooks_for(self, theme_options):
        if not self._kept_for_by_hook:
            raise MissingHook("no pool in the options file gives a hook")

        hooks = self._hooks_fitting(theme_options)
        if not hooks and theme_options.is_big_win:
            hooks = self._hooks_fitting(theme_options.as_normal_win())
        if not hooks:
            raise MissingHook(f"no hook fits {theme_options}")

        return hooks

    def _hooks_fitting(self, theme_options):
        hooks = []
        for hook, kept_for in self._kept_for_by_hook.items():
            if kept_for.fits(theme_options):
                hooks.append(hook)
        return hooks

    @staticmethod
    def _read_hooks(pools_by_kind):
        kept_for_by_hook = {}
        for kind, pool in pools_by_kind.items():
            if HOOK_ROLE not in pool[ROLES]:
                continue
            for slug, entry in pool[ENTRIES_BY_SLUG].items():
                kept_for_by_hook[f"{kind}/{slug}"] = _KeptFor.read(entry)
        return kept_for_by_hook

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
