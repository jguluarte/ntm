---
name: fix-todo-list
description: >-
    Tidies the user's todo list by clearing stale planned dates, then returns
    what it changed. Run by the weekly planning job, or by the user ("fix my
    todo list", "tidy my todo list").
---

# ntm:fix-todo-list

Clears stale planned dates and returns what it changed. It never notifies
anyone; the caller decides what to tell the user.

## Usage

```
/ntm:fix-todo-list [--dry-run]
```

`--dry-run` reports what would be cleared and writes nothing.

## Steps

1. Load `ntm:conventions`.
2. Compute `TODAY` once, as its Dates section says, and use it for the whole
   run.
3. Fetch every open task with the guide's `fetch open`, excluded tasks included.
   Skip the blocker reads and the project list: this skill checks no labels. If
   the fetch fails, retry once; if it fails again, stop and return
   `Fix-todo-list FAILED: <what failed>`.
4. For each task planned before `TODAY`, clear the date with the guide's
   `clear planned date` and change nothing else. Failed writes follow the
   conventions' Writing to the todo list section.

## Result

Return plain text:

- `Fixed <TODAY>:`, then one line per change:
  `Cleared <id> <title> <url> (was <date>)`. If every write failed, the header
  alone.
- `Nothing to fix.` when nothing matched.
- `Couldn't write:` with the writes that still failed, only when there are some.

A dry run returns `Dry run <TODAY>:` in place of `Fixed <TODAY>:`, `Would clear`
in place of `Cleared`, and `Dry run <TODAY>: nothing to fix.` in place of
`Nothing to fix.`
