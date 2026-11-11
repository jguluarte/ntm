# How ntm uses Linear

ntm works on a task list: it reads your tasks, creates new ones, edits them and
closes them. We keep ours in Linear. Each part below says what ntm needs, then
how we did it in Linear. It's our setup, told so yours can differ.

## Names

ntm writes a label's name with a `$` in front, such as `$price-watch`, and a
database's with a `%`, such as `%Settings`. The mark isn't part of the name.
Setup records the real names in `ntm-user:backend`, which every skill loads, so
yours can be anything.

| In ntm                | Our name in Linear   |
| --------------------- | -------------------- |
| `$no-autoschedule`    | `no-autoschedule`    |
| `$pending-shipment`   | `pending-shipment`   |
| `$price-watch`        | `price-watch`        |
| `$has-amazon-alert`   | `has-amazon-alert`   |
| `$amazon-unavailable` | `amazon-unavailable` |
| `%Settings`           | `Settings`           |
| `%Message-rules`      | `Message-rules`      |
| `%Message-history`    | `Message-history`    |
| `%Paused-dates`       | `Paused-dates`       |
| `%Task-review-log`    | `Task-review-log`    |
| `%Theme`              | `Theme`              |

These are the names the plugin's author uses; the marks keep the plugin's files
consistent and still leave you free to name yours differently.

## The task list

ntm needs one place that holds every task. Each task has an id you can read, a
title, a description, a link that opens it, and a status. ntm reads every open
task at once, and for reports, the tasks closed over a span of days, with when
each one closed.

Our task list is a Linear team. The team's key starts every task's id, `HOME` in
`HOME-12`; we picked one we're happy to read in reminders.

## Status groups

ntm never cares what a status is called, only which group it's in. Linear
already sorts every status into a type, so we read the type and ignore the name,
except one: a status we added and named Blocked.

| Group     | The task is                                   | In Linear                          |
| --------- | --------------------------------------------- | ---------------------------------- |
| Plannable | open, not blocked, not excluded by a label    | backlog, unstarted or started      |
| Started   | plannable, and work on it has begun           | started                            |
| Blocked   | open, but you can't move it right now         | the status named Blocked, any type |
| Done      | finished                                      | completed                          |
| Canceled  | closed without being done                     | canceled                           |
| Duplicate | the same as another; only the original counts | duplicate                          |

Planning picks plannable tasks, reminders cover every open task planned for the
day, and reports count what's done. Duplicate is a group of its own: review
merges a duplicate into the task it copies, and reports list duplicates apart
from canceled tasks.

## The planned date

ntm plans with one date on each task: the day the work is planned for. Planning
sets it, moves it and clears it freely, and reminders read it to say what's on
today.

**NEVER treat a planned date as a deadline.**

We plan with Linear's due date. To us it means the day we mean to do the work,
so a day that passes costs nothing.

A planned date before today, on a task that's still open, is "stale". ntm either
carries the work to today or clears the date.

## Projects and labels

Projects group tasks, such as a kitchen remodel or a catch-all for errands.
Labels mark tasks for ntm: `$no-autoschedule` keeps a task out of planning, and
so does any label you choose to exclude. Each feature's rules name the labels it
uses. Any other label is your own. A label on a project counts on every task in
it, so `$price-watch` on a project watches everything in it.

We use Linear's projects and issue labels. Linear keeps a project's labels as a
separate set, so we match the two by name: for `$price-watch` to count on a
project, the project carries a project label with the same name.

## Sub-tasks and blocking

A task can hold sub-tasks; a review splits a big task into smaller ones under
it. One task can block another, and the waiting one is planned for a day after
all of its blockers.

In Linear these are sub-issues and blocked-by links. A blocked-by link isn't the
Blocked group: a task can wait on another and still be plannable.

## Comments and estimates

Comments hold what's added to a task over time, such as why it's blocked or the
stores the price watch last checked. ntm reads them, and adds and updates its
own. We use Linear's comments as they are.

An estimate is the last line of a task's description, in full words:
`Estimate: 2 hours`. Linear has an estimate field of its own; we leave it empty,
and the line in the description is the estimate.

## Databases

ntm keeps its records in databases, such as `%Settings` and `%Message-rules`. A
database is a page of text, found by its title, that ntm reads whole and saves
back with its changes.

Ours are Linear documents, so everything ntm knows sits beside the tasks. Most
live in the team; a database can belong to a project, kept in its documents.

## Connecting Linear

In Claude's settings, on the Connectors tab, we added Linear and signed in to
the workspace that holds the team. `ntm-user` bundles the same connector, from
`linear-mcp.json` beside this file, and asks for its own sign-in the first time.
From there, the connector's own tool descriptions say how to make each call.

One read of the team proves the connection works. `ntm:ready-check` makes that
read before every job.

## Making your own

None of this is required. It's what worked for us in Linear. If your tasks live
somewhere else, or you'd arrange Linear differently, work out with your agent
what plays each part: the list, the groups, the planned date, the labels, the
databases. Setup records your answers in `ntm-user:backend`, and
`/ntm:self-test` shows whether they hold. The choices are yours.
