import copy
import enum
import hashlib
import random
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
SCORE = "score"
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


class MissingOptions(ValueError):
    def __init__(self, options):
        super().__init__(f"no option fits {options}")


class MissingWeight(ValueError):
    def __init__(self, options):
        super().__init__(f"every option that fits {options} weighs 0")


class UnknownEntryFile(ValueError):
    def __init__(self, file_name):
        super().__init__(f"no pool uses {file_name}")


@dataclass(init=False)
class ThemeOptions:
    reminder_type: ReminderType | None
    task_outcomes: frozenset[TaskOutcome]

    def __init__(self, type=""):
        values = set(type.split(",")) if type else set()
        reminder_types = ReminderType.named_in(values)
        task_outcomes = TaskOutcome.named_in(values)

        known = reminder_types | task_outcomes
        unknown = values - {member.value for member in known}
        if unknown:
            raise UnknownOption(unknown)

        if len(reminder_types) > 1:
            raise MoreThanOneReminderType(reminder_types)

        self.reminder_type = reminder_types.pop() if reminder_types else None
        self.task_outcomes = frozenset(task_outcomes)

    @property
    def is_big_win(self):
        return TaskOutcome.BIG_WIN in self.task_outcomes

    def as_finished_task(self):
        finished_task = copy.copy(self)
        without_big_win = self.task_outcomes - {TaskOutcome.BIG_WIN}
        finished_task.task_outcomes = without_big_win | {TaskOutcome.DONE}
        return finished_task

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

    def fits(self, options):
        if options.is_big_win and not self.kept_for_big_win:
            return False

        reminder_type = options.reminder_type
        if self.reminder_types and reminder_type not in self.reminder_types:
            return False

        task_outcomes = options.task_outcomes
        if self.task_outcomes and self.task_outcomes.isdisjoint(task_outcomes):
            return False

        return True


class Lottery:
    _generator = random.Random()

    @classmethod
    def set_seed(cls, seed):
        cls._generator.seed(seed)

    def __init__(self, draw_weights):
        total = sum(draw_weights.values())
        self.chance_by_candidate = {
            candidate: draw_weight / total
            for candidate, draw_weight in draw_weights.items()
        }

    @property
    def names(self):
        return [candidate.name for candidate in self.chance_by_candidate]

    @property
    def chance_by_name(self):
        chances = self.chance_by_candidate.items()
        return {candidate.name: chance for candidate, chance in chances}

    def draw(self):
        candidates = list(self.chance_by_candidate)
        chances = self.chance_by_candidate.values()
        [winner] = self._generator.choices(candidates, weights=chances)
        return winner


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
        self.path = path
        self._fields = self._load(path)
        self._validate(self._fields)
        self._checksums = self._fields.pop(CHECKSUMS_BY_FILE, {})
        self._options = self._read_options(self._fields[POOLS_BY_KIND])

        if not self._options:
            raise InvalidTheme(f"$.{POOLS_BY_KIND}", "no pool gives a hook")

    def lottery_for(self, options):
        fitting = self._fitting(options)

        if not fitting and options.is_big_win:
            fitting = self._fitting(options.as_finished_task())

        if not fitting:
            raise MissingOptions(options)

        draw_weights = {option: option.draw_weight for option in fitting}

        if not any(draw_weights.values()):
            raise MissingWeight(options)

        return Lottery(draw_weights)

    def draw_from(self, options):
        return self.lottery_for(options).draw()

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
        Path(self.path).write_text(text, encoding="utf-8")

    def _fitting(self, options):
        return [option for option in self._options if option.fits(options)]

    @staticmethod
    def _read_options(pools_by_kind):
        options = []

        for kind, pool in pools_by_kind.items():
            if HOOK_ROLE in pool[ROLES]:
                for slug, entry in pool[ENTRIES_BY_SLUG].items():
                    options.append(Option.from_entry(kind, slug, entry))

        return options

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
