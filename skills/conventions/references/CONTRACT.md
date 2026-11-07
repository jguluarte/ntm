# Backend contract

A backend guide maps the operations the conventions name onto one backend's
connector. `linear.md` is the complete, tested one. For any other backend, Todo
list in `ntm-user:settings` says how each operation here is done, in the user's
words. A backend can be built on anything the user's agent can reach, for
example a table in a Claude Doc (the Claude Docs connector's own guide gives its
calls). `/ntm:configure-todo-list` fills it with the user against this contract,
and once `ntm-user` is installed, `/ntm:self-test` checks it.

Write a guide as a list of operations, each saying which tool calls carry it out
and which fields map to the conventions' names. Keep the headings below so
skills can find what they need.

## What the backend needs to have

- Tasks with: an id, a title, a description, a status, labels, a single date
  field usable as the planned date, a parent/sub-task relation, and a web url.
  An estimate field and a blocked-by relation are used when present. Say in the
  guide if the backend lacks them; the skills that use them (reviewing,
  planning) work from titles and descriptions instead. With no estimate field,
  the task review log's Estimates block is the record: a task counts as reviewed
  when it has an entry there, and `update task` skips the estimate.
- Some way to group tasks (projects, folders, epics) that can carry labels. If
  groups can't carry labels, say so; the conventions' project-label inheritance
  then doesn't apply, and the user puts system labels on tasks directly.
- A connector for Claude that can list, read and write the above.

Some gaps are survivable: no estimate field, no blocked-by relation, no labels
on groups, no priority, no updated-at, no documents (see Notes), no way to keep
a note inside a project (then every note is at list level). The guide says which
it lacks, and the skills work around them as above. Two aren't: a backend with
no date field to use as the planned date, or no way to tell open tasks from
closed, can't run this system.

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

Each must be covered, and its entry must say what's under it here. Operation
names are what every skill uses; keep them exactly.

### `ping`

One read that proves the connector works and sees the todo list named in Todo
list, and how to tell sign-in expired from wrong account from backend error (the
names `ntm:ready-check` reports).

### `fetch open`

How to get every open task (every plannable status, plus blocked when Todo
list's blocked line isn't blank) with the standard fields, paginated, plus every
project with its name and labels, and its summary when a skill asks for it.

Standard fields: id, title, url (the task's link), status, status class,
priority, estimate, planned date, labels, project, parent id, completed at,
updated at; and, for priority, which value is highest and which means none.

### `fetch closed`

Closed tasks (done; canceled and duplicate on request) with their completion
time, how to limit to a span, and how to limit to one label.

### `read task`

One task with description, parent and blocked-by relations.

### `list sub-tasks`

A task's sub-tasks, open and closed, with the standard fields.

### `read comments` / `write comment` / `update comment`

Per task; if the backend can't update a comment in place, say to delete and
re-add, or to append.

### `set planned date` / `clear planned date`

The date field used, and that nothing else changes.

### `set status`

By the status name in Todo list.

### `add labels` / `remove labels`

Without dropping the others.

### `mark duplicate of`

The duplicate relation; or, if the backend has none, close with the duplicate
status and a comment naming the original.

### `create task`

Title, description, project, parent, blocked-by, labels; and how to check for an
existing match first.

### `update task`

Change a task's title, description, estimate, project (or none), parent, or add
a blocked-by link; nothing else changes.

### `read note` / `write note`

See Notes; `write note` creates a missing note with the content given.

## Notes

Notes are the texts the system keeps on the todo list, titled as Notes under
Todo list says. `read note <title>` returns the note's content, or says it's
missing. `write note <title>` replaces the content, and creates a missing note
with the content given. Both take an optional project, for a note kept in a
project.

If the backend has documents, use them, found by title. If it doesn't, keep each
note in the description of a task titled with the note's title, labeled with the
$no-autoschedule label (its real name from Labels) and left open in a plannable
status. `ntm:fix-todo-list` never touches it (no sub-tasks, no date) and
planners skip it for its label. `read note` is then a title search that reads
that task's description; `write note` replaces it, creating the task when there
is none. A note kept in a project is a task created in that project. The
conventions say every skill ignores such a task as work.

## Setup operations

Used by `ntm:configure-todo-list`. Say which call does each, and what's under it
here.

### `list todo-lists`

The todo lists the connector can see, by name and id; or, where the backend has
no todo lists to list, say so (the user names or pastes theirs, or
`ntm:configure-todo-list` runs `create todo-list`).

### `create todo-list`

Only where the backend has no todo lists to list: make one with the statuses,
labels and notes settled so far, and return its id.

### `list statuses`

A list's status names, so each class can be matched to real names.

### `list labels`

The list's task labels, and its project labels when those are a separate set.

### `create label`

A task label by name, with a description; and a project label by name when those
are a separate set.

### `list projects`

Every project with its name, id and labels.

### `create project`

A project by name, with the project labels it should carry.

### `create note`

A note with a given title and first content, at list level or in a project,
without touching one that already exists (`read note` first). The message
history note's first content is its `Keep:` line.

## Writing

Say how a write reports success, so the conventions' retry rule (retry once,
then report) can be applied.
