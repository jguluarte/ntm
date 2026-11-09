# Linear guide

The backend guide for Linear, and a tested one: how each operation the backend
contract names is carried out with the Linear connector. The build copies
everything below this paragraph into `ntm-user:backend` as written, with
`<List name>` and `<List id>` filled in. Setting Linear up with the user is part
of setup's todo list step, `todo-list.md`.

Use the tools of the Linear connector that's signed in. Its own instructions and
tool descriptions are the authority on how to call them. This guide says which
tool does each operation and which of the user's values goes where.

## Todo list

- **Team:** `<List name>`, the team's name; `<List id>` is its id, used wherever
  a call below takes `teamId`.
- **Project labels:** labels on a project are Linear project labels, a separate
  set from issue labels (`list_project_labels` / `save_project_label`).
  Inheritance matches them to issue labels by name, so a label a project carries
  needs a project label with the same name.
- **Automations:** Linear can close a parent when its sub-issues are all done
  (Parent auto-close, in the team's settings under Workflow).
- **Estimates:** `estimate` holds the team's points, on the team's estimate
  type: linear (1, 2, 3, 4, 5), exponential (1, 2, 4, 8, 16), Fibonacci (1, 2,
  3, 5, 8) or T-shirt sizes, stored as points (XS 1, S 2, M 3, L 5, XL 8). A
  team can extend its scale or allow zero. Times can't be stored. The connector
  doesn't say which type a team uses; the user does. When Estimate pattern,
  under Planning in the Settings document, gives a point for each estimate,
  convert through it: the user's estimate to its point when writing, a point
  back to their estimate when reading.

Setup doesn't ask about estimates; the user's first review does. When they need
help there, guide them: ask which estimate type their team uses (each one's
points are above). If they're unsure, it's in Linear under the team's settings,
Estimates. If they still don't know, look at estimates already set:
`list_issues` with `team: "<List name>"`, `limit: 50` and `fields` `title` and
`estimate`, and suggest the type whose points fit (a 4 rules out Fibonacci and
T-shirt, a 5 rules out exponential; Fibonacci and T-shirt store the same points,
so ask which they see in Linear). When their scale isn't the team's, agree with
them which of the team's points each of their estimates becomes, and add that to
Estimate pattern.

## Status classes

A task's class comes from `statusType`, Linear's own type for its status:

- `backlog` and `unstarted`: plannable.
- `started`: plannable and started.
- `completed`: done.
- `canceled`: canceled.
- `duplicate`: duplicate.

One exception: a status named Blocked is the blocked class, whatever its type
(Deviations can name another). Results carry `status` (the name) and
`statusType`. `list_issues` and `save_issue` take either a type or a name in
`state`.

## Operations

### `ping`

`get_team` (`query: "<List id>"`). Team `<List name>` comes back: pass. A
different team: wrong account. Unauthorized or forbidden: sign-in expired. Not
found: wrong account. Anything else: backend error.

### `fetch open`

One `list_issues` call per open type: `state` set to `backlog`, `unstarted` and
`started`. A Blocked status has one of these types, so it comes back too. Each
call has `team: "<List name>"`, `limit: 250`, and `fields`: `title`, `url`,
`status`, `statusType`, `priority`, `estimate`, `dueDate`, `labels`, `project`,
`parentId`, `completedAt`, `updatedAt`. Merge the results.

Also list every project once with `list_projects` (`team: "<List name>"`,
`fields` `name` and `labels`, plus `summary` when a skill asks for the project's
summary). Match each issue's `project` against them by name, so inherited labels
count.

`dueDate` holds the planned date: the day the work is planned for. `url` is the
task's link; always ask for it in `fields`. `priority` is `0` when none is set;
`1` is the highest.

### `fetch closed`

`list_issues` as above with `state` set to `completed`; add a call each for
`canceled` and `duplicate` only when asked. For a span, pass `completedAt` as
its first day. When a skill asks for one label, add `label: "<label name>"` to
each call.

### `read task`

`get_issue` with the id, `includeRelations: true` for blocked-by relations.
Descriptions come with it.

### `read comments` / `write comment` / `update comment`

`list_comments` with the issue id. `save_comment` with `issueId` and `body`
creates; with `id` it updates in place.

### `set planned date` / `clear planned date`

`save_issue` with `id` and `dueDate: "YYYY-MM-DD"`; clear with `dueDate: null`.
Change nothing else on the issue.

### `set status`

`save_issue` with `id` and `state`. For done, canceled and duplicate, pass the
type: `completed`, `canceled` or `duplicate`. For blocked, pass `Blocked` (or
the name Deviations gives). For a plannable status, pass its name;
`list_issue_statuses` with `team` lists them.

### `add labels` / `remove labels`

`save_issue` with `id` and `addLabels` or `removeLabels` (lists of label names).
Check a label exists with `list_issue_labels` (`team`) before adding one for the
first time.

### `mark duplicate of`

`save_issue` with `id`, `duplicateOf: "<original id>"` and `state: "duplicate"`.

### `create task`

`save_issue` without `id`: `team`, `title`, `description`, optional `project`,
`parentId`, `dueDate`, `labels`. Blocked-by relations: `blockedBy: ["<id>"]`.
Check for an existing match with `list_issues` (`query`) first.

### `update task`

`save_issue` with `id` and only the fields the skill changes: `title`,
`description`, `estimate`, `project` (`project: null` to remove it), and
`blockedBy: ["<id>"]` to add a blocked-by link. Nothing else changes.

### Databases

Databases are Linear documents in the team, under the titles the core rules
give. A database kept inside a project (the price watch stores database, in the
project that carries the $price-watch label) lives in that project's documents
instead. Search with `projectId` instead of `teamId` (the project's id, from
`list_projects` with `team: "<List name>"` and `query: "<project name>"`), and
create with `project: "<project name>"` instead of `team`.

- **`read database`:** `list_documents` with `query: "<database title>"` and
  `teamId: "<List id>"`, then `get_document` with the id of the result whose
  `title` is the database's title. No match means the database is missing.
- **`write database`:** `save_document` with the database's `id` and the new
  `content`, changing only what the skill says to change. When the database is
  missing, create it the way `create database` does, but with the whole content
  given, not only its frontmatter (the content for the message history database
  already starts with its frontmatter).
- **`create database`:** `read database` first; one that exists is left alone.
  Otherwise `save_document` without `id`, with `team: "<List name>"` (or
  `project: "<project name>"` for a database kept in a project), `title` set to
  the database's title, and `content` set to its first content (for the message
  history database, its frontmatter).

## Writing

The response says whether the write succeeded; the core rules' retry rule
applies.
