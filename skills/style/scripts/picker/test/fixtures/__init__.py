from pathlib import Path

FIXTURES = Path(__file__).parent
EVEN = FIXTURES / "Even-options.yaml"
SILENT = FIXTURES / "Silent-options.yaml"
SHAPELESS = FIXTURES / "Shapeless-options.yaml"

EVEN_HOOKS = ["scenes/dawn", "scenes/noon", "scenes/dusk", "characters/host"]
EVEN_DRAWS = {
    0: "hook: characters/host",
    1: "hook: scenes/noon",
    2: "hook: scenes/dawn",
    3: "hook: scenes/noon",
    4: "hook: scenes/noon",
    5: "hook: scenes/dusk",
}
