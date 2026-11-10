---
name: fix-todo-list
description: >-
    Tidies the user's task list by clearing stale planned dates, and returns
    what it changed. Run by a job, or by the user ("fix my todo list", "tidy my
    todo list").
---

# ntm:fix-todo-list

Clears every stale planned date, one before today on a task that's still open,
and returns what it changed.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## Usage

```
/ntm:fix-todo-list [--dry-run]
```

`--dry-run`: report what would be cleared, and write nothing.

## Fix

### 1. Find the stale dates

Find every open task with a stale planned date, blocked and excluded tasks
included.

### 2. Clear them

Clear each one's planned date, and change nothing else. With `--dry-run`, skip
this step.

## Result

Return plain text:

| Lines                                                                             | When                         |
| --------------------------------------------------------------------------------- | ---------------------------- |
| `Fixed <today>:`, then `Cleared <id> <title> <url> (was <date>)` per date cleared | there were stale dates       |
| `Couldn't write:`, then `<id> <title> <url> (was <date>)` per date not cleared    | after those, when any failed |
| `Nothing to fix.`                                                                 | there were none              |
| `Fix-todo-list FAILED: <what went wrong>`                                         | the task list can't be read  |

In a dry run, `Dry run <today>:` takes the place of `Fixed <today>:`,
`Would clear` of `Cleared`, and `Dry run <today>: nothing to fix.` of
`Nothing to fix.`
