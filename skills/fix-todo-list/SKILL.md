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
2. Compute `TODAY` once, as the conventions' Dates section says, and use it for
   the whole run.
3. Fetch every open task with `fetch open` from the backend guide (in
   `ntm:conventions`), excluded tasks included. Skip the project list: this
   skill checks no labels.
    - If the fetch fails, retry once. If it fails again, stop and return
      `Fix-todo-list FAILED: <what failed>`.
4. For each fetched task with a planned date before `TODAY`, clear the date with
   the backend guide's `clear planned date` and change nothing else. Failed
   writes follow the conventions' Writing to the todo list section. With
   `--dry-run`, make no writes; only record what would be cleared.

## Result

Return plain text:

- `Fixed <TODAY>:`, then one line per change:
  `Cleared <id> <title> <url> (was <date>)`.
- `Nothing to fix.` when nothing matched.
- `Couldn't write:` with the writes that still failed, only when there are some.

If every write failed, return `Fixed <TODAY>:` with no change lines, then
`Couldn't write:`.

A dry run returns `Dry run <TODAY>:` in place of `Fixed <TODAY>:`, `Would clear`
in place of `Cleared`, and `Dry run <TODAY>: nothing to fix.` in place of
`Nothing to fix.`
