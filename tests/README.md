# Tests

`make test` runs the bats tests here (Bash Automated Testing System), then the
picker's Python tests in `skills/style/scripts/picker/test/` with pytest. Each
`@test` block is one test, and it fails when a line in it fails. bats, jq,
Python, PyYAML, jsonschema and pytest come from devbox.

## User-facing names

The user-facing names are a contract: the skills, the agents, and the
`plugin.json` fields listed in `expected/plugin.json`. `user-facing-names.bats`
holds the plugin to the contract in `expected/`, and fails on any difference: a
name added, a name removed, or a changed value.

- `expected/skills.txt`: one skill per line, a folder `skills/<name>/`
- `expected/agents.txt`: one agent per line, a file `agents/<name>.md`
- `expected/plugin.json`: the `plugin.json` fields that must match

A rename fails twice: once as a name added, once as a name removed.

A failing test means a change modified the contract. When the change is meant,
update `expected/` in the same PR and say so in its description: the user sees
the rename in the diff and can push back before merging. When it isn't, put the
name back. `git log tests/expected/` is the record of every name change.

## The style skill's scripts

`skills/style/scripts/picker/test/` holds the tests of the picker and
`recalculate.py`, in `skills/style/scripts/picker/`, written as `unittest` test
cases and run by pytest. `pyproject.toml` puts that folder on Python's import
path, so a test imports their classes by name.

| File                  | What it checks                                                         |
| --------------------- | ---------------------------------------------------------------------- |
| `test_theme.py`       | The lottery `Theme` builds, one entry file's entries, saving, failures |
| `test_lottery.py`     | The chances a `Lottery` gives, and that a seed draws the same          |
| `test_entry_file.py`  | The line counts and checksum `EntryFile` reads                         |
| `test_picker.py`      | What a `Picker` picks, the chances table, and the one failure line     |
| `test_recalculate.py` | What a `Recalculation` weighs and records, or fails with               |

`fixtures/` holds the themes they read. A theme with several files has a folder
of its own, whose `__init__.py` names each file. A one-file theme is an options
file named for what it holds or lacks.

| Folder            | What it holds                                                  |
| ----------------- | -------------------------------------------------------------- |
| `casebook/`       | The example in `references/theme-files.md`                     |
| `weighing/`       | A theme without numbers whose entries have 1, 3, 9 and 0 lines |
| `themes/`         | One-file themes `Theme` loads                                  |
| `invalid-themes/` | One-file themes `Theme` refuses, named for the fault           |
