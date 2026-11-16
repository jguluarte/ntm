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

DEFAULT_WEIGHT = 1
DEFAULT_SCORE = 0


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
        weight = fields.get(WEIGHT, DEFAULT_WEIGHT)
        score = fields.get(SCORE, DEFAULT_SCORE)
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


@dataclass(frozen=True)
class _Pool:
    kind: str
    weight: float
    score: float
    hooks: tuple[Option, ...]

    @classmethod
    def from_fields(cls, kind, fields):
        hooks = tuple(
            Option.from_entry(kind, slug, entry)
            for slug, entry in fields[ENTRIES_BY_SLUG].items()
        )
        weight = fields.get(WEIGHT, DEFAULT_WEIGHT)
        score = fields.get(SCORE, DEFAULT_SCORE)
        return cls(kind, weight, score, hooks)

    @property
    def name(self):
        return self.kind

    @property
    def draw_weight(self):
        return self.weight * 2 ** self.score

    def hooks_that_fit(self, theme_options):
        return [hook for hook in self.hooks if hook.fits(theme_options)]

    def can_be_drawn_for(self, theme_options):
        hooks = self.hooks_that_fit(theme_options)
        return any(hook.draw_weight > 0 for hook in hooks)


class HookManager:
    def __init__(self, pools):
        self._pools_by_kind = {pool.kind: pool for pool in pools}

    def kind_lottery_for(self, theme_options):
        drawn_for = self._theme_options_to_draw_for(theme_options)
        draw_weights = {}
        for pool in self._pools_by_kind.values():
            if pool.can_be_drawn_for(drawn_for):
                draw_weights[pool] = pool.draw_weight

        if not draw_weights:
            raise NoHookHasWeight(theme_options)

        return self._lottery_of(draw_weights)

    def hook_lottery_for(self, theme_options, kind):
        drawn_for = self._theme_options_to_draw_for(theme_options)
        hooks = self._pools_by_kind[kind].hooks_that_fit(drawn_for)
        draw_weights = {hook: hook.draw_weight for hook in hooks}
        return self._lottery_of(draw_weights)

    def _theme_options_to_draw_for(self, theme_options):
        if not self._pools_by_kind:
            raise NoHooks()

        if self._any_hook_fits(theme_options):
            return theme_options

        normal_win = self._as_normal_win(theme_options)
        if theme_options.is_big_win and self._any_hook_fits(normal_win):
            return normal_win

        raise MissingHook(theme_options)

    def _any_hook_fits(self, theme_options):
        pools = self._pools_by_kind.values()
        return any(pool.hooks_that_fit(theme_options) for pool in pools)

    @staticmethod
    def _lottery_of(draw_weights):
        total = sum(draw_weights.values())
        return {
            candidate: draw_weight / total
            for candidate, draw_weight in draw_weights.items()
        }

    @staticmethod
    def _as_normal_win(theme_options):
        without_big_win = theme_options.task_outcomes - {TaskOutcome.BIG_WIN}
        task_outcomes = without_big_win | {TaskOutcome.DONE}
        return ThemeOptions(theme_options.reminder_type, task_outcomes)


class Theme:
    def __init__(self, path):
        fields = self._load(path)
        self._validate(fields)
        pools = self._read_hook_pools(fields[POOLS_BY_KIND])
        self._hook_manager = HookManager(pools)

    def kind_lottery_for(self, theme_options):
        return self._hook_manager.kind_lottery_for(theme_options)

    def hook_lottery_for(self, theme_options, kind):
        return self._hook_manager.hook_lottery_for(theme_options, kind)

    @staticmethod
    def _read_hook_pools(pools_by_kind):
        pools = []

        for kind, fields in pools_by_kind.items():
            if HOOK_ROLE in fields[ROLES]:
                pools.append(_Pool.from_fields(kind, fields))

        return pools

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
