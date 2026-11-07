# Linear guide

The backend guide for Linear, and a tested one: how each operation the
conventions name is carried out with the Linear connector. `ntm:conventions`
reads it when Backend is `linear`; `ntm:configure-todo-list` reads it for Setup.

Use the tools of the Linear connector that's signed in. Its own instructions and
tool descriptions are the authority on how to call them. This guide says which
tool does each operation and which of the user's values goes where.

Values below that name a settings section (Todo list, Labels, Planning, About
you) come from `ntm-user:settings`, read as the conventions' Loading step says.

## Todo list

- **Team:** List name from Todo list (List id is the team id, used wherever a
  call below takes `teamId`). Task ids use Task prefix from Todo list.
- **Project labels:** labels on a project are Linear project labels, a separate
  set from issue labels (`list_project_labels` / `save_project_label`).
  Inheritance matches them to issue labels by name, so a system label a project
  should carry needs a project label of the same name (the project labels under
  Labels).
- **Automations:** Linear can close a parent when its sub-issues are all done
  (Parent auto-close, in the team's settings under Workflow).
- **Estimates:** `estimate` holds the team's points, on the team's estimate
  type: linear (1, 2, 3, 4, 5), exponential (1, 2, 4, 8, 16), Fibonacci (1, 2,
  3, 5, 8) or T-shirt sizes, stored as points (XS 1, S 2, M 3, L 5, XL 8). A
  team can extend its scale or allow zero. Times can't be stored. The connector
  doesn't say which type a team uses; the user does. When Planning has an
  Estimate mapping, convert through it: the user's estimate to its point when
  writing, a point back to their estimate when reading.

## Status classes

Todo list in your settings maps each class to the status names. `list_issues`
filters by `state` with a status name; results carry `status` (the name) and
`statusType` (Linear's own type: `backlog`, `unstarted`, `started`, `completed`,
`canceled`, `duplicate`). Use the names from Todo list to filter and to write;
use `statusType` to tell closed from open when a result mixes states. A task's
status class is the class whose line in Todo list lists its `status` name;
`statusType` alone doesn't give it.

## Operations

### `ping`

`get_team` (`query: "<List id>"`). The team named in List name comes back: pass.
A different team: wrong account. Unauthorized or forbidden: sign-in expired. Not
found: wrong account. Anything else: backend error.

### `fetch open`

One `list_issues` call per open status name: every plannable status, plus the
blocked status (skip the blocked call when Todo list's blocked line is blank).
Each call has `team: "<List name>"`, `assignee: "me"` only when Your tasks in
Todo list says the user's tasks are the ones assigned to them, `limit: 250`, and
`fields`: `title`, `url`, `status`, `statusType`, `priority`, `estimate`,
`dueDate`, `labels`, `project`, `parentId`, `completedAt`, `updatedAt`. Merge
the results.

Also list every project once with `list_projects` (`team: "<List name>"`,
`fields` `name` and `labels`, plus `summary` when a skill asks for the project's
summary). Match each issue's `project` against them by name, so inherited labels
count.

`dueDate` holds the planned date: the day the work is planned for. `url` is the
task's link; always ask for it in `fields`. `priority` is `0` when none is set;
`1` is the highest.

### `fetch closed`

`list_issues` as above with `state` set to the done status name; add a call each
for the canceled and duplicate names only when asked. For a span, pass
`completedAt` as the span's start and then keep issues whose `completedAt` falls
in it, in the timezone from About you. When a skill asks for one label, add
`label: "<label name>"` to each call.

### `read task`

`get_issue` with the id, `includeRelations: true` for parent and blocked-by
relations. Descriptions come with it; sub-issues don't.

### `list sub-tasks`

`list_issues` with `parentId: "<id>"` and no `state`, same `fields` as
`fetch open`.

### `read comments` / `write comment` / `update comment`

`list_comments` with the issue id. `save_comment` with `issueId` and `body`
creates; with `id` it updates in place.

### `set planned date` / `clear planned date`

`save_issue` with `id` and `dueDate: "YYYY-MM-DD"`; clear with `dueDate: null`.
Change nothing else on the issue.

### `set status`

`save_issue` with `id` and `state: "<status name from Todo list>"`.

### `add labels` / `remove labels`

`save_issue` with `id` and `addLabels` or `removeLabels` (lists of label names).
Check a label exists with `list_issue_labels` (`team`) before adding one for the
first time.

### `mark duplicate of`

`save_issue` with `id`, `duplicateOf: "<original id>"` and
`state: "<duplicate status name from Todo list>"`.

### `create task`

`save_issue` without `id`: `team`, `title`, `description`, optional `project`,
`parentId`, `dueDate`, `labels`. Blocked-by relations: `blockedBy: ["<id>"]`.
Check for an existing match with `list_issues` (`query`) first.

### `update task`

`save_issue` with `id` and only the fields the skill changes: `title`,
`description`, `estimate`, `project` (`project: null` to remove it), `parentId`,
and `blockedBy: ["<id>"]` to add a blocked-by link. Nothing else changes.

### Notes

Notes are Linear documents in the team, titled as Notes under Todo list says. A
note kept inside a project (the price watch stores note, in the price watch
project from Todo list) lives in that project's documents instead. Search with
`projectId` instead of `teamId` (the project's id, from `list_projects` with
`team: "<List name>"` and `query: "<project name>"`), and create with
`project: "<project name>"` instead of `team`.

- **`read note`:** `list_documents` with `query: "<note title>"` and
  `teamId: "<List id>"`, then `get_document` with the id of the result whose
  `title` is the note's title. No match means the note is missing.
- **`write note`:** `save_document` with the note's `id` and the new `content`,
  changing only what the skill says to change. When the note is missing, create
  it the way `create note` does, but with the whole content given, not only a
  `Keep:` line (the content for the message history note already starts with its
  `Keep:` line).

## Setup

The walkthrough `ntm:configure-todo-list` follows with the user, part by part in
order; a part named for one of its steps (Planning) waits for that step. The
calls it uses are under Setup operations.

### The backend

Backend is `linear`. If the user doesn't have Linear yet, do Starting from
nothing first.

### Starting from nothing

These happen outside the chat, on the user's side; walk them through in order
and wait for "done" before The connector below:

1. Sign up at linear.app. The free plan is enough: one workspace, unlimited
   issues.
2. The new workspace comes with one team; that team is the todo list. Its key
   (the few capital letters Linear asks for when naming it, `HOME` for
   `HOME-12`) becomes Task prefix, so pick one they'll be happy reading in
   reminders.
3. A new team's statuses already match the classes: Backlog, Todo, In Progress,
   Done, Canceled and Duplicate. Nothing to change. If they want a "can't move
   right now" status, they add one named Blocked in the team's workflow
   settings; otherwise the $pending-shipment label and blocked-by links cover
   that ground.

Labels, the price watch project and the notes don't need to be made by hand:
Labels and Notes in `ntm:configure-todo-list` create them.

### The connector

Check that a signed-in Linear connector is present. If it isn't there, walk the
user through it: in Claude's settings, the Connectors tab, add Linear and sign
in to their workspace, then come back here and say so.

### The todo list

`list todo-lists`; propose the team. List name is its name, List id its id, Task
prefix its issue key.

Once the team is chosen, suggest the user turn on Parent auto-close in the
team's settings under Workflow, so a parent closes as soon as its sub-tasks are
all done.

### The price watch project

`list projects`; ask which project holds purchases waiting for a good price, or
none (none turns price watch off). If they want one that doesn't exist yet,
settle its name now; it's created in Labels, once the project labels exist.

### Planning

Ask which estimate type their team uses: linear, exponential, Fibonacci or
T-shirt sizes (Estimates, under Todo list above, has each one's points). If
they're unsure, it's in Linear under the team's settings, Estimates. If they
still don't know, run `sample estimates` and suggest the type that fits. When
their scale isn't the team's, agree with them which of the team's points each
estimate on their scale becomes, and record it as Estimate mapping.

## Setup operations

Used by `ntm:configure-todo-list`.

### `list todo-lists`

`list_teams`. Each comes back with its name, id and issue key (the task prefix).

### `create todo-list`

Not needed; Linear has teams to list.

### `list statuses`

`list_issue_statuses` with `team`. Each comes back with its name and `type`,
which suggests the class (`backlog`, `unstarted` and `started` are plannable,
`started` the started one; `completed` done; `canceled` canceled; `duplicate`
duplicate); the user confirms the mapping.

### `sample estimates`

`list_issues` with `team: "<List name>"`, `limit: 50` and `fields` `title` and
`estimate`. Suggest the estimate type (Estimates, above) whose points fit the
ones already set: a 4 rules out Fibonacci and T-shirt, a 5 rules out
exponential. Fibonacci and T-shirt store the same points; ask which they see on
their tasks in Linear. No estimates set means no suggestion.

### `list labels`

`list_issue_labels` with `team` for issue labels; `list_project_labels` with
`team` for project labels, a separate set.

### `create label`

`save_issue_label` with `name`, `teamId: "<List id>"` and `description` for an
issue label; `save_project_label` with `name`, `teamId` and `description` for a
project label.

### `list projects`

`list_projects` with `team: "<List name>"`, `fields` `name` and `labels`. Each
comes back with its id.

### `create project`

Create the project labels it should carry first (`create label`), then
`save_project` with `name`, `addTeams` naming the todo list, and `labels`. When
updating an existing project, pass its current labels plus the missing ones.

### `create note`

`read note` first; one that exists is left alone. Otherwise `save_document`
without `id`, with `team: "<List name>"` (or `project: "<project name>"` for a
note kept in a project), `title` set to the note's title from Todo list, and
`content` set to its first content (for the message history note, the `Keep:`
line).

## Writing

The response says whether the write succeeded; the conventions' retry rule
applies.
