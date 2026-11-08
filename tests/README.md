# Tests

`make test` runs the bats tests here. bats and jq come from devbox.

## User-facing names

User-facing names change only with Justin's yes. `user-facing-names.bats`
compares the names the plugin has with the names he expects in `expected/`, and
fails either way: a name the plugin has that isn't expected, or an expected name
the plugin doesn't have.

- `expected/skills.txt`: one skill per line, a folder `skills/<name>/`
- `expected/agents.txt`: one agent per line, a file `agents/<name>.md`
- `expected/plugin.json`: the `plugin.json` values that must match

Only Justin edits `expected/`. A Claude Code hook in his own settings blocks
every Claude session from writing to it.

To approve a rename, Justin edits the line in `expected/` himself and commits it
as "Approve <what>", for example "Approve skill rename: today to whats-planned".
`git log tests/expected/` is the record of every name he approved.
