# Linear guide

How ntm runs on Linear: setting it up with the user, then how each operation in
`contract.md` is done with the Linear connector. The connector's own
instructions and tool descriptions are the authority on how to call its tools;
this guide says which tool does each operation and which of the user's values
goes where.

The build copies Task list through Writing into `ntm-user:backend` as written,
with `<List name>` and `<List id>` filled in. It also copies `linear-mcp.json`,
beside this guide, into `ntm-user`'s `.mcp.json`, so the connector comes
bundled.

## Setting up Linear

### 1. A Linear account

Only when the user doesn't have Linear yet. They sign up at linear.app; the free
plan is enough. The new workspace comes with one team, and that team is their
task list. Its key, the capital letters that start every task's id (`HOME` in
`HOME-12`), shows up in their reminders, so they pick one they like reading.

The team's statuses already fit ntm. A user who wants one for tasks they can't
move right now adds a status named Blocked in the team's workflow settings.

Wait for them to say they're done.

### 2. The connector

ToolSearch for `get_team`. When it isn't there, the user adds Linear on the
Connectors tab in Claude's settings, signs in to their workspace, and says so.
Search again before going on.

### 3. The team

`list todo-lists`, and propose a team. Its name is the List name and its id the
List id.

`ping` it right away. A pass: say in a line that the list answers. Anything
else: say what failed, as `ping` words it, and fix it with them, such as signing
in again with the account that holds the team. If it won't pass, say so and
stop: every later step needs the list.

Suggest turning on Parent auto-close, in the team's settings under Workflow, so
a parent closes once its sub-tasks are all done.

## Task list

The task list is the Linear team `<List name>`. `<List id>` is its id, used
wherever a call takes `teamId`.

Projects carry Linear project labels, a separate set from issue labels. A
project's label counts by name, so each system label has a project label of the
same name.

ntm doesn't use Linear's estimate field. An estimate is the `Estimate:` line at
the end of the issue's description, such as `Estimate: 2 hours`.

## Status classes

A status's class comes from its `statusType`:

| `statusType`           | Class                 |
| ---------------------- | --------------------- |
| `backlog`, `unstarted` | plannable             |
| `started`              | plannable and started |
| `completed`            | done                  |
| `canceled`             | canceled              |
| `duplicate`            | duplicate             |

A status named Blocked is the blocked class, whatever its type. Results carry
`status`, the name, and `statusType`; `list_issues` and `save_issue` take either
in `state`.

## Operations

### `ping`

`get_team` with `query: "<List id>"`. Team `<List name>` comes back: pass.
Another team, or not found: wrong account. Unauthorized or forbidden: sign-in
expired. Anything else: backend error.

The connector bundled with `ntm-user` needs its own sign-in. Until it has one,
it shows only `authenticate` and `complete_authentication`, which is sign-in
expired. The fix, in a chat: call `authenticate` and give the user the link it
returns; when the page it lands on doesn't load, pass that page's address to
`complete_authentication`. In a job no one can sign in, so the fix is "open a
chat and run /ntm:self-test".

### `fetch open`

`list_issues` once for each open type, with `state` set to `backlog`,
`unstarted` and `started`, and merge the results. A Blocked status has one of
these types, so it comes back too. Each call takes `team: "<List name>"`,
`limit: 250` and `fields`: `title`, `url`, `status`, `statusType`, `priority`,
`description`, `dueDate`, `labels`, `project`, `parentId`, `completedAt` and
`updatedAt`.

Then `list_projects` once, with `team: "<List name>"` and `fields` `name` and
`labels`, plus `summary` when a skill asks for it. Match each issue's `project`
to them by name, so its project's labels count.

`dueDate` is the planned date and `url` the task's link. The estimate is read
from `description`. `priority` is `0` for none and `1` for the highest.

### `fetch closed`

`list_issues` as in `fetch open`, with `state: "completed"`, plus a call each
for `canceled` and `duplicate` only when asked. For a span, pass its first day
as `completedAt`. For one label, add `label: "<label name>"` to each call.

### `read task`

`get_issue` with the id and `includeRelations: true`, for the description and
blocked-by relations.

### `read comments` / `write comment` / `update comment`

`list_comments` with the issue id. `save_comment` with `issueId` and `body` adds
one; with `id` as well, it changes that one in place.

### `set planned date` / `clear planned date`

`save_issue` with `id` and `dueDate: "YYYY-MM-DD"`, or `dueDate: null` to clear
it.

### `set status`

`save_issue` with `id` and `state`: `completed`, `canceled` or `duplicate` for
those classes, `Blocked` for blocked, and a status's name for plannable;
`list_issue_statuses` with `team` lists them.

### `add labels` / `remove labels`

`save_issue` with `id` and `addLabels` or `removeLabels`, each a list of label
names.

### `mark duplicate of`

`save_issue` with `id`, `duplicateOf: "<original id>"` and `state: "duplicate"`.

### `create task`

`list_issues` with `query` first, to check for a match. Then `save_issue`
without `id`: `team`, `title`, `description`, and any of `project`, `parentId`,
`dueDate`, `labels` and `blockedBy: ["<id>"]`.

### `update task`

`save_issue` with `id` and only the fields that change: `title`, `description`
(where the estimate is written), `project` (`null` removes it), or
`blockedBy: ["<id>"]` to add a blocked-by link.

## Databases

Databases are Linear documents in the team, under the titles the rules give. One
kept in a project lives in that project's documents instead: search with
`projectId`, the project's id from `list_projects`, in place of `teamId`, and
create with `project: "<project name>"` in place of `team`.

### `read database`

`list_documents` with `query: "<database title>"` and `teamId: "<List id>"`,
then `get_document` with the id of the result whose `title` is the database's
title. No match: the database is missing.

### `write database`

`save_document` with the database's `id` and the new `content`, changing only
what the skill changes. When it's missing, create it as `create database` does,
with the whole content.

### `create database`

`read database` first, and leave one that exists alone. Otherwise
`save_document` with `team: "<List name>"`, `title` set to the database's title,
and `content` set to its first content.

## Writing

The response says whether the write succeeded; the rules' retry rule applies.

## Setup operations

### `list todo-lists`

`list_teams`. Each team comes back with its name and id.

### `list projects`

`list_projects` with `team: "<List name>"` and `fields` `name` and `labels`.
Each comes back with its id.

### `create label`

Each label is made as both an issue label and a project label, under the same
name. `list_issue_labels` and `list_project_labels` with `team`; for each set
without the name, `save_issue_label` or `save_project_label` with `name`,
`teamId: "<List id>"` and `description`.

### `create project`

`save_project` with `name`, `addTeams: ["<List name>"]` and `labels`. For an
existing project, pass its `id` and its current labels plus the new ones, since
`labels` replaces the set.
