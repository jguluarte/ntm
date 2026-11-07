# Claude Docs guide (untested)

**Untested.** Drafted against the Claude Docs connector's guide and a probe doc;
no job has run on it yet.

How each operation named in the conventions is carried out with the Claude Docs
connector (`mcp__Claude_Docs__*` tools). `batch`, `guide` and `update` are
always listed; load `read` with ToolSearch (`select:mcp__Claude_Docs__read`)
before calling it. Before the first docs call of a run,
`guide( items = ["topic.index","topic.editing"] )`: the reads, cell targets, row
inserts and refusal codes used below are defined there. There is no task tracker
here: the todo list is one Claude Doc that Claude keeps, and every operation is
a read or an edit of that doc. Cost: reads pull a whole table, and writes are
row-by-row cell edits, so each run spends more tokens than a connector to a task
tracker would. That's fine for a few dozen tasks.

Values below that name a settings section (Todo list, Labels, About you) come
from `ntm-user:settings`, read as the conventions' Loading step says.

Any call written over several lines here is laid out for reading: send each call
compact (one line, same keys and values), and write any JSON you store on the
todo list compact.

Notation below: `C` = `{"kind":"project","id":"<List id>"}`, carried as
`container` on every call inside the doc. Every `update` on a tab is:

```python
update(
    ref = {
        "object": "node",
        "id": "<tab body id>"
    },
    engine = "prose",
    container = C,
    payload = {
        "ops": […]
    }
)
```

## Todo list

- **Doc:** List name from Todo list is the doc's title; List id is the doc's id,
  the trailing part of its link (`https://claude.ai/artifact/<id>`). Docs can't
  be found by title, so List id is required;
  `read( ref = {"object":"project","id":"<List id>"} )` accepts the id or the
  whole link.
- **Tabs:** tab 1, "Todo list", holds two pipe tables: the task table under
  `## Tasks` (columns Id, Title, Status, Planned date, Labels, Project, Parent,
  Blocked by, Estimate, Done on, Comments) and the projects table under
  `## Projects` (Name, Labels, Summary). Tab 2, "Notes", holds one section per
  note, headed `# <note title>`. The doc read lists the tabs (`files[]`, each
  with its `content.id`, the tab body id); the tab outline
  (`payload = {"projection":"outline"}`) gives the two table ids.
- **Cells:** Id is `<Task prefix>-<n>`. Status is a dropdown chip on the doc's
  Status enum. Planned date and Done on are date chips. Labels and Blocked by
  are comma-separated text; Parent is an id; Project is a project name; Estimate
  is a number. Comments holds the task's comments, one paragraph each,
  `YYYY-MM-DD: text`. There is no description column; a task's description is
  its first Comments line.
- **Projects:** the projects table; a project's Labels cell is comma-separated
  text, and inheritance matches those names against task labels. Task labels and
  project labels are one set of names here.
- **Automations:** none. Nothing closes or dates itself; `ntm:fix-todo-list`
  closes finished parents itself.
- **Missing fields:** no priority (every task's priority is none) and no
  updated-at (blank).

## Status classes

The status names in Todo list are the Status enum's options, in Todo list's
order: the plannable statuses, then blocked (when not blank), done, canceled,
duplicate. A read prints a Status cell as
`<dropdown enum='<enum id>' index='<n>'>Name</dropdown>`; the name is the
status, and its class is the line in Todo list that lists it. Open = any row
whose status is a plannable or blocked name; closed = done, canceled or
duplicate. To write a status, `replace` the cell with a dropdown chip whose
`index` is the option's position: take `<enum id>` from any Status cell, and the
positions from `read( ref = {"object":"enum","id":"<enum id>"}, container = C )`
(its `options[].order`).

## Operations

### `ping`

`read( ref = {"object":"project","id":"<List id>"} )`, then the outline of the
first tab's body. A doc named as List name says whose first tab holds a table
under `## Tasks`: pass. Refused `access`, or no `files[]`: wrong account (the
doc isn't visible to this account; there is no sign-in to expire). Anything
else: backend error.

### `fetch open`

Read the task table in full:

```python
read(
    ref = {
        "object": "node",
        "id": "<tab 1 body id>"
    },
    engine = "prose",
    container = C,
    payload = {
        "kind": "view",
        "parentId": "<task table id>"
    }
)
```

Repeat with `next`'s keys while `complete` is false. Keep the read's `rev` and
each row's position (header is row 0) for the writes below. Keep every row whose
status is a plannable or blocked name. Standard fields from the columns: id,
title, url (the doc's link, `frame.url` of the doc read, the same for every
task), status, status class, priority (none), estimate, planned date (the date
chip's `value`), labels, project, parent id, completed at (Done on), updated at
(blank).

Also read the projects table the same way (`parentId` = its id); Summary is in
the row when a skill asks for it.

### `fetch closed`

The same read, keeping rows whose status is the done name; canceled and
duplicate names only when asked. Done on is the completion date; for a span,
keep rows whose Done on falls in it; for one label, keep rows whose Labels cell
lists it (or whose project's does).

### `read task`

Its row from the fetch: Comments is the description and comments, Parent its
parent, Blocked by its blockers. When a skill reads one task outside a fetch,
`payload = {"kind":"search","text":"<id>"}` gives the row id of every cell
holding the id (its own row, and rows naming it as Parent or Blocked by); then
`{"kind":"view","parentId":"<row id>"}` reads a row alone.

### `list sub-tasks`

Every row of the task table as read for `fetch open` (before the status filter),
open and closed, whose Parent is the id.

### `read comments` / `write comment` / `update comment`

The Comments cell's paragraphs after the first (the first is the description),
dated lines. `write comment`: `insert` after the cell's last paragraph id
(`"side":"after"`, `"as":"markdown"`, content `<TODAY>: <text>`); on an empty
cell, `replace` the cell instead. `update comment`: `replace` the line's words,
with `"as":"text"`, at:

```python
{
    "kind": "find",
    "text": "<the line as read>",
    "within": {
        "kind": "cell",
        "table": "<task table id>",
        "row": <n>,
        "col": 10
    }
}
```

### `set planned date` / `clear planned date`

`replace` the Planned date cell
(`{"kind":"cell","table":"<task table id>","row":<n>,"col":3}`,
`"ifRev":<rev of the read>`) with a date chip:

```json
{
    "with": {
        "as": "markdown",
        "blocks": {
            "d": {
                "type": "date",
                "value": "YYYY-MM-DD"
            }
        },
        "from": {
            "kind": "inline",
            "content": "<?claude block d?>"
        }
    }
}
```

Clear with an empty paragraph: `"blocks":{"empty":{"type":"paragraph"}}` and
content `<?claude block empty?>` (a replace with empty content is refused).
Nothing else in the row changes.

### `set status`

`replace` the Status cell (col 2) with

```python
"blocks": {
    "st": {
        "type": "dropdown",
        "enum": "<enum id>",
        "index": <option position>
    }
}
```

and content `<?claude block st?>`. In the same call, set Done on (col 9) to
today's date chip when the new status is the done, canceled or duplicate name,
and clear it when the new status is plannable or blocked.

### `add labels` / `remove labels`

`replace` the Labels cell (col 4, `"as":"markdown"`) with the cell's current
names plus or minus the given ones, comma-separated. Labels are free text;
nothing to create first.

### `mark duplicate of`

`set status` to the duplicate name (with Done on), and `write comment`
`duplicate of <original id>`.

### `create task`

Check for an existing match by title in the fetched rows first. Id =
`<Task prefix>-<max n in the Id column + 1>`, closed rows included. Append a
row: `insert` on the task table id, `"side":"end"`, `"as":"blocks"`, content one
`row` of eleven `cell`s each holding a `paragraph` (text runs
`{"type":"text","text":"…"}`; an empty paragraph for a blank cell): Id, Title,
blank, blank, Labels, Project, Parent, Blocked by, blank, blank, the description
as a dated first Comments line. Then `set status` on the new row (position `-1`,
the last row, with `ifRev` set to the append's ack `rev`) with the first
plannable status, and `set planned date` when one is given.

### `update task`

`replace` only the cells the skill changes: Title (col 1), Estimate (col 8),
Project (col 5; empty paragraph for none), Parent (col 6), or Blocked by (col 7,
the current ids plus the new one). The description is the first Comments line:
`replace` its first paragraph as `update comment` does. Nothing else changes.

## Notes

Every note is a section on tab 2 (body id from the doc read's second `files[]`
entry), headed `# <note title>` and running to the next level-1 heading or the
end of the tab. The note's own `##` headings nest under it unchanged. A project
is ignored: a note "kept in a project" lives on tab 2 like the rest.

### `read note`

Read tab 2 in full (`payload = {"kind":"view"}`), find the `heading='1'` block
whose text is the note's title, and return the blocks after it up to the next
`heading='1'`. No such heading means the note is missing.

### `write note`

In one `update`, `delete` the section's current blocks
(`{"kind":"blocks","ids":[…]}` with `"ifRev":<rev of the read>`), then `insert`
the new content with `"side":"end"` on the heading's id (`"as":"markdown"`).
When the note is missing, create it as `create note` does, with the content
given as its content (not only a `Keep:` line; the content for the message
history note already starts with its `Keep:` line).

## Setup

Used by `ntm:configure-todo-list`, in order, except that The statuses, The
labels and The notes run at its Statuses, Labels and Notes steps.

### The backend

Say first that this guide is untested. Backend is `claude-docs`.

### The todo list

The todo list is one Claude Doc that Claude reads and edits itself. There are no
todo lists to list. If they already have a todo list doc, List id is the
trailing part of the link they paste and List name the doc's title. Otherwise
propose a title, create the doc with `create todo-list` once Statuses, Labels
and Notes are settled (it's built from them), and record the id it mints. Task
prefix is whatever they want on their ids. The price watch project is a row in
the doc's projects table: an existing one, a new one made with `create project`,
or none.

### The statuses

A new Claude Doc has no statuses to list: propose the names (for example
Backlog, Todo, In Progress as started, Done, Canceled, Duplicate; blocked only
if they want one) and `create todo-list` makes them.

### The labels

Labels are free text and nothing is created.

### The notes

A new Claude Doc doesn't exist yet at this point: settle the titles only, then
`create todo-list`, which makes a section per note (the message history's
`Keep:` line included). Then `create project` for the price watch project if one
was chosen, and finish the pauses, task review log and price watch stores notes
with `write note`.

## Setup operations

Used by `ntm:configure-todo-list`.

### `list todo-lists`

None; the user pastes the doc's link, or `ntm:configure-todo-list` runs
`create todo-list`.

### `create todo-list`

One `batch` with

```python
container = {
    "kind": "project",
    "create": {
        "name": "<List name>",
        "doc": {
            "markdown": "# Todo list"
        }
    }
}
```

and members, in order: the Status enum (the statuses from Todo list in the order
under Status classes):

```python
{
    "$lid": "s",
    "verb": "create",
    "object": "enum",
    "payload": {
        "value": {
            "name": "Status",
            "options": [
                {
                    "name": "<status>"
                },
                …
            ]
        }
    }
}
```

then an `update` on `$lid:n` inserting at `{"kind":"root"}` `"side":"end"` the
markdown `## Tasks`, the header-only task table, `## Projects` and the
header-only projects table (the enum can't be referenced from the birth's own
`doc.markdown`, hence the separate member); a file
`{"$lid":"f2",…"birthName":"Notes.ldoc"}`, a prose node `$lid:n2` with parent
`$lid:f2` and content `# <note title>` for each note under Todo list (with the
message history note's `Keep:` line under its heading), the `update` pointing
`f2` at `n2`; and the project patch placing `$lid:f` as "Todo list" (`order`
`a0`) and `$lid:f2` as "Notes" (`a1`). The ack's `created.minted` is the doc id:
List id. Give the user its link.

### `list statuses`

The enum read under Status classes (enum id from any Status cell, or the birth
ack's `lids.s`).

### `list labels`

The distinct names across the Labels columns of both tables; one set serves as
task and project labels.

### `create label`

Nothing to create; labels are free text.

### `list projects`

The projects table, read as in `fetch open`; a project's id is its name.

### `create project`

Append a row to the projects table (`insert` `"as":"blocks"` as in
`create task`, three cells: Name, Labels, Summary).

### `create note`

`read note` first; one that exists is left alone. Otherwise `insert`
`# <note title>` plus its first content at `{"kind":"root"}` on tab 2,
`"side":"end"` (`"as":"markdown"`).

## Writing

Every write answers `verdict: allow` with the new `rev` and an outline of what
it wrote; that is success. A refusal changes nothing and names a `code`.
`guard_mismatch` or `cell_none` means the table changed since the read: re-read
the table and resend with the new `rev` and positions; that is the retry. Any
other refusal counts as the failed attempt for the conventions' retry rule.
