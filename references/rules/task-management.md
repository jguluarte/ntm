# Task management rules

How ntm plans the user's task list when they use task management: which tasks
planning picks, the order it plans them in, and the labels and databases the
feature uses.

## Labels

### `$no-autoschedule`

The user keeps this task out of automatic planning. Planning never picks it, but
a date the user sets on it themselves gets reminders like any other.

### `$pending-shipment`

Something ordered for this task hasn't arrived, so the user can't start it yet.
Planning leaves it alone until the label comes off.

### Labels to exclude from auto-scheduling

Planning never picks a task carrying one of these labels. They're listed under
Planning in the `%Settings` database: by default `$no-autoschedule` and
`$pending-shipment`, and the user can add their own. A label on a project counts
on every task in it.

## Planning

### Plannable tasks

Planning picks only plannable tasks: open, not blocked, and not excluded by a
label. Reminders cover every open task planned for the day, whatever its labels
or status.

### Planned dates

A planned date is the day the user means to do the work, and planning sets,
moves and clears it freely. **A planned date is NEVER a deadline.**

### Blocking order

When one task blocks another, the waiting task is planned for a day after every
one of its open blockers: any later day, never the same one. Until each blocker
has a planned date, today or later, the waiting task isn't planned. Planning can
date a blocker and the task it blocks in the same run.

For example, if `one` blocks `two` and `one` is planned for Tuesday, `two` can
go on Wednesday or any day after.

The user also uses blocking to put one thing after another. That's fine, and
nothing to ask them about.

## Databases

### `%Message-rules`

What each reminder's message says. The messenger agent follows it, and the user
changes it.

### `%Paused-dates`

The days when nothing gets planned automatically. `ntm:pause` keeps it. Planning
never dates a task on a paused day, but a date the user sets there stands and
gets its reminders.

### `%Task-review-log`

What reviews have taught about how the user sizes and breaks up tasks. The
estimator agent keeps it, from what `ntm:review-todo-list` sends it.
