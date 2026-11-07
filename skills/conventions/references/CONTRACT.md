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

- **No estimate field:** the task review log is the record, as the conventions'
  Estimates says, and `update task` skips the estimate.
- **No blocked-by relation:** reviewing and planning work from titles and
  descriptions instead.
- **No labels on groups:** the conventions' project-label inheritance doesn't
  apply, and the user puts system labels on tasks directly.
- **No priority, or no updated-at:** skills do without them.
- **No documents:** notes are kept in tasks (see Notes).
- **No way to keep a note inside a project:** every note is at list level.

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

Cover every operation. Skills call them by these names; keep them exactly.

| Operation                                            | Must say                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ping`                                               | one read that proves the connector works and sees the todo list named in Todo list, and how to tell sign-in expired from wrong account from backend error (the names `ntm:ready-check` reports)                                                                                                                                                                                                                                                                         |
| `fetch open`                                         | how to get every open task (every plannable status, plus blocked when Todo list's blocked line isn't blank) with the standard fields, paginated, plus every project with its name and labels, and its summary when a skill asks for it. Standard fields: id, title, url (the task's link), status, status class, priority, estimate, planned date, labels, project, parent id, completed at, updated at; and, for priority, which value is highest and which means none |
| `fetch closed`                                       | closed tasks (done; canceled and duplicate on request) with their completion time, how to limit to a span, and how to limit to one label                                                                                                                                                                                                                                                                                                                                |
| `read task`                                          | one task with description, parent and blocked-by relations                                                                                                                                                                                                                                                                                                                                                                                                              |
| `list sub-tasks`                                     | a task's sub-tasks, open and closed, with the standard fields                                                                                                                                                                                                                                                                                                                                                                                                           |
| `read comments` / `write comment` / `update comment` | per task; if the backend can't update a comment in place, say to delete and re-add, or to append                                                                                                                                                                                                                                                                                                                                                                        |
| `set planned date` / `clear planned date`            | the date field used, and that nothing else changes                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `set status`                                         | by the status name in Todo list                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `add labels` / `remove labels`                       | without dropping the others                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `mark duplicate of`                                  | or, if the backend has no duplicate relation, close with the duplicate status and a comment naming the original                                                                                                                                                                                                                                                                                                                                                         |
| `create task`                                        | title, description, project, parent, blocked-by, labels; and how to check for an existing match first                                                                                                                                                                                                                                                                                                                                                                   |
| `update task`                                        | change a task's title, description, estimate, project (or none), parent, or add a blocked-by link; nothing else changes                                                                                                                                                                                                                                                                                                                                                 |
| `read note` / `write note`                           | see Notes; `write note` creates a missing note with the content given                                                                                                                                                                                                                                                                                                                                                                                                   |

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
that task's description; `write note` replaces the description, creating the
task when there is none. A note kept in a project is a task created in that
project. The conventions say every skill ignores such a task as work.

## Setup operations

Used by `ntm:configure-todo-list`. Say which call does each.

| Operation          | Must say                                                                                                                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `list todo-lists`  | the todo lists the connector can see, by name and id; or, where the backend has no todo lists to list, say so (the user names or pastes theirs, or `ntm:configure-todo-list` runs `create todo-list`)  |
| `create todo-list` | only where the backend has no todo lists to list: make one with the statuses, labels and notes settled so far, and return its id                                                                       |
| `list statuses`    | a list's status names, so each class can be matched to real names                                                                                                                                      |
| `list labels`      | the list's task labels, and its project labels when those are a separate set                                                                                                                           |
| `create label`     | a task label by name, with a description; and a project label by name when those are a separate set                                                                                                    |
| `list projects`    | every project with its name, id and labels                                                                                                                                                             |
| `create project`   | a project by name, with the project labels it should carry                                                                                                                                             |
| `create note`      | a note with a given title and first content, at list level or in a project, without touching one that already exists (`read note` first). The message history note's first content is its `Keep:` line |

## Writing

Say how a write reports success, so the conventions' retry rule (retry once,
then report) can be applied.
