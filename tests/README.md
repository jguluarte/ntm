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

A failing test means a change modified the contract, and that needs the explicit
involvement of the user. Put the name back, or get the user's explicit approval.
On a yes, the user updates `expected/` and commits it as "Approve <what>", for
example "Approve skill rename: today to whats-planned".
`git log tests/expected/` is the record of every approved name.
