import hashlib
import random
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import jsonschema
import yaml

OPTIONS_SCHEMA = Path(__file__).with_name("options.schema.yaml")

CHECKSUMS_BY_FILE = "checksums"
POOLS_BY_KIND = "pools"
FILE = "file"
ROLES = "roles"
ENTRIES_BY_SLUG = "entries"
WEIGHT = "weight"
SCORE = "score"
HOOK_ROLE = "hook"

ABOUT = "about"
LINES = "lines"
RIFFS = "riffs"


class InvalidTheme(ValueError):
    def __init__(self, where, why):
        super().__init__(f"{where}: {why}")


class MissingWeight(ValueError):
    def __init__(self):
        super().__init__("every option weighs 0")


class UnknownEntryFile(ValueError):
    def __init__(self, file_name):
        super().__init__(f"no pool uses {file_name}")


@dataclass(frozen=True)
class Option:
    kind: str
    slug: str
    weight: float
    score: float

    @classmethod
    def from_entry(cls, kind, slug, entry):
        fields = entry or {}
        weight = fields.get(WEIGHT, 1)
        score = fields.get(SCORE, 0)
        return cls(kind, slug, weight, score)

    @property
    def name(self):
        return f"{self.kind}/{self.slug}"

    @property
    def draw_weight(self):
        return self.weight * 2 ** self.score


class Lottery:
    def __init__(self, draw_weights, seed=None):
        self._generator = random.Random(seed)
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
    def __init__(self, path, seed=None):
        self.path = path
        self.seed = seed
        self._fields = self._load(path)
        self._validate(self._fields)
        self._checksums = self._fields.pop(CHECKSUMS_BY_FILE, {})
        self._options = self._read_options(self._fields[POOLS_BY_KIND])

        if not self._options:
            raise InvalidTheme(f"$.{POOLS_BY_KIND}", "no options found")

    @cached_property
    def lottery(self):
        draw_weights = {option: option.draw_weight for option in self._options}

        if not any(draw_weights.values()):
            raise MissingWeight()

        return Lottery(draw_weights, self.seed)

    def draw(self):
        return self.lottery.draw()

    def entries_from(self, file_name):
        names = []

        for kind, pool in self._fields[POOLS_BY_KIND].items():
            if pool.get(FILE) == file_name:
                names += [f"{kind}/{slug}" for slug in pool[ENTRIES_BY_SLUG]]

        if not names:
            raise UnknownEntryFile(file_name)

        return names

    def weight_of(self, entry_name):
        kind, slug = entry_name.split("/")
        entries_by_slug = self._fields[POOLS_BY_KIND][kind][ENTRIES_BY_SLUG]
        entry = entries_by_slug[slug] or {}
        return entry.get(WEIGHT, 1)

    def set_weight(self, entry_name, weight):
        kind, slug = entry_name.split("/")
        entries_by_slug = self._fields[POOLS_BY_KIND][kind][ENTRIES_BY_SLUG]
        entry = entries_by_slug[slug] or {}
        entries_by_slug[slug] = {**entry, WEIGHT: weight}

    def checksum_of(self, file_name):
        return self._checksums[file_name]

    def set_checksum(self, file_name, checksum):
        self._checksums[file_name] = checksum

    def save(self, path=None):
        checksums_first = {CHECKSUMS_BY_FILE: self._checksums, **self._fields}
        text = yaml.dump(
            checksums_first, Dumper=_OptionsDumper, sort_keys=False,
        )
        Path(path or self.path).write_text(text, encoding="utf-8")

    @staticmethod
    def _read_options(pools_by_kind):
        options = []

        for kind, pool in pools_by_kind.items():
            if HOOK_ROLE in pool[ROLES]:
                for slug, entry in pool[ENTRIES_BY_SLUG].items():
                    option = Option.from_entry(kind, slug, entry)
                    options.append(option)

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
