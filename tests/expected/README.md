# Expected names

The names a user sees, as Justin expects them. `make test` fails when the plugin
and these files disagree in either direction: a name the plugin has that isn't
listed here, or a name listed here that the plugin doesn't have.

- `skills.txt`: one line per folder `skills/<name>/`
- `agents.txt`: one line per file `agents/<name>.md`
- `plugin.json`: the values `.claude-plugin/plugin.json` must have. Keys not
  listed here, such as `version` and `description`, change freely.

Only Justin edits this folder. A local Claude Code hook blocks every Claude
session from writing to it, so a rename can't pass by updating these files.

## Approving a change

1. A PR adds, removes or renames a skill, an agent or a plugin.json value, and
   `make test` fails.
2. Justin says yes or no on the PR. On a no, the change is put back.
3. On a yes, he edits the line here himself: rename it, add it or delete it.
4. He commits it as "Approve <what>", for example "Approve skill rename: today
   to whats-planned".

`git log tests/expected/` is the record of every name he approved.
