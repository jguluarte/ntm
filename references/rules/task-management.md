# Task management rules

## Labels

### `$no-autoschedule`

The user keeps this task out of automatic planning.

### `$pending-shipment`

Something ordered for this task hasn't arrived, so the user can't start it yet.

## Planning

### Labels to exclude from auto-scheduling

A task carrying one of these labels is excluded. They're listed under Planning
in the `%Settings` database: by default `$no-autoschedule` and
`$pending-shipment`, and the user can add their own. A label on a project counts
on every task in it.

### Plannable tasks

Planning picks only plannable tasks: open, not in the blocked status, and not
excluded by a label. Reminders cover every open task planned for the day,
blocked or excluded included.

### Planned dates

A planned date is the day the user means to do the work, and planning sets,
moves and clears it freely. **A planned date is NEVER a deadline.**

### Blocking order

A task waiting on open blockers is planned for a day after all of them. It waits
until each blocker has a planned date. Planning can date a blocker and the task
it blocks in the same run.

For example, if `one` blocks `two` and `one` is planned for Tuesday, `two` can
go on Wednesday or any day after.

The user sometimes blocks a task only to order it behind another. That's fine,
and nothing to ask them about.

## Databases

### `%Message-rules`

What each reminder's message says. The messenger agent follows it, and the user
changes it.

### `%Paused-dates`

The days when nothing gets planned automatically. `ntm:pause` keeps it. Planning
never dates a task on a paused day, but a date the user sets there stands.

### `%Task-review-log`

What reviews have taught about how the user sizes and breaks up tasks. The
estimator agent keeps it, from what `ntm:review-todo-list` sends it.
