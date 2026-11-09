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

Skills call these by name; keep the names exactly. For each, the guide gives the
call, what goes in and what comes back.

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

Reads, writes and updates a task's comments. If the backend can't update a
comment in place, `update comment` says to delete and re-add, or to append.

### `set planned date` / `clear planned date`

Sets or clears a task's planned date. Names the date field used; nothing else
changes.

### `set status`

Sets a task's status to one in a given class, as Status classes says.

### `add labels` / `remove labels`

Adds or removes labels without dropping the others.

### `mark duplicate of`

Marks a task as a duplicate of another with the backend's duplicate relation.
With no such relation, closes it with the duplicate status and a comment naming
the original.

### `create task`

Creates a task with a title, description, project, parent, blocked-by and
labels, and says how to check for an existing match first.

### `update task`

Changes a task's title, description, estimate or project (or removes the
project), or adds a blocked-by link; nothing else changes.

### `read database` / `write database`

Reads or writes a database, as Databases says. `write database` creates a
missing database with the content given.

## Databases

Databases are the documents the system keeps its own records in, on the todo
list, each under the title the conventions give it. `read database <title>`
returns its content, or says it's missing. `write database <title>` replaces the
content, and creates a missing database with the content given. Both take an
optional project, for a database kept in a project.

If the backend has documents, use them, found by title. If it doesn't, keep each
database in the description of a task titled with the database's title, labeled
with the $no-autoschedule label (its real name from Labels) and left open in a
plannable status. `ntm:fix-todo-list` never touches it (it has no planned date)
and planners skip it for its label. `read database` is then a title search that
reads that task's description; `write database` replaces the description,
creating the task when there is none. A database kept in a project is a task
created in that project. The conventions say every skill ignores such a task as
work.

## Setup operations

Used by `ntm:configure-todo-list`. For each, say which call does it and what's
under its heading here.

### `list todo-lists`

Lists the todo lists the connector can see, by name and id. Where the backend
has no todo lists to list, says so (the user names or pastes theirs, or
`ntm:configure-todo-list` runs `create todo-list`).

### `create todo-list`

Only where the backend has no todo lists to list: makes one with the statuses,
labels and databases settled so far, and returns its id.

### `list statuses`

Lists a todo list's status names, so each class can be matched to real names.

### `sample estimates`

Only where the backend stores estimates on a scale of its own: reads the
estimates already set on some of the list's tasks, so the backend's scale can be
suggested when the user doesn't know it.

### `list labels`

Lists the todo list's task labels, and its project labels when those are a
separate set.

### `create label`

Creates a task label by name, with a description, and a project label by name
when those are a separate set.

### `list projects`

Lists every project with its name, id and labels.

### `create project`

Creates a project by name, with the project labels it should carry.

### `create database`

Creates a database with a given title and first content, at list level or in a
project, without touching one that already exists (`read database` first). The
message history database's first content is its frontmatter, which holds its
`Keep:` line.

## Writing

Say how a write reports success, so the conventions' retry rule (retry once,
then report) can be applied.

## Setting something up with the user

How `ntm:configure-todo-list` writes the description with the user. Walk this
contract with them, heading by heading, in its order. For each operation, name
the tool and the parameters that carry it out. Once they name the tool for
`ping`, confirm the connector as the skill says. Read the tool's schema from the
ToolSearch result rather than guessing: which date field is the planned date,
how results paginate, whether labels add or replace, whether a comment can be
edited in place. Where a choice is theirs (which date field, which grouping is a
project), propose one and let them react. Try a read by hand where it's cheap.
Writes other than the setup operations wait for `/ntm:self-test`.

Say which of the gaps under What the backend needs to have the backend has. For
no date field, or no way to tell open from closed, look with them for something
that covers it: a field or status they can repurpose, a label, or a different
place to keep the list, such as a table in a Claude Doc. Carry on once it's
covered. With no documents, each database lives in the description of an open
task titled with the database's title, as Databases says; tell them.
