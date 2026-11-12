---
name: fix-task-list
description: >-
    Tidies the user's task list by clearing stale planned dates and removing
    pauses that have ended, and returns what it changed. Run by a job, or by the
    user ("fix my todo list", "tidy my todo list").
---

# ntm:fix-task-list

Cleans up stale information in the backend.

## Usage

```
/ntm:fix-task-list [--dry-run]
```

With `--dry-run`, write nothing and say what would change, under
`Dry run <today>:`.

## Fix

Load `ntm-user:backend`, and then find all non-closed tasks which have a planned
date in the past.

**If this is not a `--dry-run`**, clear the date on all of those tasks.

If `ntm-user:backend` lists a `%Paused-dates`, find the pauses in it that have
ended. **If this is not a `--dry-run`**, remove them, keeping the list as
`ntm:pause` does.

## Result

For a job, return these lines, with one `Cleared` line per date cleared and one
`Removed` line per pause removed:

```
Fixed <today>:
Cleared <id> <title> <url> (was <date>)
Removed pause <pause, as the list had it>
```

When there were none, return `Nothing to fix.`; when the task list can't be
read, `Fix-task-list FAILED: <what went wrong>`. In chat, tell the user the same
in plain words.
