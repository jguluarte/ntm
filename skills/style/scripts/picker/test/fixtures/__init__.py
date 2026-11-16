from pathlib import Path

FIXTURES = Path(__file__).parent

THEMES = FIXTURES / "themes"
EVEN = THEMES / "Even-options.yaml"
CASEBOOK = THEMES / "Casebook-options.yaml"
WITHOUT_NUMBERS = THEMES / "Without-numbers-options.yaml"
EVERY_TYPE = THEMES / "Every-type-options.yaml"
WITHOUT_BIG_WIN = THEMES / "Without-big-win-options.yaml"
SPEAKERS_ONLY = THEMES / "Speakers-only-options.yaml"
NOT_THERE = THEMES / "Not-there-options.yaml"

INVALID_THEMES = FIXTURES / "invalid-themes"
WITHOUT_POOLS = INVALID_THEMES / "Without-pools-options.yaml"
POOL_WITHOUT_ROLES = INVALID_THEMES / "Pool-without-roles-options.yaml"
UNKNOWN_ROLE = INVALID_THEMES / "Unknown-role-options.yaml"
UNKNOWN_TYPE = INVALID_THEMES / "Unknown-type-options.yaml"

ENTRY_FILES = FIXTURES / "entry-files"
CASEBOOK_CHARACTERS = ENTRY_FILES / "Casebook-characters.yaml"
CASEBOOK_SCENES = ENTRY_FILES / "Casebook-scenes.yaml"
