---
name: configure-todo-list
description: >-
    The user's todo list, with them in chat. On a first run, where it lives and
    the agreements ntm works by on it (the backend, the list, the status names
    for each class, the labels, the databases, how planning and shopping work),
    returned as settings. Once configured, a change to those settings. Run from
    ntm:configure, or when the user says "set up my todo list", "connect
    Linear", "rename my labels" or "change how my week is planned".
---

# ntm:configure-todo-list

Settles Todo list, Labels, Planning and Shopping in `ntm-user:settings` with the
user and returns their text. Everything here is an agreement with a proposed
default: show the default in one line, take their answer, record it. Everything
happens in chat, in short rounds: you bring proposals, they react. Never hand
them a form. This skill never writes a file.

Which path runs is a matter of context:

- `ntm-user:settings` won't load, or `ntm:configure` is running this: the setup
  walk, which returns the Todo list, Labels, Planning and Shopping sections.
- Configured: the re-run path (Before you start, step 2), which changes those
  settings: a backend, a label name, the planning rhythm, what counts as a deal.

Reviewing the tasks themselves ("let's review my list", "review the kitchen
project", "estimate the garage work") is `/ntm:review-todo-list`; when the words
are about that, load it and follow it instead.

## Usage

```
/ntm:configure-todo-list [linear|<name>]
```

The backend to use on a first run. Without one, ask (see The backend).

## Before you start

1. Load `ntm:conventions`. On a first run its first step says "not configured;
   run `/ntm:configure`". That's expected: carry on with the values you settle
   here. Its `references/CONTRACT.md` is the contract every backend meets;
   `references/linear.md` is the guide it ships.
2. If `ntm-user:settings` loaded and its Todo list names a backend, this is a
   re-run. Show the current Todo list, Labels, Planning and Shopping sections,
   ask what to change, and go to the step below that owns it; everything else
   stays as it is.
3. Keep a running list of what you've settled. Produce the sections at the end,
   not as you go, so a change of mind costs nothing.

## The backend

Ask what they keep tasks in today. If they're undecided, offer the two choices
in one line: Linear (free for individuals; the guide ntm ships) or their own
backend, which they describe. With no tracker at all, a table in a Claude Doc is
an easy one to build on.

Read the chosen backend's guide (`references/linear.md` under `ntm:conventions`)
now, since the settings don't name it yet, and follow its Setup section in
order; a part the guide ties to a step below waits for that step. Before its
first call, confirm the connector: ToolSearch for the tool the guide's `ping`
names (for their own backend, the tool they name). If it isn't there, ask them
to connect it on the Connectors tab and come back, and stop with
`Configure-todo-list FAILED: <backend> connector not attached`.

### Your own

Backend is the name they give. Walk the contract with them in order: What the
backend needs to have, Todo list, Status classes, each operation under
Operations, Databases, Setup operations, Writing. For each operation, name the
tool and the parameters that carry it out. Read the tool's schema from the
ToolSearch result rather than guessing: which date field is the planned date,
how results paginate, whether labels add or replace, whether a comment can be
edited in place. Where a choice is theirs (which date field, which grouping is a
project), propose one and let them react. Try a read by hand where it's cheap.
The setup operations run below as described; every other write waits for
`/ntm:self-test`.

The contract names the survivable gaps (no estimate field, no blocked-by
relation, no labels on groups, no documents) and the two fatal ones (no date
field, no way to tell open from closed). Say which the backend has. A fatal one
ends here: `Configure-todo-list FAILED: <backend> has no <thing>`. With no
documents, each database lives in the description of an open task titled with
the database's title, as the contract's Databases section says; tell them.

What you settle goes under Todo list as prose, in their words, below its lines
(see Returning the sections): one short paragraph per contract heading.
Statuses, Labels and Databases below then go through the setup operations as
they described them.

## Your tasks

Ask once, plainly: does anyone else use this list? If not, Your tasks is the
default, every task on the list. If so, ask how to tell theirs apart (for
example, assigned to them) and record it in their words.

## Statuses

`list statuses` on the todo list. Propose a mapping from the names you see:
usually a backlog, a to-do and an in-progress status as plannable, the
in-progress one as started; then done, canceled and duplicate. The status `type`
suggests the class; the user confirms. If the todo list has a status that means
"can't move right now", that's blocked. If not, leave blocked blank and say the
$pending-shipment label and blocked-by links cover the same ground.

## Labels

Show the defaults in one table, task labels and project labels, with the
one-line meaning of each from the conventions' System labels: task labels
$no-autoschedule, $pending-shipment, $has-amazon-alert, $amazon-unavailable;
project labels $price-watch, $no-autoschedule. A plain "ok" keeps every name;
record any rename.

Then `list labels`, task and project sets. For each label the todo list lacks,
offer to create it with `create label` under its settled name, with its one-line
meaning as the description. Project labels are their own set where the backend
keeps one: $price-watch and $no-autoschedule as project labels, so projects can
carry them.

Then the price watch project, when one was chosen: create it now with
`create project`, carrying both project labels. If it already exists, make sure
it carries both; the guide says whether `labels` replaces the set.

## Databases

The system keeps its own records in five databases on the todo list, each under
a fixed title: Pauses, Message history, Task review log, Price watch stores,
Amazon alert steps. For each, `read database` by its title. Found: keep it.
Missing: ask whether they already keep it under another title. If so, say to add
that title under Deviations with `/ntm:settings`; if not, create it with
`create database`:

- **pauses:** `## Pauses` with `None.` under it.
- **message history:** its first content is the line
  `Keep: 60 entries or 8 weeks`.
- **task review log:** `## How you work` and `## Estimates`, both empty.
- **price watch stores:** only when a price watch project is named; created in
  that project, with the headings `## Seed`, `## Vouched`, `## Blocked`. Ask for
  a few seed stores by category to put under Seed, with their domains, or leave
  Seed empty and say the first price watch run will report it. Vouched and
  Blocked start empty.
- **Amazon alert steps:** find only. `ntm:sync-price-watch-to-amazon` writes it
  the first time it learns the steps.

## Planning

How `ntm:plan` works the todo list. Show the defaults as one short list, one
line each, and say what each is for in a few words; a plain "ok" keeps them all,
and they change any line in their own words:

- **Rhythm:** one task per weekday. What each planning day gets.
- **Planning days:** weekdays. The days that get a task automatically.
- **Plans ahead:** one week (Monday to Friday). How far the weekly planning
  plans; could be two weeks, or the month.
- **Estimate scale:** asked on its own, below.
- **A day's worth:** about an hour. What a day's picks aim for.
- **Never picks:** $no-autoschedule, $pending-shipment, blocked status. The
  exclusions, each checked on the task and its ancestors; name the labels by the
  names settled above.
- **Parents:** plan the open sub-tasks, never the parent.
- **Weekly message:** what got done, what's still open, the week ahead. The
  halves the weekly planning message carries.

Estimate scale gets its own question, one high-level question: how would they
like to estimate their tasks? Only if they want more detail, ask the estimator
agent's Explain estimating request and pass its ways on; when the agent isn't
available, follow its file as the conventions' "Chat, jobs and agents" says.
Record their answer as Estimate scale, in their words, and as Estimate help
whether they're new to estimating or comfortable with it.

Then ask, once: anything else about how they want planning done? Capture it as
written below the lines ("nothing heavy on Fridays", "garage work only on
weekends"). "Nothing" leaves it blank.

## Shopping

Only when a price watch project was chosen; otherwise skip and return no
Shopping section. How the shopper judges a deal. The same way as Planning, one
line each:

- **Condition:** new, unless a task says otherwise.
- **Delivery:** online only, to their country (from About you).
- **A deal:** at or near the task's target, or well below the usual price. What
  gets them an alert.
- **Amazon interface:** how `/ntm:sync-price-watch-to-amazon` reaches Amazon:
  Claude's built-in browser, their own browser through the Claude extension, or
  off (no Amazon alerts). Blank means it asks.

Then ask, once: anything else about how they shop? Stores they always or never
use go in the price watch stores database (Seed above), not here; this is for
what counts beyond that. Capture it as written below the lines; "nothing" leaves
it blank.

## Returning the sections

Write the sections in exactly these line shapes, the ones `ntm-user:settings`
uses, filled with what you settled. A line may be left blank where the shape
says so. Fill the defaults in where they kept them. For a backend of their own,
the operations prose follows the Todo list lines. Show the sections and let them
react.

```
## Todo list

- Backend: <linear | the name they gave>
- List name: <as the backend names it>
- List id: <blank if the backend needs none>
- Task prefix: <e.g. HOME for HOME-12>
- Your tasks: <default every task on the list; or how to tell theirs apart>
- Statuses — the list's real names for each class:
  - plannable: <one or more names>
  - started: <one of the plannable names>
  - blocked: <blank if the todo list has none>
  - done: <name>
  - canceled: <name>
  - duplicate: <name>
- Price watch project: <project name; blank = price watch off>

<for their own backend: how each operation in the contract is done, in their
words>

## Labels

The real name on your todo list for each label the system uses.

- Task labels:
  - no-autoschedule: <real name; default no-autoschedule>
  - pending-shipment: <real name; default pending-shipment>
  - has-amazon-alert: <real name; default has-amazon-alert>
  - amazon-unavailable: <real name; default amazon-unavailable>
- Project labels (tasks inherit them):
  - price-watch: <real name; default price-watch>
  - no-autoschedule: <real name; default no-autoschedule>

## Planning

How your todo list is planned. Read by `ntm:plan` and the weekly planning;
Estimate scale, Estimate mapping and Estimate help by the estimator agent.

- Rhythm: <default one task per weekday>
- Planning days: <default weekdays>
- Plans ahead: <default one week>
- Estimate scale: <how they estimate their tasks, in their words>
- Estimate mapping: <each estimate on their scale and the list's point it
  becomes; blank when their scale is the list's>
- Estimate help: <new to it | comfortable; default new to it>
- A day's worth: <default about an hour>
- Never picks: <default no-autoschedule, pending-shipment, blocked status>
- Parents: <default plan the open sub-tasks, never the parent>
- Weekly message: <default what got done, what's still open, the week ahead>

<anything else about how they want planning done, as written; or nothing>

## Shopping

How the price watch judges a deal. Read by `ntm:price-watch` and the shopper
agent; Amazon interface by `ntm:sync-price-watch-to-amazon`.

- Condition: <default new>
- Delivery: <default online only, to your country>
- A deal: <default at or near the task's target, or well below the usual price>
- Amazon interface: <default blank>

<anything else about how they shop, as written; or nothing>
```

Then:

- Run from `ntm:configure`: return the sections to the caller, which packages
  once at the end.
- Run directly: load `ntm:settings` and follow its Regenerating
  `ntm-user.plugin` section with the section text you produced.

One more line, for every backend: once `ntm-user` is installed, run
`/ntm:self-test` in a new chat. It starts with `ready-check` and exercises the
operations the jobs use on a throwaway task, and is the smoke test for the
guide. Say it now when run directly. When run from `ntm:configure`, return it
with the sections so `configure` says it at its end.
