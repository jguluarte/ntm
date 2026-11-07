# Linear guide

Tested. How each operation named in the conventions is carried out with the
Linear connector (`mcp__Linear__*` tools). Load the tools you need with
ToolSearch (`select:mcp__Linear__list_issues,mcp__Linear__save_issue,…`) before
calling them.

The connector accepts human-readable references: task ids like `ABC-12`, the
todo list name as `team`, and `me` for the signed-in user.

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
- **Automations:** a parent auto-closes when its last sub-issue closes, and
  sub-issues auto-close when their parent closes, if the todo list has Linear's
  default workflow automations on. `ntm:fix-todo-list` handles either case.
- **Estimates:** `estimate` holds the team's points. When Planning has an
  Estimate mapping, convert through it: the user's size to its point when
  writing, a point back to its size when reading.

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

`get_team` (`query: "<List id>"`). A team named as List name says comes back:
pass. A different team: wrong account. Unauthorized or forbidden: sign-in
expired. Not found: wrong account. Anything else: backend error.

### `fetch open`

One `list_issues` call per open status name: every plannable status, plus the
blocked status (skip the blocked call when Todo list's blocked line is blank).
Each call has `team: "<List name>"`, no assignee filter, `limit: 250`, and
`fields`: `title`, `url`, `status`, `statusType`, `priority`, `estimate`,
`dueDate`, `labels`, `project`, `parentId`, `completedAt`, `updatedAt`. Paginate
with `cursor` while `hasNextPage` is true. Merge the results.

Also list every project once with `list_projects` (`team: "<List name>"`,
`fields` `name` and `labels`, plus `summary` when a skill asks for the project's
summary, paginating with `cursor`). Match each issue's `project` against them by
name, so inherited labels count.

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
relations. Descriptions come with it; comments and sub-issues don't.

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
Never use `labels`, which replaces the whole set. Check a label exists with
`list_issue_labels` (`team`) before adding one for the first time.

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
  it as `create note` does, with the content given as its content (not only a
  `Keep:` line; the content for the message history note already starts with its
  `Keep:` line).

## Setup operations

Used by `ntm:configure-todo-list`.

- **`list todo-lists`:** `list_teams`. Each comes back with its name, id and
  issue key (the task prefix).
- **`create todo-list`:** not needed; Linear has teams to list.
- **`list statuses`:** `list_issue_statuses` with `team`. Each comes back with
  its name and `type`, which suggests the class (`backlog`, `unstarted` and
  `started` are plannable, `started` the started one; `completed` done;
  `canceled` canceled; `duplicate` duplicate); the user confirms the mapping.
- **`read estimate type`:** `get_team` with `query: "<List id>"`; its estimate
  type is the scale `estimate` takes: linear (1–5), exponential, Fibonacci, or
  T-shirt sizes, stored as points (XS 1, S 2, M 3, L 5, XL 8). Times can't be
  stored.
- **`list labels`:** `list_issue_labels` with `team` for issue labels;
  `list_project_labels` with `team` for project labels, a separate set.
- **`create label`:** `save_issue_label` with `name`, `teamId: "<List id>"` and
  `description` for an issue label; `save_project_label` with `name`, `teamId`
  and `description` for a project label.
- **`list projects`:** `list_projects` with `team: "<List name>"`, `fields`
  `name` and `labels`, paginating with `cursor`. Each comes back with its id.
- **`create project`:** create the project labels it should carry first
  (`create label`), then `save_project` with `name`, `addTeams` naming the todo
  list, and `labels`. `labels` replaces the set, so pass current plus missing
  when updating an existing project.
- **`create note`:** `read note` first; one that exists is left alone. Otherwise
  `save_document` without `id`, with `team: "<List name>"` (or
  `project: "<project name>"` for a note kept in a project), `title` set to the
  note's title from Todo list, and `content` set to its first content (for the
  message history note, the `Keep:` line).

## Writing

`save_issue`, `save_comment`, `save_document`, `save_project` and the label
saves both create and update: omit `id` to create, pass `id` to update, and pass
only the fields to change. The response says whether the write succeeded; the
conventions' retry rule applies.
