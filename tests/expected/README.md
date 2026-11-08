# Expected names

The names a user sees, as Justin expects them. `make test` fails when the plugin
and these files disagree in either direction: a name the plugin has that isn't
listed here, or a name listed here that the plugin doesn't have.

- `skills.txt`: one line per skill, a folder `skills/<name>/` with a `SKILL.md`
- `agents.txt`: one line per agent, a file `agents/<name>.md`
- `plugin.json`: the values `.claude-plugin/plugin.json` must have. Keys not
  listed here, such as `version` and `description`, change freely.

`make test` also fails when a skill's or agent's frontmatter `name:` line
differs from its folder or file name, since that is the name a user sees.

`.claude/NAMES.md` is the record of every approved name and where Justin said
yes. These files are what `make test` holds the plugin to, and they follow
NAMES.md.

Only Justin edits this folder. A Claude Code hook in his own settings, outside
this repo, blocks every Claude session from writing to it, so a rename can't
pass by updating these files.

## Approving a change

1. A PR adds, removes or renames a skill, an agent or a plugin.json value, and
   `make test` fails.
2. Justin says yes or no on the PR. On a no, the change is put back.
3. On a yes, his yes goes in NAMES.md as usual, and he edits the line here
   himself: rename it, add it or delete it.
4. He commits it as "Approve <what>", for example "Approve skill rename: today
   to whats-planned".
