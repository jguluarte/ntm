---
name: configure-board
description: Sets up or changes where the user's ntm board lives and the agreements ntm works by on it, in chat: the backend, the board, the status names for each class, the labels, the notes, how planning runs and how the price watch judges a deal. Run from ntm:configure, or when the user says "set up my board", "connect Linear", "use Claude Docs for my board", "use Todoist as my board", "rename my labels", "change how my week is planned" or "change my board settings".
---

# ntm:configure-board

Settles Board, Labels, Planning and Shopping in `ntm-user:settings` with the user and returns their text. Everything here is an agreement with a proposed default: show the default in one line, take their answer, record it. Everything happens in chat, in short rounds: you bring proposals, they react. Never hand them a form. This skill never writes a file.

## Usage

```
/ntm:configure-board [linear|claude-docs|<name>]
```

The backend to use. Without one, ask (see The backend).

## Before you start

1. Load `ntm:conventions`. On a first run its first step says "not configured; run `/ntm:configure`". That's expected: carry on with the values you settle here. Its `references/CONTRACT.md` is the contract every backend meets; `references/linear.md` and `references/claude-docs.md` are the two guides it ships.
2. If `ntm-user:settings` loaded and its Board names a backend, this is a re-run. Show the current Board, Labels, Planning and Shopping sections, ask what to change, and go to the step below that owns it; everything else stays as it is.
3. Keep a running list of what you've settled. Produce the sections at the end, not as you go, so a change of mind costs nothing.

## The backend

Ask what they keep tasks in today. If they're undecided, offer the three choices in one line: Linear (free for individuals; the guide most used), Claude Docs (no ticket system; Claude keeps the board in one doc; untested, and heavier per run), or their own backend, which they describe.

If they chose Linear and don't have it yet, do Linear's Starting from nothing first. Then confirm the connector: ToolSearch for the tool the guide's `ping` names (for their own backend, the tool they name). If it isn't there, ask them to connect it on the Connectors tab and come back, and stop with `Configure-board FAILED: <backend> connector not attached`.

### Linear

Backend is `linear`.

**Starting from nothing.** If they don't have Linear yet, these happen outside the chat, on their side; walk them through in order and wait for "done" before step 1:

1. Sign up at linear.app. The free plan is enough: one workspace, unlimited issues.
2. The new workspace comes with one team; that team is the board. Its key (the few capital letters Linear asks for when naming it, `HOME` for `HOME-12`) becomes Ticket prefix, so pick one they'll be happy reading in reminders.
3. A new team's statuses already match the classes: Backlog, Todo, In Progress, Done, Canceled and Duplicate. Nothing to change. If they want a "can't move right now" status, they add one named Blocked in the team's workflow settings; otherwise the `pending-shipment` label and blocked-by links cover that ground.
4. Connect Linear to Claude: in Claude's settings, the Connectors tab, add Linear and sign in to the workspace. Then come back here and say so.

Labels, the price watch project and the notes don't need making by hand: Labels and Notes below create them.

1. **The board.** `list boards`; propose the team. Board name is its name, Board id its id, Ticket prefix its issue key.
2. **The price watch project.** `list projects`; ask which project holds purchases waiting for a good price, or none (none = price watch off). If they want one that doesn't exist yet, settle its name now; it's created in Labels, once the project labels exist.

### Claude Docs

Say first that this guide is untested. Backend is `claude-docs`.

The board is one Claude Doc that Claude reads and edits itself. There are no boards to list. If they already have a board doc, Board id is the trailing part of the link they paste and Board name the doc's title. Otherwise propose a title, create the doc with `create board` once Statuses, Labels and Notes are settled (it's built from them), and record the id it mints. Ticket prefix is whatever they want on their ids. The price watch project is a row in the doc's projects table: an existing one, a new one made with `create project`, or none.

### Your own

Backend is the name they give. Walk the contract with them in order: What the backend needs to have, Board, Status classes, each operation in the Operations table, Notes, Setup operations, Writing. For each operation, name the tool and the parameters that carry it out. Read the tool's schema from the ToolSearch result rather than guessing: which date field is the planned date, how results paginate, whether labels add or replace, whether a comment can be edited in place. Where a choice is theirs (which date field, which grouping is a project), propose one and let them react. Try a read by hand where it's cheap. The setup operations run below as described; every other write waits for `/ntm:self-test`.

The contract names the survivable gaps (no estimate field, no blocked-by relation, no labels on groups, no documents) and the two fatal ones (no date field, no way to tell open from closed). Say which the backend has. A fatal one ends here: `Configure-board FAILED: <backend> has no <thing>`. With no documents, each note lives in the description of an open ticket titled with the note's title, as the contract's Notes section says; tell them.

What you settle goes under Board as prose, in their words, below the template's lines: one short paragraph per contract heading. Statuses, Labels and Notes below then go through the setup operations as they described them.

## Statuses

`list statuses` on the board. Propose a mapping from the names you see: usually a backlog, a to-do and an in-progress status as plannable, the in-progress one as started; then done, canceled and duplicate. The status `type` suggests the class; the user confirms. If the board has a status that means "can't move right now", that's blocked. If not, leave blocked blank and say the `pending-shipment` label and blocked-by links cover the same ground.

A new Claude Doc has no statuses to list: propose the names (for example Backlog, Todo, In Progress as started, Done, Canceled, Duplicate; blocked only if they want one) and `create board` makes them.

## Labels

Show the defaults in one table, ticket labels and project labels, with the one-line meaning of each from the conventions' System labels: ticket labels `no-autoschedule`, `pending-shipment`, `has-amazon-alert`, `amazon-unavailable`; project labels `price-watch`, `no-autoschedule`. A plain "ok" keeps every name; record any rename.

Then `list labels`, issue and project sets. For each label the board lacks, offer to create it with `create label` under its settled name, with its one-line meaning as the description. Project labels are their own set where the backend keeps one (Linear does): `price-watch` and `no-autoschedule` as project labels, so projects can carry them. On Claude Docs labels are free text and nothing is created.

Then the price watch project, when one was chosen: create it now with `create project`, carrying both project labels. If it already exists, make sure it carries both; the guide says whether `labels` replaces the set.

## Notes

Each note under Board has a title. Show the five defaults in one line (Pauses, Message history, Grooming log, Price watch stores, Amazon alert steps); a plain "ok" keeps them, and they rename any. Then, for each, `read note` by its settled title. Found: keep it. Missing: ask whether a document already holds that thing under another title (record that title) or create it with `create note`:

- **pauses:** `## Pauses` with `None.` under it.
- **message history:** its first content is the line `Keep: 60 entries or 8 weeks`.
- **grooming log:** `## How you work` and `## Estimates`, both empty.
- **price watch stores:** only when a price watch project is named; created in that project, with the headings `## Seed`, `## Vouched`, `## Blocked`. Ask for a few seed stores by category to put under Seed, with their domains, or leave Seed empty and say the first price watch run will report it. Vouched and Blocked start empty.
- **Amazon alert steps:** find only. `ntm:amazon-alerts` writes it the first time it learns the steps.

A new Claude Doc doesn't exist yet at this point: settle the titles only, then `create board`, which makes a section per note (the message history's `Keep:` line included). Then `create project` for the price watch project if one was chosen, and finish the pauses, grooming log and price watch stores notes with `write note`.

## Planning

How the planner works the board. Show the defaults as one short list, one line each, and say what each is for in a few words; a plain "ok" keeps them all, and they change any line in their own words:

- **Rhythm:** one task per weekday. What the planner gives each planning day.
- **Planning days:** weekdays. The days that get a task automatically.
- **Plans ahead:** Monday to Friday. What "the week" means to the weekly planning; could be the next two weeks, or the month.
- **Sizing:** Fibonacci points; 1 finishes in a night, 2 is iffy for one evening, 3 or more is multi-day. What an estimate means on their board; the planner guesses from the title when a ticket has none. On a backend with no estimate field, say the grooming log is the record.
- **A day's worth:** about an hour. What the planner aims for when it picks.
- **Never picks:** `no-autoschedule`, `pending-shipment`, blocked status. The exclusions, each checked on the ticket and its ancestors; name the labels by the names settled above.
- **Parents:** plan the open sub-tickets, never the parent.
- **Weekly message:** what got done, what's still open, the week ahead. The halves the weekly planning message carries.

Then ask, once: anything else about how they want planning done? Capture it as written below the lines ("nothing heavy on Fridays", "garage work only on weekends"). "Nothing" leaves it blank.

## Shopping

Only when a price watch project was chosen; otherwise skip and return no Shopping section. How the shopper judges a deal. The same way as Planning, one line each:

- **Condition:** new, unless a ticket says otherwise.
- **Delivery:** online only, to their country (from About you).
- **A deal:** at or near the ticket's target, or well below the usual price. What gets them an alert.

Then ask, once: anything else about how they shop? Stores they always or never use go in the price watch stores note (Seed above), not here; this is for what counts beyond that. Capture it as written below the lines; "nothing" leaves it blank.

## Returning the sections

Write the sections in exactly these line shapes, the ones the `ntm-user:settings` template uses, filled with what you settled. A line may be left blank where the shape says so. Fill the defaults in where they kept them. For a backend of their own, the operations prose follows the Board lines. Show the sections and let them react.

```
## Board

- Backend: <linear | claude-docs | the name they gave>
- Board name: <as the backend names it>
- Board id: <blank if the backend needs none>
- Ticket prefix: <e.g. HOME for HOME-12>
- Statuses — the board's real names for each class:
  - plannable: <one or more names>
  - started: <one of the plannable names>
  - blocked: <blank if the board has none>
  - done: <name>
  - canceled: <name>
  - duplicate: <name>
- Price watch project: <project name; blank = price watch off>
- Notes — the title of each document the system keeps:
  - pauses: <title; default Pauses>
  - message history: <title; default Message history>
  - grooming log: <title; default Grooming log>
  - price watch stores: <title; default Price watch stores>
  - Amazon alert steps: <title; default Amazon alert steps>

<for their own backend: how each operation in the contract is done, in their words>

## Labels

The real name on your board for each label the system uses.

- Ticket labels:
  - no-autoschedule: <real name; default no-autoschedule>
  - pending-shipment: <real name; default pending-shipment>
  - has-amazon-alert: <real name; default has-amazon-alert>
  - amazon-unavailable: <real name; default amazon-unavailable>
- Project labels (tickets inherit them):
  - price-watch: <real name; default price-watch>
  - no-autoschedule: <real name; default no-autoschedule>

## Planning

How the planner works your board. Read by `ntm:plan`, the planner agent and the weekly planning.

- Rhythm: <default one task per weekday>
- Planning days: <default weekdays>
- Plans ahead: <default Monday to Friday>
- Sizing: <default Fibonacci points; 1 finishes in a night, 2 is iffy for one evening, 3 or more is multi-day>
- A day's worth: <default about an hour>
- Never picks: <default no-autoschedule, pending-shipment, blocked status>
- Parents: <default plan the open sub-tickets, never the parent>
- Weekly message: <default what got done, what's still open, the week ahead>

<anything else about how they want planning done, as written; or nothing>

## Shopping

How the price watch judges a deal. Read by `ntm:price-watch` and the shopper agent.

- Condition: <default new>
- Delivery: <default online only, to your country>
- A deal: <default at or near the ticket's target, or well below the usual price>

<anything else about how they shop, as written; or nothing>
```

Then:

- Run from `ntm:configure`: return the sections to the caller, which packages once at the end.
- Run directly: load `ntm:settings` and follow its Regenerating `ntm-user.plugin` section with the section text you produced.

One more line, for every backend: once `ntm-user` is installed, run `/ntm:self-test` in a new chat. It starts with `ready-check`, exercises every operation Board describes on a throwaway ticket, and is the smoke test for the guide. Say it now when run directly. When run from `ntm:configure`, return it with the sections so `configure` says it at its end.
