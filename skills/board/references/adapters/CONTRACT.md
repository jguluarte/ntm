# Adapter contract

An adapter maps the operations the board rules name onto one tracker's connector. `linear.md` is the complete, tested one. `claude-docs.md` is the second shipped adapter, for a board kept in a Claude Doc with no tracker connector at all: untested, and heavier per run (every read pulls a whole table and every write edits a row), fine for a few dozen tickets. To support another tracker, `nudge:adapter` drafts `<tracker>.md` in this folder with the user, following this contract, marks it Untested, and runs a smoke test against their board; the mark becomes `Tested on <date>` when the test passes.

Write an adapter as a list of operations, each saying which tool calls carry it out and which fields map to the board rules' names. Keep the headings below so skills can find what they need.

## What the tracker needs to have

- Tickets with: an id, a title, a description, a status, labels, a single date field usable as the planned date, a parent/sub-ticket relation, and a web url. An estimate field and a blocked-by relation are used when present; say in the adapter if the tracker lacks them, and the skills that use them (grooming, planning) work from titles and descriptions instead. With no estimate field, the grooming log's Estimates block is the record: a ticket counts as groomed when it has an entry there, `update ticket` skips the estimate, and the log keeps every entry rather than the newest 150.
- Some way to group tickets (projects, folders, epics) that can carry labels. If groups can't carry labels, say so; the board rules' project-label inheritance then doesn't apply, and the user puts system labels on tickets directly.
- A connector for Claude that can list, read and write the above.

Some gaps are survivable: no estimate field, no blocked-by relation, no labels on groups, no priority, no updated-at, no documents (see Notes), no way to keep a note inside a project (then every note is at board level). The adapter says which it lacks, and the skills work around them as above. Two aren't: a tracker with no date field to use as the planned date, or no way to tell open tickets from closed, can't run this system.

## Board

Name the board (the config's `board name`), what id it needs, and which automations the tracker runs on parent/sub-ticket closing, if any. If the tracker has no unit above projects, the board is the whole account (`board name` is what the tracker calls it, `board id` blank). If ids carry no prefix, `ticket prefix` is blank and ids are the tracker's own; `(ABC-12)` in the rules then means the bare id.

## Status classes

Say how the config's status names are used to filter and to write, and how to tell open from closed in results. A tracker with no status names, only open and closed, records `plannable statuses` as `open`, `done status` as `closed`, and the started, blocked, canceled and duplicate rows as blank; the classes those rows name then don't exist on this board, and `set status` to done closes the ticket.

## Operations

Each must be covered.

| Operation | Must say |
| --- | --- |
| `ping` | one read that proves the connector works and sees the configured board, and how to tell sign-in expired from wrong account from tracker error (the names nudge:ping reports) |
| `fetch open` | how to get every open ticket (every plannable status, plus blocked when the config's `blocked status` isn't blank) with the standard fields, paginated, plus every group with its name and labels, and its summary when a skill asks for it. Standard fields: id, title, url (the ticket's link), status, status class, priority, estimate, planned date, labels, project, parent id, completed at, updated at; and, for priority, which value is highest and which means none |
| `fetch closed` | closed tickets (done; canceled and duplicate on request) with their completion time, how to limit to a span, and how to limit to one label |
| `read ticket` | one ticket with description, parent and blocked-by relations |
| `list sub-tickets` | a ticket's sub-tickets, open and closed, with the standard fields |
| `read comments` / `write comment` / `update comment` | per ticket; if the tracker can't update a comment in place, say to delete and re-add, or to append |
| `set planned date` / `clear planned date` | the date field used, and that nothing else changes |
| `set status` | by configured status name |
| `add labels` / `remove labels` | without dropping the others |
| `mark duplicate of` | or, if the tracker has no duplicate relation, close with the duplicate status and a comment naming the original |
| `create ticket` | title, description, project, parent, blocked-by, labels; and how to check for an existing match first |
| `update ticket` | change a ticket's title, description, estimate, project (or none), parent, or add a blocked-by link; nothing else changes |
| `read note` / `write note` | see Notes |

## Notes

Notes are the shared texts the system keeps on the board (the config's Notes section). `read note <name>` returns the note's content, or says it's missing. `write note <name>` replaces the content, and creates the note when it's missing. Both take an optional project, for a note kept in a project.

If the tracker has documents, use them, found by title. If it doesn't, keep each note in the description of a ticket titled with the note's configured name, labeled with the `no-autoschedule label` and left open in a plannable status. Cleanup never touches it (no sub-tickets, no date) and planners skip it for its label. `read note` is then a title search that reads that ticket's description; `write note` replaces it, creating the ticket when there is none; a note kept in a project is a ticket created in that project. The board rules say every skill ignores such a ticket as work.

## Setup operations

Used by `nudge:setup` only: `list boards`, `list statuses` (a board's status names), `list labels`, `create label`, `create project`, `create board` (only where the tracker has no boards to list; `list boards` then says so). Say which call does each.

## Writing

Say how a write reports success, so the board rules' retry rule (retry once, then report) can be applied.
