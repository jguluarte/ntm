# Linear adapter

How each operation named in the board rules is carried out with the Linear connector (`mcp__Linear__*` tools). Load the tools you need with ToolSearch (`select:mcp__Linear__list_issues,mcp__Linear__save_issue,…`) before calling them.

The connector accepts human-readable references: ticket ids like `ABC-12`, the board name as `team`, and `me` for the signed-in user.

## Board

- **Team:** the config's `board name` (its `board id` is the team id, used wherever a call below takes `teamId`). Ticket ids use the config's `ticket prefix`.
- **Project labels:** labels on a project are Linear project labels, a separate set from issue labels (`list_project_labels` / `save_project_label`); inheritance matches them to issue labels by name, so a system label a project should carry needs a project label of the same name.
- **Automations:** a parent auto-closes when its last sub-issue closes, and sub-issues auto-close when their parent closes, if the board has Linear's default workflow automations on. Cleanup handles either case.

## Status classes

The config maps each class to the board's status names. `list_issues` filters by `state` with a status name; results carry `status` (the name) and `statusType` (Linear's own type: `backlog`, `unstarted`, `started`, `completed`, `canceled`, `duplicate`). Use the config's names to filter and to write; use `statusType` to tell closed from open when a result mixes states. A ticket's status class is the class whose config row lists its `status` name; `statusType` alone doesn't give it.

## Operations

### `ping`

`get_team` (`query: "<board id>"`). A team named `board name` comes back: pass. A different team: wrong account. Unauthorized or forbidden: sign-in expired. Not found: wrong account. Anything else: tracker error.

### `fetch open`

One `list_issues` call per open status name (every plannable status, plus the blocked status; skip the blocked call when the config's `blocked status` is blank), each with `team: "<board name>"`, no assignee filter, `limit: 250`, and `fields`: `title`, `url`, `status`, `statusType`, `priority`, `estimate`, `dueDate`, `labels`, `project`, `parentId`, `completedAt`, `updatedAt`. Paginate with `cursor` while `hasNextPage` is true. Merge the results.

Also list every project once with `list_projects` (`team: "<board name>"`, `fields` `name` and `labels`, plus `summary` when a skill asks for the project's summary, paginating with `cursor`), and match each issue's `project` against them by name, so inherited labels count.

`dueDate` holds the planned date: the day the work is planned for. `url` is the ticket's link; always ask for it in `fields`. `priority` is `0` when none is set; `1` is the highest.

### `fetch closed`

`list_issues` as above with `state` set to the done status name; add a call each for the canceled and duplicate names only when asked. For a span, pass `completedAt` as the span's start and then keep issues whose `completedAt` falls in it, in the config's timezone. When a skill asks for one label, add `label: "<label name>"` to each call.

### `read ticket`

`get_issue` with the id, `includeRelations: true` for parent and blocked-by relations. Descriptions come with it; comments and sub-issues don't.

### `list sub-tickets`

`list_issues` with `parentId: "<id>"` and no `state`, same `fields` as `fetch open`.

### `read comments` / `write comment` / `update comment`

`list_comments` with the issue id. `save_comment` with `issueId` and `body` creates; with `id` it updates in place.

### `set planned date` / `clear planned date`

`save_issue` with `id` and `dueDate: "YYYY-MM-DD"`; clear with `dueDate: null`. Change nothing else on the issue.

### `set status`

`save_issue` with `id` and `state: "<status name from the config>"`.

### `add labels` / `remove labels`

`save_issue` with `id` and `addLabels` or `removeLabels` (lists of label names). Never use `labels`, which replaces the whole set. Check a label exists with `list_issue_labels` (`team`) before adding one for the first time.

### `mark duplicate of`

`save_issue` with `id`, `duplicateOf: "<original id>"` and `state: "<duplicate status name>"`.

### `create ticket`

`save_issue` without `id`: `team`, `title`, `description`, optional `project`, `parentId`, `dueDate`, `labels`. Blocked-by relations: `blockedBy: ["<id>"]`. Check for an existing match with `list_issues` (`query`) first.

### `update ticket`

`save_issue` with `id` and only the fields the skill changes: `title`, `description`, `estimate`, `project` (`project: null` to remove it), `parentId`, and `blockedBy: ["<id>"]` to add a blocked-by link. Nothing else changes.

### Notes

Notes are Linear documents in the team. A note kept inside a project (the price-watch stores note) lives in that project's documents instead: search with `projectId` instead of `teamId` (the project's id, from `list_projects` with `team: "<board name>"` and `query: "<project name>"`), and create with `project: "<project name>"` instead of `team`.

- **`read note`:** `list_documents` with `query: "<note name>"` and `teamId: "<board id>"`, then `get_document` with the match's id. No match means the note is missing.
- **`write note`:** `save_document` with the note's `id` and the new `content`, changing only what the skill says to change. When the note is missing, create it: `save_document` without `id`, with `team` (or `project`), `title` set to the note's configured name, and `content`.

## Setup operations

Used by `nudge:setup` only.

- **`list boards`:** `list_teams`.
- **`list statuses`:** `list_issue_statuses` with `team`.
- **`list labels`:** `list_issue_labels` with `team`.
- **`create label`:** `save_issue_label` with `name` and `teamId: "<board id>"`.
- **`create project`:** project labels are a separate set from ticket labels (`list_project_labels` with `team`; `save_project_label` with `name`, `teamId`): create the ones the project should carry first, then `save_project` with `name`, `addTeams` naming the board, and `labels`. `labels` replaces the set, so pass current plus missing when updating (see Board).

## Writing

`save_issue`, `save_comment` and `save_document` both create and update: omit `id` to create, pass `id` to update, and pass only the fields to change. The response says whether the write succeeded; the board rules' retry rule applies.
