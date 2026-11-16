from pathlib import Path

from . import casebook as casebook

FIXTURES = Path(__file__).parent

THEMES = FIXTURES / "themes"
EVEN = THEMES / "Even-options.yaml"
EVERY_TYPE = THEMES / "Every-type-options.yaml"
WITHOUT_BIG_WIN = THEMES / "Without-big-win-options.yaml"
WEIGHTED = THEMES / "Weighted-options.yaml"
NOT_THERE = THEMES / "Not-there-options.yaml"

INVALID_THEMES = FIXTURES / "invalid-themes"
WITHOUT_POOLS = INVALID_THEMES / "Without-pools-options.yaml"
POOL_WITHOUT_ROLES = INVALID_THEMES / "Pool-without-roles-options.yaml"
UNKNOWN_ROLE = INVALID_THEMES / "Unknown-role-options.yaml"
UNKNOWN_TYPE = INVALID_THEMES / "Unknown-type-options.yaml"
NEGATIVE_WEIGHT = INVALID_THEMES / "Negative-weight-options.yaml"
SPEAKERS_ONLY = INVALID_THEMES / "Speakers-only-options.yaml"
