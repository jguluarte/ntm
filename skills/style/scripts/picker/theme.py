import enum
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import yaml

OPTIONS_SCHEMA = Path(__file__).with_name("options.schema.yaml")

POOLS_BY_KIND = "pools"
ROLES = "roles"
ENTRIES_BY_SLUG = "entries"
TYPE = "type"
WEIGHT = "weight"
SCORE = "score"
HOOK_ROLE = "hook"


class ReminderType(enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    WEEKLY = "weekly"

    @classmethod
    def named_in(cls, values):
        known = {reminder_type.value for reminder_type in cls}
        return {cls(value) for value in values & known}


class TaskOutcome(enum.Enum):
    SLIPPED = "slipped"
    DONE = "done"
    BIG_WIN = "big_win"

    @classmethod
    def named_in(cls, values):
        known = {task_outcome.value for task_outcome in cls}
        return {cls(value) for value in values & known}


class InvalidTheme(ValueError):
    def __init__(self, where, why):
        super().__init__(f"{where}: {why}")


class InvalidOptions(ValueError):
    pass


class UnknownOption(InvalidOptions):
    def __init__(self, values):
        listed = ", ".join(sorted(values))
        super().__init__(f"not an option: {listed}")


class MoreThanOneReminderType(InvalidOptions):
    def __init__(self, reminder_types):
        values = sorted(reminder_type.value for reminder_type in reminder_types)
        listed = ", ".join(values)
        super().__init__(f"more than one reminder type: {listed}")


class NoHooks(ValueError):
    def __init__(self):
        super().__init__("no pool in the options file gives a hook")


class MissingHook(ValueError):
    def __init__(self, theme_options):
        super().__init__(f"no hook fits {theme_options}")


class NoHookHasWeight(ValueError):
    def __init__(self, theme_options):
        super().__init__(f"every hook that fits {theme_options} weighs 0")


@dataclass(frozen=True)
class ThemeOptions:
    reminder_type: ReminderType | None = None
    task_outcomes: frozenset[TaskOutcome] = frozenset()

    @classmethod
    def parse(cls, text):
        values = set(text.split(","))
        reminder_types = ReminderType.named_in(values)
        task_outcomes = TaskOutcome.named_in(values)

        options = reminder_types | task_outcomes
        unknown = values - {option.value for option in options}
        if unknown:
            raise UnknownOption(unknown)

        if len(reminder_types) > 1:
            raise MoreThanOneReminderType(reminder_types)

        reminder_type = reminder_types.pop() if reminder_types else None
        return cls(reminder_type, frozenset(task_outcomes))

    @property
    def is_big_win(self):
        return TaskOutcome.BIG_WIN in self.task_outcomes

    def __str__(self):
        reminder = [self.reminder_type.value] if self.reminder_type else []
        outcomes = sorted(outcome.value for outcome in self.task_outcomes)
        return ",".join(reminder + outcomes)


@dataclass(frozen=True)
class Option:
    kind: str
    slug: str
    reminder_types: frozenset[ReminderType]
    task_outcomes: frozenset[TaskOutcome]
    weight: float
    score: float

    @classmethod
    def from_entry(cls, kind, slug, entry):
        fields = entry or {}
        types = fields.get(TYPE, [])
        values = {types} if isinstance(types, str) else set(types)
        reminder_types = frozenset(ReminderType.named_in(values))
        task_outcomes = frozenset(TaskOutcome.named_in(values))
        weight = fields.get(WEIGHT, 1)
        score = fields.get(SCORE, 0)
        return cls(kind, slug, reminder_types, task_outcomes, weight, score)

    @property
    def name(self):
        return f"{self.kind}/{self.slug}"

    @property
    def draw_weight(self):
        return self.weight * 2 ** self.score

    @property
    def kept_for_big_win(self):
        return TaskOutcome.BIG_WIN in self.task_outcomes

    def fits(self, theme_options):
        if theme_options.is_big_win and not self.kept_for_big_win:
            return False

        reminder_type = theme_options.reminder_type
        if self.reminder_types and reminder_type not in self.reminder_types:
            return False

        task_outcomes = theme_options.task_outcomes
        if self.task_outcomes and self.task_outcomes.isdisjoint(task_outcomes):
            return False

        return True


class HookManager:
    def __init__(self, hooks):
        self._hooks = hooks

    def chances_for(self, theme_options):
        hooks = self._responding_to(theme_options)
        total = sum(hook.draw_weight for hook in hooks)

        if total == 0:
            raise NoHookHasWeight(theme_options)

        return {hook: hook.draw_weight / total for hook in hooks}

    def _responding_to(self, theme_options):
        if not self._hooks:
            raise NoHooks()

        hooks = self._hooks_that_fit(theme_options)

        if not hooks and theme_options.is_big_win:
            hooks = self._hooks_that_fit(self._as_normal_win(theme_options))

        if not hooks:
            raise MissingHook(theme_options)

        return hooks

    def _hooks_that_fit(self, theme_options):
        return [hook for hook in self._hooks if hook.fits(theme_options)]

    @staticmethod
    def _as_normal_win(theme_options):
        without_big_win = theme_options.task_outcomes - {TaskOutcome.BIG_WIN}
        task_outcomes = without_big_win | {TaskOutcome.DONE}
        return ThemeOptions(theme_options.reminder_type, task_outcomes)


class Theme:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        hooks = self._read_hooks(fields[POOLS_BY_KIND])
        self._hook_manager = HookManager(hooks)

    def hook_chances_for(self, theme_options):
        return self._hook_manager.chances_for(theme_options)

    @staticmethod
    def _read_hooks(pools_by_kind):
        hooks = []

        for kind, pool in pools_by_kind.items():
            if HOOK_ROLE in pool[ROLES]:
                for slug, entry in pool[ENTRIES_BY_SLUG].items():
                    hooks.append(Option.from_entry(kind, slug, entry))

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
