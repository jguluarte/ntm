---
name: cleanup
description: Tidies the user's nudge board by closing parents whose sub-tickets are all closed and clearing stale planned dates, then returns what it changed. Run by the weekly cleanup job, or by the user ("clean up the board", "tidy my board").
---

# nudge:cleanup

Fixes board state that's always safe to fix, and returns what it changed. It never notifies anyone: whoever called it decides what to tell the user.

## Usage

```
/nudge:cleanup
```

## Setup

1. Load `nudge:board`.
2. Compute `TODAY` once, as the board rules' Dates section says, and use it for the whole run, even if the run crosses midnight.
3. Fetch every open ticket with the adapter's `fetch open`, and keep every result, including excluded tickets and containers. Skip the Scheduling fetch's other steps, and skip listing the projects with their labels: the only label these rules check is the `deadline label`, and the board rules put it on a ticket, never a project.

## Rules

Apply the rules in order, so a ticket rule 1 closes isn't also cleared by rule 2.

### 1. Close finished parents

```
tickets where status is open
  and it has sub-tickets
  and every sub-ticket is closed (done, canceled or duplicate)
→ set status to done
```

Fetch the closed tickets that have a parent (the adapter's `fetch closed`, with the canceled and duplicate statuses as well as done, keeping those with a parent id). Check each distinct parent that's among the open tickets: read it with `read ticket`, and if it's still open, list its sub-tickets with the adapter's `list sub-tickets`; if every one is closed, set the parent to done with `set status` and change nothing else. This includes tickets with the `deadline label`.

Whenever you close a parent, check its own parent the same way, even if you already checked it this run, so a chain closes in one run. The board's automation may close that parent as soon as you close its last sub-ticket (the adapter says whether the tracker does that): if `read ticket` shows it's already closed, don't write it, report it as `Closed` like your own closes, and carry on up the chain from it. Any other parent found already closed is skipped without a report, and a parent whose close failed counts as still open.

### 2. Clear stale dates

```
tickets where status is open
  and labels does not contain the deadline label
  and planned date is not null
  and planned date < TODAY
→ clear planned date
```

Of the open tickets, keep those that match, leaving out any that rule 1 closed or found already closed. Clear each with the adapter's `clear planned date` and change nothing else.

### Failures and dry runs

Retry a failed read (a Setup fetch or a read in rule 1) once. If it still fails, stop and return `Cleanup FAILED: <what failed>`, then, only if anything was changed or failed to write before it, the result as below (never `Nothing to clean up.`). Writes follow the board rules; list any that still fail under `Couldn't write:`.

If the caller asks for a dry run, make no writes, and treat every parent that would be closed as closed, both when checking its own parent and in rule 2. In the result, write `Dry run <TODAY>:` in place of `Cleaned up <TODAY>:`, and `Would close` and `Would clear` in place of `Closed` and `Cleared`.

## Result

Return plain text:

- `Cleaned up <TODAY>:` then one line per change:
  - `Closed <ID> <title> <url>`
  - `Cleared <ID> <title> <url> (was <date>)`
- `Nothing to clean up.` when nothing matched, or `Dry run <TODAY>: nothing to clean up.` in a dry run. If writes were attempted but all failed, give the header with no change lines.
- `Couldn't write:` with any failed writes, only when there are some.
