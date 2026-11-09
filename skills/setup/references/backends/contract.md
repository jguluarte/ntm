# Backend contract

How an agent queries the user's todo list, whatever backend holds it. Their
`ntm-user:backend` is written against this file: for each piece below, the tool
call that does it, what goes in and what comes back. `linear.md` is the tested
guide for Linear. For any other backend, setup writes one with the user from
this file, and `/ntm:self-test` checks it. A backend can be anything the agent
can reach, such as a table in a Claude Doc. Keep the headings: skills cite them.

## What the backend needs to have

A connector the agent can use to list, read and write tasks. Each task has an
id, title, description, status, labels, a parent, a web url, and one date field
to use as the planned date. Tasks group into projects (or folders, epics),
ideally ones that carry labels.

Two gaps are fatal until setup covers them with the user: no planned date field,
and no way to tell open tasks from closed. The rest are survivable; the guide
names the ones its backend has, and skills work around them:

- **No estimate field:** the estimate goes in the description, on a line
  `Estimate: <estimate>`; `fetch open` reads it there, `update task` writes it.
- **No blocked-by relation:** review and planning go by titles and descriptions.
- **No labels on groups:** no project-label inheritance; system labels go on
  tasks.
- **No priority or updated-at:** skills do without.
- **No documents:** databases live in tasks (see Databases).
- **No databases inside a project:** every database is at list level.

## Todo list

The todo list's name (List name) and the id calls take (List id). With no unit
above projects, the todo list is the whole account: List name is what the
backend calls it, List id is blank. Task ids are the backend's own, whatever
their shape (`(ABC-12)` in the conventions). Say whether the backend can close a
parent once its sub-tasks are all done, and if so whether the user wants it to.

## Status classes

Which of the user's statuses fall in each class (plannable, started, blocked,
done, canceled, duplicate), in their words, and how to filter by class, write a
status and tell open from closed in results. With only open and closed, open is
plannable, closed is done, and `set status` to done closes the task.

## Operations

What base skills call, by these names.

### `ping`

One read that proves the connector works and sees the todo list. Returns pass,
or which of the failures `ntm:ready-check` reports: sign-in expired, wrong
account or backend error.

### `fetch open`

Every open task (plannable, plus blocked where the list has it), paginated, with
the standard fields: id, title, url, status, status class, priority (which value
is highest, which is none), estimate, planned date, labels, project, parent id,
completed at and updated at. Also every project with its name and labels, and
its summary on request.

### `fetch closed`

Closed tasks (done; canceled and duplicate on request) with their completion
time, limited on request to a span and to one label.

### `read task`

One task by id, with its description and blocked-by relations.

### `read comments` / `write comment` / `update comment`

A task's comments, read, added or edited. With no edit in place,
`update comment` deletes and re-adds, or appends.

### `set planned date` / `clear planned date`

Sets or clears the planned date field, and nothing else.

### `set status`

Sets a status in a given class (see Status classes).

### `add labels` / `remove labels`

Adds or removes labels, keeping the others.

### `mark duplicate of`

Links a task as a duplicate of another. With no such relation, closes it in the
duplicate status with a comment naming the original.

### `create task`

Takes a title, description, project, parent, blocked-by and labels; returns the
new task's id and url. Says how to check for an existing match first.

### `update task`

Changes the title, description, estimate or project (or removes the project), or
adds a blocked-by link, and nothing else.

### `read database` / `write database`

See Databases.

## Databases

The system's own records, each a document on the todo list under the title the
conventions give it. `read database <title>` returns its content or says it's
missing; `write database <title>` replaces the content, creating the database if
it's missing. Both take an optional project, for one kept in a project.

With no documents, each database is the description of an open task in a
plannable status with no planned date, titled with the database's title, labeled
$no-autoschedule (its real name from Labels), and in its project if it has one.
`ntm:fix-todo-list` leaves it alone; planners skip it for its label, and skills
don't treat it as work. A read finds it by title; a write replaces its
description, creating the task if needed.

## Setup operations

Used by `ntm:configure-todo-list`, in the same form as Operations.

### `list todo-lists`

The todo lists the connector sees, by name and id, or that the backend has none
to list (the user names theirs, or setup runs `create todo-list`).

### `create todo-list`

Only where there are none to list: makes one with the statuses, labels and
databases settled so far, and returns its id.

### `list statuses`

A todo list's status names, to match each class to.

### `sample estimates`

Only where estimates use a scale of the backend's own: estimates already set on
some tasks, to suggest the scale when the user doesn't know it.

### `list labels`

The task labels, and the project labels when those are a separate set.

### `create label`

Takes a name, a description and which set; makes a task label, or a project
label where those are a separate set.

### `list projects`

Every project with its name, id and labels.

### `create project`

Takes a name and the project labels it carries; makes the project.

### `create database`

Takes a title, first content and optional project; makes the database, leaving
one that exists alone (`read database` first). The message history database's
first content is its frontmatter, which holds its `Keep:` line.

## Writing

Say how a write reports success, so the conventions' retry rule (retry once,
then report) can be applied.

## Setting something up with the user

How `ntm:configure-todo-list` writes the guide with the user: walk this file
with them, heading by heading, naming the tool and parameters for each
operation. Once they name the tool for `ping`, confirm the connector as the
skill says. Read each tool's schema from ToolSearch rather than guessing: the
date field, pagination, whether labels add or replace, whether a comment edits
in place. Where a choice is theirs (which date field, which grouping is a
project), propose one and let them react. Try a read by hand where it's cheap;
writes other than the setup operations wait for `/ntm:self-test`.

Name the gaps their backend has. For a fatal one, look with them for a cover: a
field or status to repurpose, a label, or another place for the list, such as a
table in a Claude Doc. With no documents, tell them databases live in tasks (see
Databases).
