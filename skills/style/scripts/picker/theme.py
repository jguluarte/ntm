import enum
import hashlib
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import yaml

OPTIONS_SCHEMA = Path(__file__).with_name("options.schema.yaml")

CHECKSUMS_BY_FILE = "checksums"
POOLS_BY_KIND = "pools"
FILE = "file"
ROLES = "roles"
ENTRIES_BY_SLUG = "entries"
TYPE = "type"
WEIGHT = "weight"
HOOK_ROLE = "hook"

ABOUT = "about"
LINES = "lines"
RIFFS = "riffs"


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


class UnknownEntryFile(ValueError):
    def __init__(self, file_name):
        super().__init__(f"no pool uses {file_name}")


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

    @classmethod
    def from_entry(cls, kind, slug, entry):
        types = (entry or {}).get(TYPE, [])
        values = {types} if isinstance(types, str) else set(types)
        reminder_types = frozenset(ReminderType.named_in(values))
        task_outcomes = frozenset(TaskOutcome.named_in(values))
        return cls(kind, slug, reminder_types, task_outcomes)

    @property
    def name(self):
        return f"{self.kind}/{self.slug}"

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

    def responding_to(self, theme_options):
        if not self._hooks:
            raise NoHooks()

        names = self._names_that_fit(theme_options)

        if not names and theme_options.is_big_win:
            names = self._names_that_fit(self._as_normal_win(theme_options))

        if not names:
            raise MissingHook(theme_options)

        return names

    def _names_that_fit(self, theme_options):
        return [hook.name for hook in self._hooks if hook.fits(theme_options)]

    @staticmethod
    def _as_normal_win(theme_options):
        without_big_win = theme_options.task_outcomes - {TaskOutcome.BIG_WIN}
        task_outcomes = without_big_win | {TaskOutcome.DONE}
        return ThemeOptions(theme_options.reminder_type, task_outcomes)


class _OptionsDumper(yaml.SafeDumper):
    def represent_list_on_one_line(self, items):
        return self.represent_sequence(
            "tag:yaml.org,2002:seq", items, flow_style=True,
        )

    def represent_bare_entry(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")


_OptionsDumper.add_representer(list, _OptionsDumper.represent_list_on_one_line)
_OptionsDumper.add_representer(type(None), _OptionsDumper.represent_bare_entry)


class Theme:
    def __init__(self, path):
        self._path = path
        self._fields = self._load(path)
        self._validate(self._fields)
        self._checksums = self._fields.pop(CHECKSUMS_BY_FILE, {})
        hooks = self._read_hooks(self._fields[POOLS_BY_KIND])
        self._hook_manager = HookManager(hooks)

    def hooks_for(self, theme_options):
        return self._hook_manager.responding_to(theme_options)

    def entries_from(self, file_name):
        names = []

        for kind, pool in self._fields[POOLS_BY_KIND].items():
            if pool.get(FILE) == file_name:
                names += [f"{kind}/{slug}" for slug in pool[ENTRIES_BY_SLUG]]

        if not names:
            raise UnknownEntryFile(file_name)

        return names

    def set_weight(self, entry_name, weight):
        kind, slug = entry_name.split("/")
        entries_by_slug = self._fields[POOLS_BY_KIND][kind][ENTRIES_BY_SLUG]
        entry = entries_by_slug[slug] or {}
        entries_by_slug[slug] = {**entry, WEIGHT: weight}

    def set_checksum(self, file_name, checksum):
        self._checksums[file_name] = checksum

    def save(self):
        checksums_first = {CHECKSUMS_BY_FILE: self._checksums, **self._fields}
        text = yaml.dump(
            checksums_first, Dumper=_OptionsDumper, sort_keys=False,
        )
        Path(self._path).write_text(text, encoding="utf-8")

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


class EntryFile:
    def __init__(self, path):
        contents = Path(path).read_bytes()
        self.name = Path(path).name
        self.checksum = hashlib.sha256(contents).hexdigest()
        self.line_counts = self._count_lines(yaml.safe_load(contents))

    @classmethod
    def _count_lines(cls, fields):
        line_counts = {}

        for kind, entries_by_slug in cls._without_about(fields):
            for slug, entry in cls._without_about(entries_by_slug):
                lines = entry.get(LINES, []) + entry.get(RIFFS, [])
                line_counts[f"{kind}/{slug}"] = len(lines)

        return line_counts

    @staticmethod
    def _without_about(fields):
        return [(key, value) for key, value in fields.items() if key != ABOUT]
