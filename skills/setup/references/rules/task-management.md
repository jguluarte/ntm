# Task management rules

## System labels

- **$no-autoschedule:** the user has opted this task out of automatic planning.
  Planners never pick it, but once the user dates it themselves, it's reminded
  about like any other dated task.
- **$pending-shipment:** something has been ordered for this task and hasn't
  arrived, so the user can't start it.

## Databases

- **pauses** (`Pauses`): the pause schedule, under `## Pauses`. `ntm:pause`
  keeps it.
- **task review log** (`Task review log`): `ntm:review-todo-list` keeps it, and
  hands the estimator what it needs from it.

## Excluded tasks

Excluded labels from automatic scheduling, in Planning in your settings, lists
the labels planners never pick; by default $no-autoschedule and
$pending-shipment. A task is excluded when it carries one of them, itself or
through its project (see Project labels). A task in the blocked status is always
excluded too; that isn't a setting.

Planners skip excluded tasks: they never pick or date them. Reminders don't: any
open task the user has dated gets reminded about, excluded or not.

Planners also never plan onto a paused day (`/ntm:pause --check` over the span
says which days are). A date the user set on a paused day stands, and gets its
reminders.

## Planned dates

Planners set, move and clear planned dates freely.

A date is **stale** when it's earlier than today and the task is still open.

## Relationships

How each relation affects planning. Planning in your settings can say otherwise;
these are the defaults.

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
