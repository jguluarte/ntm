# Claude Docs guide (untested)

**Untested.** Drafted against the Claude Docs connector's guide and a probe doc; no job has run on it yet.

How each operation named in the conventions is carried out with the Claude Docs connector (`mcp__Claude_Docs__*` tools). `batch`, `guide` and `update` are always listed; load `read` with ToolSearch (`select:mcp__Claude_Docs__read`) before calling it. Before the first docs call of a run, `guide( items = ["topic.index","topic.editing"] )`: the reads, cell targets, row inserts and refusal codes used below are defined there. There is no ticket system here: the board is one Claude Doc that Claude keeps, and every operation is a read or an edit of that doc. Cost: reads pull a whole table, and writes are row-by-row cell edits, so each run spends more tokens than a connector to a ticket system would. That's fine for a few dozen tickets.

Values below that name a settings section (Board, Labels, About you) come from `ntm-user:settings`, read as the conventions' Loading step says.

Notation below: `C` = `{"kind":"project","id":"<Board id>"}`, carried as `container` on every call inside the doc. Every `update` on a tab is `update( ref = {"object":"node","id":"<tab body id>"}, engine = "prose", container = C, payload = {"ops":[…]} )`.

## Board

- **Doc:** Board name from Board is the doc's title; Board id is the doc's id, the trailing part of its link (`https://claude.ai/artifact/<id>`). Docs can't be found by title, so Board id is required; `read( ref = {"object":"project","id":"<Board id>"} )` accepts the id or the whole link.
- **Tabs:** tab 1, "Board", holds two pipe tables: the ticket table under `## Tickets` (columns Id, Title, Status, Planned date, Labels, Project, Parent, Blocked by, Estimate, Done on, Notes) and the projects table under `## Projects` (Name, Labels, Summary). Tab 2, "Notes", holds one section per note, headed `# <note title>`. The doc read lists the tabs (`files[]`, each with its `content.id`, the tab body id); the tab outline (`payload = {"projection":"outline"}`) gives the two table ids.
- **Cells:** Id is `<Ticket prefix>-<n>`. Status is a dropdown chip on the doc's Status enum. Planned date and Done on are date chips. Labels and Blocked by are comma-separated text; Parent is an id; Project is a project name; Estimate is a number. Notes holds the ticket's comments, one paragraph each, `YYYY-MM-DD: text`. There is no description column; a ticket's description is its first Notes line.
- **Projects:** the projects table; a project's Labels cell is comma-separated text, and inheritance matches those names against ticket labels. Issue labels and project labels are one set of names here.
- **Automations:** none. Nothing closes or dates itself; `ntm:fix-todo-list` closes finished parents itself.
- **Missing fields:** no priority (every ticket's priority is none) and no updated-at (blank).

## Status classes

The status names in Board are the Status enum's options, in Board's order: the plannable statuses, then blocked (when not blank), done, canceled, duplicate. A read prints a Status cell as `<dropdown enum='<enum id>' index='<n>'>Name</dropdown>`; the name is the status, and its class is the line in Board that lists it. Open = any row whose status is a plannable or blocked name; closed = done, canceled or duplicate. To write a status, `replace` the cell with a dropdown chip whose `index` is the option's position: take `<enum id>` from any Status cell, and the positions from `read( ref = {"object":"enum","id":"<enum id>"}, container = C )` (its `options[].order`).

## Operations

### `ping`

`read( ref = {"object":"project","id":"<Board id>"} )`, then the outline of the first tab's body. A doc named as Board name says whose first tab holds a table under `## Tickets`: pass. Refused `access`, or no `files[]`: wrong account (the doc isn't visible to this account; there is no sign-in to expire). Anything else: backend error.

### `fetch open`

Read the ticket table in full: `read( ref = {"object":"node","id":"<tab 1 body id>"}, engine = "prose", container = C, payload = {"kind":"view","parentId":"<ticket table id>"} )`; repeat with `next`'s keys while `complete` is false. Keep the read's `rev` and each row's position (header is row 0) for the writes below. Keep every row whose status is a plannable or blocked name. Standard fields from the columns: id, title, url (the doc's link, `frame.url` of the doc read, the same for every ticket), status, status class, priority (none), estimate, planned date (the date chip's `value`), labels, project, parent id, completed at (Done on), updated at (blank).

Also read the projects table the same way (`parentId` = its id); Summary is in the row when a skill asks for it.

### `fetch closed`

The same read, keeping rows whose status is the done name; canceled and duplicate names only when asked. Done on is the completion date; for a span, keep rows whose Done on falls in it; for one label, keep rows whose Labels cell lists it (or whose project's does).

### `read ticket`

Its row from the fetch: Notes is the description and comments, Parent its parent, Blocked by its blockers. When a skill reads one ticket outside a fetch, `payload = {"kind":"search","text":"<id>"}` gives the row id of every cell holding the id (its own row, and rows naming it as Parent or Blocked by); then `{"kind":"view","parentId":"<row id>"}` reads a row alone.

### `list sub-tickets`

Every row of the ticket table as read for `fetch open` (before the status filter), open and closed, whose Parent is the id.

### `read comments` / `write comment` / `update comment`

The Notes cell's paragraphs after the first (the first is the description), dated lines. `write comment`: `insert` after the cell's last paragraph id (`"side":"after"`, `"as":"markdown"`, content `<TODAY>: <text>`); on an empty cell, `replace` the cell instead. `update comment`: `replace` the line's words, `{"kind":"find","text":"<the line as read>","within":{"kind":"cell","table":"<ticket table id>","row":<n>,"col":10}}`, `"as":"text"`.

### `set planned date` / `clear planned date`

`replace` the Planned date cell (`{"kind":"cell","table":"<ticket table id>","row":<n>,"col":3}`, `"ifRev":<rev of the read>`) with a date chip: `"with":{"as":"markdown","blocks":{"d":{"type":"date","value":"YYYY-MM-DD"}},"from":{"kind":"inline","content":"<?claude block d?>"}}`. Clear with an empty paragraph: `"blocks":{"empty":{"type":"paragraph"}}` and content `<?claude block empty?>` (a replace with empty content is refused). Nothing else in the row changes.

### `set status`

`replace` the Status cell (col 2) with `"blocks":{"st":{"type":"dropdown","enum":"<enum id>","index":<option position>}}` and content `<?claude block st?>`. In the same call, set Done on (col 9) to today's date chip when the new status is the done, canceled or duplicate name, and clear it when the new status is plannable or blocked.

### `add labels` / `remove labels`

`replace` the Labels cell (col 4, `"as":"markdown"`) with the cell's current names plus or minus the given ones, comma-separated. Labels are free text; nothing to create first.

### `mark duplicate of`

`set status` to the duplicate name (with Done on), and `write comment` `duplicate of <original id>`.

### `create ticket`

Check for an existing match by title in the fetched rows first. Id = `<Ticket prefix>-<max n in the Id column + 1>`, closed rows included. Append a row: `insert` on the ticket table id, `"side":"end"`, `"as":"blocks"`, content one `row` of eleven `cell`s each holding a `paragraph` (text runs `{"type":"text","text":"…"}`; an empty paragraph for a blank cell): Id, Title, blank, blank, Labels, Project, Parent, Blocked by, blank, blank, the description as a dated first Notes line. Then `set status` on the new row (position `-1`, the last row, with `ifRev` set to the append's ack `rev`) with the first plannable status, and `set planned date` when one is given.

### `update ticket`

`replace` only the cells the skill changes: Title (col 1), Estimate (col 8), Project (col 5; empty paragraph for none), Parent (col 6), or Blocked by (col 7, the current ids plus the new one). The description is the first Notes line: `replace` its first paragraph as `update comment` does. Nothing else changes.

## Notes

Every note is a section on tab 2 (body id from the doc read's second `files[]` entry), headed `# <note title>` and running to the next level-1 heading or the end of the tab. The note's own `##` headings nest under it unchanged. A project is ignored: a note "kept in a project" lives on tab 2 like the rest.

- **`read note`:** read tab 2 in full (`payload = {"kind":"view"}`), find the `heading='1'` block whose text is the note's title, and return the blocks after it up to the next `heading='1'`. No such heading means the note is missing.
- **`write note`:** in one `update`, `delete` the section's current blocks (`{"kind":"blocks","ids":[…]}` with `"ifRev":<rev of the read>`), then `insert` the new content with `"side":"end"` on the heading's id (`"as":"markdown"`). When the note is missing, create it as `create note` does, with the content given as its content (not only a `Keep:` line; the content for the message history note already starts with its `Keep:` line).

## Setup operations

Used by `ntm:configure-integration`.

- **`list boards`:** none; the user pastes the doc's link, or `ntm:configure-integration` runs `create board`.
- **`create board`:** one `batch` with `container = {"kind":"project","create":{"name":"<Board name>","doc":{"markdown":"# Board"}}}` and members, in order: the Status enum (`{"$lid":"s","verb":"create","object":"enum","payload":{"value":{"name":"Status","options":[{"name":"<status>"},…]}}}`, the statuses from Board in the order under Status classes); an `update` on `$lid:n` inserting at `{"kind":"root"}` `"side":"end"` the markdown `## Tickets`, the header-only ticket table, `## Projects` and the header-only projects table (the enum can't be referenced from the birth's own `doc.markdown`, hence the separate member); a file `{"$lid":"f2",…"birthName":"Notes.ldoc"}`, a prose node `$lid:n2` with parent `$lid:f2` and content `# <note title>` for each note under Board (with the message history note's `Keep:` line under its heading), the `update` pointing `f2` at `n2`; and the project patch placing `$lid:f` as "Board" (`order` `a0`) and `$lid:f2` as "Notes" (`a1`). The ack's `created.minted` is the doc id: Board id. Give the user its link.
- **`list statuses`:** the enum read under Status classes (enum id from any Status cell, or the birth ack's `lids.s`).
- **`list labels`:** the distinct names across the Labels columns of both tables; one set serves as issue and project labels.
- **`create label`:** nothing to create; labels are free text.
- **`list projects`:** the projects table, read as in `fetch open`; a project's id is its name.
- **`create project`:** append a row to the projects table (`insert` `"as":"blocks"` as in `create ticket`, three cells: Name, Labels, Summary).
- **`create note`:** `read note` first; one that exists is left alone. Otherwise `insert` `# <note title>` plus its first content at `{"kind":"root"}` on tab 2, `"side":"end"` (`"as":"markdown"`).

## Writing

Every write answers `verdict: allow` with the new `rev` and an outline of what it wrote; that is success. A refusal changes nothing and names a `code`. `guard_mismatch` or `cell_none` means the table changed since the read: re-read the table and resend with the new `rev` and positions; that is the retry. Any other refusal counts as the failed attempt for the conventions' retry rule.
