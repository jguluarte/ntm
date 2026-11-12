# Task management conventions

## Labels

### `$no-autoschedule`

The user keeps this task out of automatic planning.

### `$pending-shipment`

Something ordered for this task hasn't arrived, so the user can't start it yet.

## Planning

### Labels to exclude from auto-scheduling

A task carrying one of these labels is excluded. They're listed under Planning
in the `%Settings` database: by default `$no-autoschedule` and
`$pending-shipment`, and the user can add their own.

### Plannable tasks

Planning picks only plannable tasks: open, not in the blocked status, and not
excluded by a label. Reminders cover every task planned for the day, open and
done, blocked or excluded included.

### Blocking order

A task waiting on open blockers is picked for a day after all of them. A task
whose blocker has no planned date gets none either. Planning can date a blocker
and the task it blocks in the same run.

The user sometimes blocks a task only to order it behind another. Don't ask them
about it.

## Databases

### `%Message-rules`

What each reminder's message says. The messenger agent follows it, and the user
changes it.

### `%Paused-dates`

The days that get nothing new planned automatically. `ntm:pause` maintains it.
Planning never automatically picks a task for a paused day.

### `%Estimator-log`

What reviews have taught about how the user sizes and breaks up tasks. The
estimator agent keeps it, from what `ntm:review-task-list` sends it.
