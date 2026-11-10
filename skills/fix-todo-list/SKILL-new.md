---
name: fix-todo-list
description: >-
    Tidies the user's task list by clearing stale planned dates, and returns
    what it changed. Run by a job, or by the user ("fix my todo list", "tidy my
    todo list").
---

# ntm:fix-todo-list

Clears every stale planned date, and returns what it changed. A planned date is
stale when it's before today and its task is still open.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## Usage

```
/ntm:fix-todo-list [--dry-run]
```

With `--dry-run`, write nothing and say what would be cleared, under
`Dry run <today>:`.

## Fix

Clear every stale planned date, blocked and excluded tasks included, and change
nothing else.

## Result

For a job, return these lines, with one `Cleared` line per date cleared:

```
Fixed <today>:
Cleared <id> <title> <url> (was <date>)
```

When there were none, return `Nothing to fix.`; when the task list can't be
read, `Fix-todo-list FAILED: <what went wrong>`. In chat, tell the user the same
in plain words.
