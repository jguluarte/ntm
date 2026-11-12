# Terminology

The words ntm's skills and agents share.

## Task list

The one place that holds every task, on the user's backend. The user may call it
their todo list.

## Task

One thing on the task list, with an id, a title, a description, a link and a
status. Its id is the backend's own, such as `ABC-12`.

## Project

A group of tasks, such as a kitchen remodel or a catch-all for errands. A label
on a project counts on every task in it.

## Label

A tag on a task or a project. A label ntm uses is written with a `$`, such as
`$price-watch`; the `$` isn't part of the name, and `%Settings` gives the real
one, under Labels. Any other label is the user's own.

## Planned date

The day a task's work is planned for. Planning sets and moves it, and clears it
only when the user agrees. A planned date before today, on a task that's still
open, is "stale".

## Status groups

Each status on the task list belongs to one group, and ntm goes by the group. A
task is open until it's done, canceled or a duplicate.

| Group     | The task is                                   |
| --------- | --------------------------------------------- |
| Plannable | open, not blocked and not excluded            |
| Started   | plannable, and work on it has begun           |
| Blocked   | open, but the user can't move it right now    |
| Done      | finished                                      |
| Canceled  | closed without being done                     |
| Duplicate | the same as another; only the original counts |

A task is excluded when it carries a label `%Settings` keeps out of planning:
`$no-autoschedule` and `$pending-shipment` by default.

## Estimate

How big a task is, in hours unless `%Settings` says otherwise, in full words on
the last line of its description: `Estimate: 2 hours`.

## Database

A page of text beside the tasks where ntm keeps a record, found by its title,
read whole and saved back with its changes. A database is written with a `%`,
such as `%Settings`; the `%` isn't part of the title, and `ntm-user:backend`
says where each one lives.

## Job

A scheduled run of ntm skills, in order, such as the morning reminder. No one is
in the chat while it runs.

## The user plugin

`ntm-user`, the plugin setup builds for one user: `ntm-user:backend` and
`ntm-user:notify`.

## Theme

What the user's reminders are written in: something they enjoy, such as a show.
It lives in `%Theme`.
