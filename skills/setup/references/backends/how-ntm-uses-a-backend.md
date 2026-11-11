# How ntm uses a backend

The backend is the system that holds the user's tasks: Linear, or any tool their
agent can reach. This file describes, in plain ideas rather than calls, what ntm
does with it. Setup reads it to connect a backend, and writes how each idea is
done there into `ntm-user:backend`, which every skill loads.

## Tasks and their states

ntm works on one task list: the place that holds all of the user's tasks,
whatever the backend calls it. Each task has an id the user can read, such as
`ABC-12`, a title, a description, a link that opens it, and a status. ntm
usually reads every open task at once; for reports, it reads the tasks closed
over a span of days, with when each one closed.

ntm never cares what a status is called, only which group it's in:

| Group     | The task is                                    |
| --------- | ---------------------------------------------- |
| Plannable | open and not started, such as backlog or to do |
| Started   | in progress: work on it has begun              |
| Blocked   | open, but the user can't move it right now     |
| Done      | finished                                       |
| Canceled  | closed without being done                      |
| Duplicate | the same as another; only the original counts  |

A task is open until it's done, canceled or duplicate, so a blocked task is
still open. Planning picks only plannable and started tasks, reminders cover
every open task planned for the day, and reports count what's done.

## Planning

A task has one date that ntm uses: the day the work is planned for. It's never a
deadline, and a day passing with the work undone costs nothing. Planning sets
it, moves it and clears it freely, and reminders read it to say what's on today.

A planned date before today, on a task that's still open, is stale. ntm finds
stale dates and either carries the work to today or clears the date.

## Organizing

Projects group tasks, such as a kitchen remodel, or a catch-all for errands.

Labels mark tasks for ntm. A label written with a `$`, such as
`$no-autoschedule`, is one ntm acts on: that one keeps a task out of planning.
Each feature's rules name the labels it uses, and setup records each one's real
name on the task list. A label on a project counts on every task in it, so
`$price-watch` on a project watches everything in it. Any other label is the
user's own category.

A parent task holds sub-tasks; a review splits a big task into smaller ones
under it. One task can block another: the blocked one is planned for a day after
all of its blockers. That link isn't the Blocked group: a task can wait on
another and still be plannable.

## Notes

Comments on a task hold what's added over time, such as why it's blocked or the
stores the price watch last checked. ntm reads them, and adds and updates its
own.

A task's estimate is the last line of its description, in full words:
`Estimate: 2 hours`. It lives there on every backend, whatever estimate field
the backend has of its own.

## ntm's own records

ntm keeps its records in databases: documents written with a `%`, such as
`%Settings` and `%Message-rules`, each found by its title. ntm reads one and
saves it back with its changes. Ideally the backend holds them beside the tasks,
so everything ntm knows lives in one place. A database can belong to a project:
`%Price-watch-stores` sits in the price watch project. `ntm-user:backend`
records where each one is.

## Connecting another backend

The agent running setup reads this file and the user's own tools for their
backend. It maps each idea above onto those tools with the user, and writes how
into `ntm-user:backend`: which statuses are in which group, which date field is
the planned date, what counts as a project, where the databases live. Where the
choice is the user's, it proposes one and lets them decide. Nothing lists every
call: the tools' own descriptions say how to make them.

ntm needs at least a date to plan with and a way to tell open tasks from closed.
It also needs one quick read that proves the task list answers, which
`ntm:ready-check` runs before every job. Once `ntm-user` is installed,
`/ntm:self-test` tries the whole mapping on a throwaway task and database.

## With Linear

Linear is the backend ntm suggests; a free account is enough. A Linear team is
the task list, and the team's key starts every task's id: `HOME` in `HOME-12`.

| Idea         | In Linear                                                    |
| ------------ | ------------------------------------------------------------ |
| Planned date | the due date                                                 |
| Status group | the workflow state's type; a status named Blocked is blocked |
| Labels       | issue labels; on a project, project labels of the same names |
| Databases    | documents in the team, or in a project                       |

Projects, comments, sub-issues and blocking go by the same names in Linear. The
user's Linear tools do the rest: their descriptions say how to make each call.

To connect it, in Claude's settings, on the Connectors tab, add Linear and sign
in to the workspace that holds the team. `ntm-user` bundles the same connector,
from `linear-mcp.json` beside this file, and it asks for its own sign-in the
first time.
