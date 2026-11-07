---
name: fix-todo-list
description: Tidies the user's todo list by closing parents whose sub-tickets are all closed and clearing stale planned dates, then returns what it changed. Run by the weekly planning job, or by the user ("fix my todo list", "tidy my todo list").
---

# neurodivergent-task-manager:fix-todo-list

Fixes todo list state that's always safe to fix, and returns what it changed. It
never notifies anyone: whoever called it decides what to tell the user.

## Usage

```
/neurodivergent-task-manager:fix-todo-list [--dry-run]
```

`--dry-run`: report what would change and write nothing; see Failures and dry
runs.

## Setup

1. Load `neurodivergent-task-manager:conventions`.
2. Compute `TODAY` once, as the conventions' Dates section says, and use it for
   the whole run, even if the run crosses midnight.
3. Fetch every open ticket with the guide's `fetch open`, and keep every result,
   including excluded tickets and parents. Skip the parent and blocker reads,
   and skip listing the projects with their labels: these rules check no labels.

## Rules

Apply the rules in order, so a ticket rule 1 closes isn't also cleared by rule 2.

### 1. Close finished parents

```
tickets where status is open
  and it has sub-tickets
  and every sub-ticket is closed (done, canceled or duplicate)
→ set status to done
```

Fetch the closed tickets that have a parent (the guide's `fetch closed`, with
the canceled and duplicate statuses as well as done, keeping those with a parent
id). Check each distinct parent that's among the open tickets: read it with
`read ticket`, and if it's still open, list its sub-tickets with the guide's
`list sub-tickets`. If every one is closed, set the parent to done with
`set status` and change nothing else.

Whenever you close a parent, check its own parent the same way, even if you
already checked it this run, so a chain closes in one run. The list's automation
may close that parent as soon as you close its last sub-ticket; the guide says
whether the backend does that. If `read ticket` shows it's already closed, don't
write it, report it as `Closed` like your own closes, and carry on up the chain
from it. Any other parent found already closed is skipped without a report, and
a parent whose close failed counts as still open.

### 2. Clear stale dates

```
tickets where status is open
  and planned date is not null
  and planned date < TODAY
→ clear planned date
```

Of the open tickets, keep those that match, leaving out any that rule 1 closed
or found already closed. Clear each with the guide's `clear planned date` and
change nothing else.

### Failures and dry runs

Retry a failed read (a Setup fetch or a read in rule 1) once. If it still fails,
stop and return `Fix-todo-list FAILED: <what failed>`. Only if anything was
changed or failed to write before it, add the result as below (never
`Nothing to fix.`). Writes follow the conventions; list any that still fail
under `Couldn't write:`.

With `--dry-run`, make no writes, and treat every parent that would be closed as
closed, both when checking its own parent and in rule 2. In the result, write
`Dry run <TODAY>:` in place of `Fixed <TODAY>:`, and `Would close` and
`Would clear` in place of `Closed` and `Cleared`.

## Result

Return plain text:

- `Fixed <TODAY>:` then one line per change:
  - `Closed <id> <title> <url>`
  - `Cleared <id> <title> <url> (was <date>)`
- `Nothing to fix.` when nothing matched, or `Dry run <TODAY>: nothing to fix.`
  in a dry run. If writes were attempted but all failed, give the header with no
  change lines.
- `Couldn't write:` with any failed writes, only when there are some.
