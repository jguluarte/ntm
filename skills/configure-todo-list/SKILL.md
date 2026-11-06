---
name: configure-todo-list
description: The user's todo list, with them in chat. On a first run, where it lives and the agreements ntm works by on it (the backend, the list, the status names for each class, the labels, the notes, how planning and shopping work), returned as settings. Once configured, grooming: closes obsolete or duplicate tickets, then sizes and splits ungroomed ones with their approval; or a change to those settings. Run from ntm:configure, or when the user says "set up my todo list", "connect Linear", "let's groom", "review the kitchen project", "rename my labels" or "change how my week is planned".
---

# ntm:configure-todo-list

One interactive skill for the user's todo list, in two parts. Which part runs is a matter of context:

- `ntm-user:settings` won't load, or `ntm:configure` is running this: **Part 1, Where your list lives**: the setup walk, which returns the Todo list, Labels, Planning and Shopping sections.
- Configured, and the words are about where the list lives or how it's worked (a backend, a label name, the planning rhythm, what counts as a deal): Part 1's re-run path, which changes those settings.
- Configured, and the words are about the tickets themselves ("let's groom", "review the kitchen project", "size the garage work"), or there are no words: **Part 2, Grooming**.

Both parts happen in chat, in short rounds: you bring proposals, they react. Never hand them a form.

# Part 1: Where your list lives

Settles Todo list, Labels, Planning and Shopping in `ntm-user:settings` with the user and returns their text. Everything here is an agreement with a proposed default: show the default in one line, take their answer, record it. Everything happens in chat, in short rounds: you bring proposals, they react. Never hand them a form. This skill never writes a file.

## Usage

```
/ntm:configure-todo-list [linear|claude-docs|<name>]
```

The backend to use on a first run. Without one, ask (see The backend).

## Before you start

1. Load `ntm:conventions`. On a first run its first step says "not configured; run `/ntm:configure`". That's expected: carry on with the values you settle here. Its `references/CONTRACT.md` is the contract every backend meets; `references/linear.md` and `references/claude-docs.md` are the two guides it ships.
2. If `ntm-user:settings` loaded and its Todo list names a backend, this is a re-run. Show the current Todo list, Labels, Planning and Shopping sections, ask what to change, and go to the step below that owns it; everything else stays as it is.
3. Keep a running list of what you've settled. Produce the sections at the end, not as you go, so a change of mind costs nothing.

## The backend

Ask what they keep tasks in today. If they're undecided, offer the three choices in one line: Linear (free for individuals; the guide most used), Claude Docs (no ticket system; Claude keeps the todo list in one doc; untested, and heavier per run), or their own backend, which they describe.

If they chose Linear and don't have it yet, do Linear's Starting from nothing first. Read the chosen backend's guide (`references/linear.md` or `references/claude-docs.md` under `ntm:conventions`) now, since the settings don't name it yet. Then confirm the connector: ToolSearch for the tool the guide's `ping` names (for their own backend, the tool they name). If it isn't there, ask them to connect it on the Connectors tab and come back, and stop with `Configure-todo-list FAILED: <backend> connector not attached`.

### Linear

Backend is `linear`.

**Starting from nothing.** If they don't have Linear yet, these happen outside the chat, on their side; walk them through in order and wait for "done" before The todo list below:

1. Sign up at linear.app. The free plan is enough: one workspace, unlimited issues.
2. The new workspace comes with one team; that team is the todo list. Its key (the few capital letters Linear asks for when naming it, `HOME` for `HOME-12`) becomes Ticket prefix, so pick one they'll be happy reading in reminders.
3. A new team's statuses already match the classes: Backlog, Todo, In Progress, Done, Canceled and Duplicate. Nothing to change. If they want a "can't move right now" status, they add one named Blocked in the team's workflow settings; otherwise the `pending-shipment` label and blocked-by links cover that ground.
4. Connect Linear to Claude: in Claude's settings, the Connectors tab, add Linear and sign in to the workspace. Then come back here and say so.

Labels, the price watch project and the notes don't need making by hand: Labels and Notes below create them.

1. **The todo list.** `list todo-lists`; propose the team. List name is its name, List id its id, Ticket prefix its issue key.
2. **The price watch project.** `list projects`; ask which project holds purchases waiting for a good price, or none (none = price watch off). If they want one that doesn't exist yet, settle its name now; it's created in Labels, once the project labels exist.

### Claude Docs

Say first that this guide is untested. Backend is `claude-docs`.

The todo list is one Claude Doc that Claude reads and edits itself. There are no todo lists to list. If they already have a todo list doc, List id is the trailing part of the link they paste and List name the doc's title. Otherwise propose a title, create the doc with `create todo-list` once Statuses, Labels and Notes are settled (it's built from them), and record the id it mints. Ticket prefix is whatever they want on their ids. The price watch project is a row in the doc's projects table: an existing one, a new one made with `create project`, or none.

### Your own

Backend is the name they give. Walk the contract with them in order: What the backend needs to have, Todo list, Status classes, each operation in the Operations table, Notes, Setup operations, Writing. For each operation, name the tool and the parameters that carry it out. Read the tool's schema from the ToolSearch result rather than guessing: which date field is the planned date, how results paginate, whether labels add or replace, whether a comment can be edited in place. Where a choice is theirs (which date field, which grouping is a project), propose one and let them react. Try a read by hand where it's cheap. The setup operations run below as described; every other write waits for `/ntm:self-test`.

The contract names the survivable gaps (no estimate field, no blocked-by relation, no labels on groups, no documents) and the two fatal ones (no date field, no way to tell open from closed). Say which the backend has. A fatal one ends here: `Configure-todo-list FAILED: <backend> has no <thing>`. With no documents, each note lives in the description of an open ticket titled with the note's title, as the contract's Notes section says; tell them.

What you settle goes under Todo list as prose, in their words, below the template's lines: one short paragraph per contract heading. Statuses, Labels and Notes below then go through the setup operations as they described them.

## Statuses

`list statuses` on the todo list. Propose a mapping from the names you see: usually a backlog, a to-do and an in-progress status as plannable, the in-progress one as started; then done, canceled and duplicate. The status `type` suggests the class; the user confirms. If the todo list has a status that means "can't move right now", that's blocked. If not, leave blocked blank and say the `pending-shipment` label and blocked-by links cover the same ground.

A new Claude Doc has no statuses to list: propose the names (for example Backlog, Todo, In Progress as started, Done, Canceled, Duplicate; blocked only if they want one) and `create todo-list` makes them.

## Labels

Show the defaults in one table, ticket labels and project labels, with the one-line meaning of each from the conventions' System labels: ticket labels `no-autoschedule`, `pending-shipment`, `has-amazon-alert`, `amazon-unavailable`; project labels `price-watch`, `no-autoschedule`. A plain "ok" keeps every name; record any rename.

Then `list labels`, ticket and project sets. For each label the todo list lacks, offer to create it with `create label` under its settled name, with its one-line meaning as the description. Project labels are their own set where the backend keeps one (Linear does): `price-watch` and `no-autoschedule` as project labels, so projects can carry them. On Claude Docs labels are free text and nothing is created.

Then the price watch project, when one was chosen: create it now with `create project`, carrying both project labels. If it already exists, make sure it carries both; the guide says whether `labels` replaces the set.

## Notes

Each note under Todo list has a title. Show the five defaults in one line (Pauses, Message history, Grooming log, Price watch stores, Amazon alert steps); a plain "ok" keeps them, and they rename any. Then, for each, `read note` by its settled title. Found: keep it. Missing: ask whether a note already exists under another title (record that title) or create it with `create note`:

- **pauses:** `## Pauses` with `None.` under it.
- **message history:** its first content is the line `Keep: 60 entries or 8 weeks`.
- **grooming log:** `## How you work` and `## Estimates`, both empty.
- **price watch stores:** only when a price watch project is named; created in that project, with the headings `## Seed`, `## Vouched`, `## Blocked`. Ask for a few seed stores by category to put under Seed, with their domains, or leave Seed empty and say the first price watch run will report it. Vouched and Blocked start empty.
- **Amazon alert steps:** find only. `ntm:sync-price-watch-to-amazon` writes it the first time it learns the steps.

A new Claude Doc doesn't exist yet at this point: settle the titles only, then `create todo-list`, which makes a section per note (the message history's `Keep:` line included). Then `create project` for the price watch project if one was chosen, and finish the pauses, grooming log and price watch stores notes with `write note`.

## Planning

How the planner works the todo list. Show the defaults as one short list, one line each, and say what each is for in a few words; a plain "ok" keeps them all, and they change any line in their own words:

- **Rhythm:** one task per weekday. What the planner gives each planning day.
- **Planning days:** weekdays. The days that get a task automatically.
- **Plans ahead:** one week (Monday to Friday). How far the weekly planning plans; could be two weeks, or the month.
- **Sizing:** Fibonacci points; 1 finishes in a night, 2 is iffy for one evening, 3 or more is multi-day. What an estimate means on their todo list; the planner guesses from the title when a ticket has none. On a backend with no estimate field, say the grooming log is the record.
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
- **Amazon interface:** how `/ntm:sync-price-watch-to-amazon` reaches Amazon: Claude's built-in browser, their own browser through the Claude extension, or off (no Amazon alerts). Blank means it asks.

Then ask, once: anything else about how they shop? Stores they always or never use go in the price watch stores note (Seed above), not here; this is for what counts beyond that. Capture it as written below the lines; "nothing" leaves it blank.

## Returning the sections

Write the sections in exactly these line shapes, the ones the `ntm-user:settings` template uses, filled with what you settled. A line may be left blank where the shape says so. Fill the defaults in where they kept them. For a backend of their own, the operations prose follows the Todo list lines. Show the sections and let them react.

```
## Todo list

- Backend: <linear | claude-docs | the name they gave>
- List name: <as the backend names it>
- List id: <blank if the backend needs none>
- Ticket prefix: <e.g. HOME for HOME-12>
- Statuses — the list's real names for each class:
  - plannable: <one or more names>
  - started: <one of the plannable names>
  - blocked: <blank if the todo list has none>
  - done: <name>
  - canceled: <name>
  - duplicate: <name>
- Price watch project: <project name; blank = price watch off>
- Notes — the title of each note the system keeps:
  - pauses: <title; default Pauses>
  - message history: <title; default Message history>
  - grooming log: <title; default Grooming log>
  - price watch stores: <title; default Price watch stores>
  - Amazon alert steps: <title; default Amazon alert steps>

<for their own backend: how each operation in the contract is done, in their words>

## Labels

The real name on your todo list for each label the system uses.

- Ticket labels:
  - no-autoschedule: <real name; default no-autoschedule>
  - pending-shipment: <real name; default pending-shipment>
  - has-amazon-alert: <real name; default has-amazon-alert>
  - amazon-unavailable: <real name; default amazon-unavailable>
- Project labels (tickets inherit them):
  - price-watch: <real name; default price-watch>
  - no-autoschedule: <real name; default no-autoschedule>

## Planning

How the planner works your todo list. Read by `ntm:plan`, the planner agent and the weekly planning.

- Rhythm: <default one task per weekday>
- Planning days: <default weekdays>
- Plans ahead: <default one week>
- Sizing: <default Fibonacci points; 1 finishes in a night, 2 is iffy for one evening, 3 or more is multi-day>
- A day's worth: <default about an hour>
- Never picks: <default no-autoschedule, pending-shipment, blocked status>
- Parents: <default plan the open sub-tickets, never the parent>
- Weekly message: <default what got done, what's still open, the week ahead>

<anything else about how they want planning done, as written; or nothing>

## Shopping

How the price watch judges a deal. Read by `ntm:price-watch` and the shopper agent; Amazon interface by `ntm:sync-price-watch-to-amazon`.

- Condition: <default new>
- Delivery: <default online only, to your country>
- A deal: <default at or near the ticket's target, or well below the usual price>
- Amazon interface: <default blank>

<anything else about how they shop, as written; or nothing>
```

Then:

- Run from `ntm:configure`: return the sections to the caller, which packages once at the end.
- Run directly: load `ntm:settings` and follow its Regenerating `ntm-user.plugin` section with the section text you produced.

One more line, for every backend: once `ntm-user` is installed, run `/ntm:self-test` in a new chat. It starts with `ready-check` and exercises the operations the jobs use on a throwaway ticket, and is the smoke test for the guide. Say it now when run directly. When run from `ntm:configure`, return it with the sections so `configure` says it at its end.

# Part 2: Grooming

## Why this exists

Daily reminders only help when they point at something the user could pick up. Grooming gets tickets there, and it has to stay cheap enough that the user keeps doing it: if it turns into a process, they'll stop. When in doubt, take the lighter option:

- **A short session is a good session.** One project, or three items, is fine. Stop the moment the user wants to, and never push for more.
- **You bring proposals; the user reacts.** Never make them fill in fields, and never hit them with a list of questions.
- **Good enough reminders complete.** A ticket can be rough, or just a checklist, as long as the user says it's adequate.
- **The user drives the wording.** Your unvetted wording tends toward filler, so propose enough, keep it short, and never expand their descriptions unless they ask.

## Setup

1. Load `ntm:conventions`, and compute `TODAY` as its Dates section says.
2. Read the grooming log (see below).
3. Fetch every open ticket and list the projects, both as the conventions' Fetching says. Add each project's summary to the project fields, as the guide says.

A ticket is **ungroomed** when it's open, has no estimate, and isn't a parent with open sub-tickets. On a backend without an estimate field (its guide or Todo list in your settings says), "no estimate" means no entry in the log's Estimates block.

## The slice

The user names what to groom however they like: a project, part of one, a few tickets, or something already groomed that they want to look at again. Take what they say.

If they don't name one, use what Setup fetched to propose one project, with a one-line reason such as how much is left ungroomed. Go once they agree.

Tickets with no project get grouped by likeness and groomed a group at a time. A group can also be a reason to propose a project to file it under, even a new one.

## 1. Overview

Clear out what doesn't belong before looking at details. Look over every open ticket in the slice by title, reading a description only where the title isn't enough. Also skim the titles in projects whose names or topics overlap with the slice, for tickets logged twice or filed in the wrong place.

Propose, as one numbered list, one short line each, only for tickets you'd change:

- **Close as obsolete:** canceled, or done if it looks like it already happened, with the guide's `set status`.
- **Duplicates:** identify all of the tickets that are ultimately duplicated, and quote anything that appears only on a specific one. You can propose what to do, but the user has the final say. On approval, do what they say and close the other(s) with the guide's `mark duplicate of`.
- **Move:** to the project it belongs in, or to none, with the guide's `update ticket`.

A plain "ok" approves the whole list; the user can strike items by number. If nothing stands out, say so in one line and move on. Write what they approve as soon as they approve it.

## 2. Order of operations

Read the slice's ungroomed tickets, plus any groomed ones the user named, and their parent chains, with the guide's `read ticket`. For a blocked ticket with no blocked-by link, check its comments (`read comments`) for what it waits on.

Propose an order to groom them in, as a short list of ids and titles. Blockers come before what they block. When a ticket waits on something outside the slice:

- If the blocker has an obvious end state ("the desk is clear"), groom the ticket anyway, assuming that end state, and mention that when you present it.
- Otherwise ask the user about it when you reach it.

If much of the slice waits on another project, say so and offer to start there instead. The user adjusts the order however they like, then you start.

## 3. Ticket by ticket

One item per message, in the agreed order:

1. The id linked to its URL, and the title.
2. Your proposed **estimate**, with a few words on why, guided by how past guesses in the grooming log compared with what the user settled on. If it already has one (on a backend without an estimate field, its latest log entry's `final`), say what it is.
3. If it's a 3 or more, one line on whether it looks like it splits. Some things can't, and that's fine. Pieces come up in the talk that follows (see Splits).
4. Usually no edits. Suggest one or two at most, only where the ticket would otherwise be hard to start: a title that doesn't say what it is, or a blocker that isn't linked. Show the exact new text, and write only what the user saw.
5. The description, exactly as written.

Make it one proposal: a plain "ok" approves all of it, and the user changes any part in their own words. They'll very likely want to talk most tickets through, so do that. If it splits, the estimate is for what's left of the original; if the split came after your guess, re-propose for what's left and log that as `guess`. "Skip" leaves the ticket ungroomed for another day.

Once a ticket is settled, write it with the guide's `update ticket` (estimate, and any approved title, description or blocked-by link) and update the log. Do both in the same turn that presents the next ticket (or ends the session), so writes never make the user wait.

### Splits

- The user usually brings their own split ideas. Propose pieces only when they don't; otherwise just check whether they missed something obvious.
- Split pieces off as new tickets, and leave the original with its reduced scope. Show the exact text for the original's reduced scope and each new title, and write only that: the original with the guide's `update ticket`, the new tickets as the next bullet says. New tickets get the original's project and parent. When the order matters, the later ticket is blocked by the earlier one. Don't default to sub-tickets.
- Write new tickets with the guide's `create ticket`, the way the conventions' "Creating tickets when the user asks" section says. They join the end of the grooming order un-estimated, unless the user asks to do them next.

## The grooming log

The grooming log note, titled as Notes under Todo list in your settings says. It's yours: it's how you learn to work better with the user over time. Read it with the guide's `read note`. When it's missing, `write note` creates it with the two sections below.

### `## How you work`

Short bullets about the user, written to them (it's their note too), on whatever would help you do better with them next time: how they like tickets written and split, how they like sessions to go, and what they keep correcting. Learn from what they change, push back on or say. When something would apply again, fold it in: rewrite and merge bullets rather than appending, and keep the section to about 20 bullets.

### `## Estimates`

A `jsonl` code block, newest first, one object per approved estimate:

```jsonl
{"date": "YYYY-MM-DD", "id": "ABC-12", "guess": 2, "final": 3, "why": "wiring took longer than it looked"}
```

`guess` is what you proposed and `final` what the user approved. Keep `why` to a few words: what made them change it, or what made the guess right. Keep the newest 150 entries. On a backend without an estimate field the log is the only record of what's groomed, so keep every entry.

Save it with `write note` whenever you change it, leaving the rest as it was.

## Ending

When the user stops, or the slice is done, fold anything you learned into `## How you work` and save the log, then sum up in a line or two: how many items were groomed, closed and split, and what's still ungroomed in the slice.
