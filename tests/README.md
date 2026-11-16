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

| File                    | What it checks                                                         |
| ----------------------- | ---------------------------------------------------------------------- |
| `test_theme.py`         | The hooks `Theme` finds, an entry file's entries, saving, and failures |
| `test_theme_options.py` | The combinations `ThemeOptions` parses or refuses                      |
| `test_entry_file.py`    | The line counts and checksum `EntryFile` reads                         |
| `test_picker.py`        | What the picker's command line builds, prints or fails with            |
| `test_recalculate.py`   | What `start` builds from its command line, saves or fails with         |

`fixtures/` holds the options files they read, each named for what it holds or
lacks, and the example in `references/theme-files.md`: `Casebook-options.yaml`
and its two entry files.
