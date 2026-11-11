# Task management rules

## System labels

### `$no-autoschedule`

The user has opted this task out of automatic planning. Planners never pick it,
but once the user dates it themselves, it's reminded about like any other dated
task.

### `$pending-shipment`

Something has been ordered for this task and hasn't arrived, so the user can't
start it. Waiting on an order usually gets this label instead of the blocked
status.

## Databases

### `%Message-rules`: what each reminder's message says

Setup creates it from ntm's template; the user changes it there.

### `%Paused-dates`: days the user doesn't want to autoschedule

The days sit under `## Paused dates`. `ntm:pause` keeps it.

### `%Task-review-log`: what the estimator learns in reviews

The estimator agent keeps it, from what `ntm:review-todo-list` hands it. Setup
creates it from ntm's template.

## Excluded tasks

Labels to exclude from auto-scheduling, in Planning in the `%Settings` document,
lists the labels planners never pick; by default `$no-autoschedule` and
`$pending-shipment`. A task is excluded when it carries one of them, itself or
through its project (see Project labels). A task in the blocked status is always
excluded too; that isn't a setting.

Planning and reminders use `fetch open`, which includes blocked tasks, and keep
excluded tasks in the results.

Planners skip excluded tasks: they never pick or date them. Reminders don't: any
open task the user has dated gets reminded about, excluded or not.

Planners also never plan onto a paused day (`/ntm:pause --check` over the span
says which days are). A date the user set on a paused day stands, and gets its
reminders.

## Planned dates

Planners set, move and clear planned dates freely.

A date is **stale** when it's earlier than today and the task is still open.

## Relationships

How linked tasks limit when a task can be planned. These are the defaults; the
user's Planning settings can change them.

### Blocks and blocked by

A task blocked by open linked tasks can be planned for any day after the planned
days of all those blockers. Never the same day, but not necessarily the next
either: any later day works. A blocker's planned day is its planned date. A
blocker with no planned date, or a stale one, has no planned day, and the tasks
it blocks wait. A planner can date a blocker and then the task it blocks in the
same run.

For example, if task `two` is blocked by task `one`, then `two` can be planned
for Wednesday only if `one` is planned for Tuesday or earlier. If `one` has no
planned day, `two` can't be planned yet.

The user also uses blocked-by loosely, to push one thing behind another; that's
fine, and nothing to question them about.
