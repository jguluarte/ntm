# Tests

`make test` runs the bats tests here (Bash Automated Testing System). Each
`@test` block is one test, and it fails when a line in it fails. bats and jq
come from devbox.

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

## The picker

`picker.bats` holds the picker, `scripts/picker/pick`, to what its reference
says. Most tests run on small made-up themes in `picker/`: `Casebook`, with a
history; `Solo`, a theme of one person; and `Even`, three hooks of the same
weight and one of weight 0. A test about one odd file writes that file itself.

A test reads one number or set from `pick --chances`, or picks at a fixed
`--seed`, so no test depends on luck. One test holds the random number generator
to its published numbers. The tools tests run the picker with only the tools
they name.
