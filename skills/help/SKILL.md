---
name: help
description: >-
    What Neurodivergent Task Manager (ntm) is and how to use it, answered from
    the installed plugin's README. Shown when the user asks what ntm does, how
    to get started, what a skill is for, which version is installed, or for help
    with ntm.
---

# ntm:help

The plugin's README is the one text about ntm. This skill holds none of it: it
finds the README and answers from it.

## Finding the newest copy

Several copies of ntm can sit side by side: a synced upload keeps older
generations, such as `ntm` 0.3.0 beside `ntm~g2` 0.3.2. List each copy's
version:

```bash
find ~/.claude/plugins -path '*ntm*/.claude-plugin/plugin.json' \
    -not -path '*ntm-user*' -exec grep -H '"version"' {} +
```

Use the copy with the highest version. Its README sits two folders up from its
`plugin.json`.

If nothing is found, say in one line that the README is on the plugin's Contents
tab under Customize > Plugins, or in the repository, and stop.

## Answering

Read the README. Answer the question from the section that covers it, in prose,
short; never paste the whole file. With no specific question, give its opening
paragraph and First steps. If the README doesn't answer it, say so and name the
skill in its Skills list that would know.

## Which version is installed

Name both versions: ntm's, from the newest copy's `plugin.json`, and ntm-user's,
from the Built line its backend skill opens with. Find that line in the newest
copy of ntm-user:

```bash
find ~/.claude/plugins -path '*ntm-user*/skills/backend/SKILL.md' \
    -exec grep -H '^Built:' {} +
```

Give the line's ntm-user version, the ntm version it was built from, and its
date. If no Built line is found, say ntm-user isn't set up yet and `/ntm:setup`
builds it.
