# Backend contract

What a backend has to have, and what its guide has to say, for ntm to run on it.
A backend guide maps each operation the conventions name onto one backend's
connector; `linear.md` is the complete, tested one. Any other backend has no
guide file: the user's own description under Todo list in `ntm-user:settings` is
its guide. `/ntm:configure-todo-list` writes that description with the user by
walking this contract, and once `ntm-user` is installed, `/ntm:self-test` checks
it. A backend can be built on anything the user's agent can reach, for example a
table in a Claude Doc (the Claude Docs connector's own guide gives its calls).

Write a guide as a list of operations, each saying which tool calls carry it out
and which fields map to the conventions' names. Keep the headings below so
skills can find what they need.

## What the backend needs to have

- Tasks with: an id, a title, a description, a status, labels, a single date
  field usable as the planned date, a parent/sub-task relation, and a web url.
- Some way to group tasks (projects, folders, epics), ideally one that can carry
  labels.
- A connector for Claude that can list, read and write the above.

Two gaps are fatal: a backend with no date field to use as the planned date, or
no way to tell open tasks from closed, can't run this system.

Other gaps are survivable. The guide says which the backend lacks, and the
skills work around them:

- **No estimate field:** keep each task's estimate in its description, on a line
  `Estimate: <estimate>`. The guide says how `fetch open` and `list sub-tasks`
  read it there and how `update task` writes it.
- **No blocked-by relation:** reviewing and planning work from titles and
  descriptions instead.
- **No labels on groups:** the conventions' project-label inheritance doesn't
  apply, and the user puts system labels on tasks directly.
- **No priority, or no updated-at:** skills do without them.
- **No documents:** databases are kept in tasks (see Databases).
- **No way to keep a database inside a project:** every database is at list
  level.

## Todo list

Name the todo list (List name in Todo list), what id it needs (List id), and
which automations the backend runs on parent/sub-task closing, if any. If the
backend has no unit above projects, the todo list is the whole account (List
name is what the backend calls it, List id blank). If ids carry no prefix, Task
prefix is blank and ids are the backend's own; `(ABC-12)` in the conventions
then means the bare id.

## Status classes

Say how the status names in Todo list are used to filter and to write, and how
to tell open from closed in results. A backend with no status names, only open
and closed, lists `open` as the one plannable status, `closed` as done, and
leaves started, blocked, canceled and duplicate blank. The classes those lines
name then don't exist on this todo list, and `set status` to done closes the
task.

## Operations

Cover every operation: the guide's entry for each says what's under its heading
here. Skills call operations by these names; keep them exactly.

### `ping`

Makes one read that proves the connector works and sees the todo list named in
Todo list. Says how to tell sign-in expired from wrong account from backend
error (the names `ntm:ready-check` reports).

### `fetch open`

Gets every open task (every plannable status, plus blocked when Todo list's
blocked line isn't blank) with the standard fields, paginated, plus every
project with its name and labels, and its summary when a skill asks for it.

The standard fields are id, title, url (the task's link), status, status class,
priority, estimate, planned date, labels, project, parent id, completed at and
updated at. For priority, the entry says which value is highest and which means
none.

### `fetch closed`

Gets closed tasks (done; canceled and duplicate on request) with their
completion time, and says how to limit them to a span and to one label.

### `read task`

Reads one task with its description, parent and blocked-by relations.

### `list sub-tasks`

Lists a task's sub-tasks, open and closed, with the standard fields (see
`fetch open`).

### `read comments` / `write comment` / `update comment`

Reads, writes and updates a task's comments. If the backend can't update a
comment in place, `update comment` says to delete and re-add, or to append.

### `set planned date` / `clear planned date`

Sets or clears a task's planned date. Names the date field used; nothing else
changes.

### `set status`

Sets a task's status, by its name in Todo list.

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

Changes a task's title, description, estimate, project (or none) or parent, or
adds a blocked-by link; nothing else changes.

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
plannable status. `ntm:fix-todo-list` never touches it (no sub-tasks, no date)
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
message history database's first content is its `Keep:` line.

## Writing

Say how a write reports success, so the conventions' retry rule (retry once,
then report) can be applied.
