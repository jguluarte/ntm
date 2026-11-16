from pathlib import Path

from . import casebook as casebook
from . import weighing as weighing

FIXTURES = Path(__file__).parent

THEMES = FIXTURES / "themes"
EVEN = THEMES / "Even-options.yaml"
WEIGHTED = THEMES / "Weighted-options.yaml"
WEIGHTLESS = THEMES / "Weightless-options.yaml"
MOSTLY_WEIGHTLESS = THEMES / "Mostly-weightless-options.yaml"
NOT_THERE = THEMES / "Not-there-options.yaml"

INVALID_THEMES = FIXTURES / "invalid-themes"
WITHOUT_POOLS = INVALID_THEMES / "Without-pools-options.yaml"
POOL_WITHOUT_ROLES = INVALID_THEMES / "Pool-without-roles-options.yaml"
UNKNOWN_ROLE = INVALID_THEMES / "Unknown-role-options.yaml"
NEGATIVE_WEIGHT = INVALID_THEMES / "Negative-weight-options.yaml"
SPEAKERS_ONLY = INVALID_THEMES / "Speakers-only-options.yaml"
