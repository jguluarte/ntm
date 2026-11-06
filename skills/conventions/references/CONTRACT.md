# Backend contract

A backend guide maps the operations the conventions name onto one backend's connector. `linear.md` is the complete, tested one. `claude-docs.md` is the second shipped guide, for a board kept in a Claude Doc with no ticket-system connector at all. It's untested, and heavier per run (every read pulls a whole table and every write edits a row), but fine for a few dozen tickets. For any other backend, Board in `ntm-user:settings` says how each operation here is done, in the user's words. `/ntm:configure-board` fills it with the user against this contract, and once `ntm-user` is installed, `/ntm:self-test` checks it.

Write a guide as a list of operations, each saying which tool calls carry it out and which fields map to the conventions' names. Keep the headings below so skills can find what they need.

## What the backend needs to have

- Tickets with: an id, a title, a description, a status, labels, a single date field usable as the planned date, a parent/sub-ticket relation, and a web url. An estimate field and a blocked-by relation are used when present. Say in the guide if the backend lacks them; the skills that use them (grooming, planning) work from titles and descriptions instead. With no estimate field, the grooming log's Estimates block is the record: a ticket counts as groomed when it has an entry there, and `update ticket` skips the estimate.
- Some way to group tickets (projects, folders, epics) that can carry labels. If groups can't carry labels, say so; the conventions' project-label inheritance then doesn't apply, and the user puts system labels on tickets directly.
- A connector for Claude that can list, read and write the above.

Some gaps are survivable: no estimate field, no blocked-by relation, no labels on groups, no priority, no updated-at, no documents (see Notes), no way to keep a note inside a project (then every note is at board level). The guide says which it lacks, and the skills work around them as above. Two aren't: a backend with no date field to use as the planned date, or no way to tell open tickets from closed, can't run this system.

## Board

Name the board (Board name in Board), what id it needs (Board id), and which automations the backend runs on parent/sub-ticket closing, if any. If the backend has no unit above projects, the board is the whole account (Board name is what the backend calls it, Board id blank). If ids carry no prefix, Ticket prefix is blank and ids are the backend's own; `(ABC-12)` in the conventions then means the bare id.

## Status classes

Say how the status names in Board are used to filter and to write, and how to tell open from closed in results. A backend with no status names, only open and closed, lists `open` as the one plannable status, `closed` as done, and leaves started, blocked, canceled and duplicate blank. The classes those lines name then don't exist on this board, and `set status` to done closes the ticket.

## Operations

Each must be covered. Operation names are what every skill uses; keep them exactly.

| Operation | Must say |
| --- | --- |
| `ping` | one read that proves the connector works and sees the board named in Board, and how to tell sign-in expired from wrong account from backend error (the names `ntm:ready-check` reports) |
| `fetch open` | how to get every open ticket (every plannable status, plus blocked when Board's blocked line isn't blank) with the standard fields, paginated, plus every project with its name and labels, and its summary when a skill asks for it. Standard fields: id, title, url (the ticket's link), status, status class, priority, estimate, planned date, labels, project, parent id, completed at, updated at; and, for priority, which value is highest and which means none |
| `fetch closed` | closed tickets (done; canceled and duplicate on request) with their completion time, how to limit to a span, and how to limit to one label |
| `read ticket` | one ticket with description, parent and blocked-by relations |
| `list sub-tickets` | a ticket's sub-tickets, open and closed, with the standard fields |
| `read comments` / `write comment` / `update comment` | per ticket; if the backend can't update a comment in place, say to delete and re-add, or to append |
| `set planned date` / `clear planned date` | the date field used, and that nothing else changes |
| `set status` | by the status name in Board |
| `add labels` / `remove labels` | without dropping the others |
| `mark duplicate of` | or, if the backend has no duplicate relation, close with the duplicate status and a comment naming the original |
| `create ticket` | title, description, project, parent, blocked-by, labels; and how to check for an existing match first |
| `update ticket` | change a ticket's title, description, estimate, project (or none), parent, or add a blocked-by link; nothing else changes |
| `read note` / `write note` | see Notes; `write note` creates a missing note with the content given |

## Notes

Notes are the texts the system keeps on the board, titled as Notes under Board says. `read note <title>` returns the note's content, or says it's missing. `write note <title>` replaces the content, and creates a missing note with the content given. Both take an optional project, for a note kept in a project.

If the backend has documents, use them, found by title. If it doesn't, keep each note in the description of a ticket titled with the note's title, labeled with the `no-autoschedule` label (its real name from Labels) and left open in a plannable status. `ntm:fix-todo-list` never touches it (no sub-tickets, no date) and planners skip it for its label. `read note` is then a title search that reads that ticket's description; `write note` replaces it, creating the ticket when there is none. A note kept in a project is a ticket created in that project. The conventions say every skill ignores such a ticket as work.

## Setup operations

Used by `ntm:configure-board`. Say which call does each.

| Operation | Must say |
| --- | --- |
| `list boards` | the boards the connector can see, by name and id; or, where the backend has no boards to list, say so (the user names or pastes theirs, or `ntm:configure-board` runs `create board`) |
| `create board` | only where the backend has no boards to list: make one with the statuses, labels and notes settled so far, and return its id |
| `list statuses` | a board's status names, so each class can be matched to real names |
| `list labels` | the board's ticket labels, and its project labels when those are a separate set |
| `create label` | an issue label by name, with a description; and a project label by name when those are a separate set |
| `list projects` | every project with its name, id and labels |
| `create project` | a project by name, with the project labels it should carry |
| `create note` | a note with a given title and first content, at board level or in a project, without touching one that already exists (`read note` first). The message history note's first content is its `Keep:` line |

## Writing

Say how a write reports success, so the conventions' retry rule (retry once, then report) can be applied.
