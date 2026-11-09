---
name: fix-todo-list
description: >-
    Tidies the user's todo list by clearing stale planned dates, then returns
    what it changed. Run by the bulk planning job, or by the user ("fix my todo
    list", "tidy my todo list").
---

# ntm:fix-todo-list

Clears planned dates that have gone stale, and returns what it changed. It never
notifies anyone: whoever called it decides what to tell the user.

## Usage

```
/ntm:fix-todo-list [--dry-run]
```

`--dry-run`: report what would be cleared and write nothing.

## Setup

```
/ntm-user:backend find every open item, excluded ones included.
```

## Clear stale dates

```
tasks where status is open
  and planned date is not null
  and planned date < today
→ clear planned date
```

Clear each match's planned date as `ntm-user:backend` says, and change nothing
else.

### Failures and dry runs

Retry a failed fetch once. If it still fails, or `ntm-user:backend` says
`Backend CAN'T: <why>`, stop and return `Fix-todo-list FAILED: <what failed>`.
Retry a failed write once, and list any that still fail under `Couldn't write:`.

With `--dry-run`, make no writes. In the result, write `Dry run <today>:` in
place of `Fixed <today>:`, and `Would clear` in place of `Cleared`.

## Result

Return plain text:

- `Fixed <today>:` then one line per change:
  `Cleared <id> <title> <url> (was <date>)`
- `Nothing to fix.` when nothing matched, or `Dry run <today>: nothing to fix.`
  in a dry run. If writes were attempted but all failed, give the header with no
  change lines.
- `Couldn't write:` with any failed writes, only when there are some.
