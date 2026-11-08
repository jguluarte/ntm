---
name: configure-todo-list
description: >-
    The user's todo list, with them in chat. On a first run, where it lives and
    the agreements ntm works by on it (the backend, the list, the labels, the
    databases, how planning and shopping work), returned as settings. Once
    configured, a change to those settings. Run from ntm:configure, or when the
    user says "set up my todo list", "connect Linear", "rename my labels" or
    "change how my week is planned".
---

# ntm:configure-todo-list

Settles the Todo list, Labels, Planning and Shopping sections of
`ntm-user:settings` with the user and returns their text. Most items are an
agreement with a default: show the default in one line, take their answer,
record it. Work in short chat rounds where you propose and they react; never
hand them a form. This skill writes no files.

Two paths:

- **Setup:** `ntm-user:settings` won't load, or `ntm:configure` is running this
  (even when the settings load). Walk every section below in order.
- **Change:** run any other way, with settings whose Todo list names a backend.
  Changes one agreement, for example a backend, a label name, an excluded label
  or what counts as a deal (Before you start, step 2).

Reviewing the tasks themselves ("let's review my list", "review the kitchen
project", "estimate the garage work") is `/ntm:review-todo-list`: load it and
follow it instead.

## Usage

```
/ntm:configure-todo-list [linear|<name>]
```

The backend to use on a first run. Without one, ask (see The backend).

## Before you start

1. Load `ntm:conventions`. On a first run it reports "not configured; run
   `/ntm:configure`". That's expected: carry on with the values you settle here.
   Its `references/CONTRACT.md` is the contract every backend meets, and
   `references/linear.md` is the guide ntm ships.
2. On the Change path, show the current Todo list, Labels, Planning and Shopping
   sections, ask what to change, and go to the section that owns it. Everything
   else stays as it is.
3. Keep a running list of what you settle, and write the sections only at the
   end, so a change of mind costs nothing.

## The backend

Ask what they keep tasks in today. If they're undecided, offer two choices in
one line: Linear (free for individuals; ntm ships its guide) or a backend of
their own, which they describe. With no tracker at all, a table in a Claude Doc
is an easy one to build on.

Read the chosen backend's guide (`references/linear.md` under `ntm:conventions`)
now, since the settings don't name it yet, and follow its Setup section in
order. A part the guide ties to a section below waits for that section.

Before the guide's first call, check the connector: ToolSearch for the tool the
guide's `ping` names (for their own backend, the tool they name). If it's
missing, ask them to connect it on the Connectors tab and come back, and stop
with:

```
Configure-todo-list FAILED: <backend> connector not attached
```

### Your own

Backend is the name they give. Walk every heading of `CONTRACT.md` with them in
order, including each operation under Operations.

For each operation, name the tool and the parameters that do it. Read them from
the tool's schema in the ToolSearch result rather than guessing: which date
field is the planned date, how results paginate, whether labels add or replace,
whether a comment can be edited in place. Where the choice is theirs (which date
field, which grouping is a project), propose one and let them react. Try a read
by hand where it's cheap. The setup operations run in the sections below; every
other write waits for `/ntm:self-test`.

The contract's What the backend needs to have lists the gaps a backend can live
with (no estimate field, no blocked-by relation, no labels on groups, no
documents) and the two it can't (no date field, no way to tell open from
closed). Tell them which their backend has. A fatal gap ends the run:

```
Configure-todo-list FAILED: <backend> has no <thing>
```

With no documents, each database lives in the description of an open task titled
with the database's title, as the contract's Databases section says; tell them.

Record what you settle as prose under the Todo list lines, in their words, one
short paragraph per contract heading. Their status mapping is the Status classes
paragraph. Statuses, Labels and Databases below then use the setup operations as
they described them.

## Statuses

Nothing to store: each status's class is read from the backend at run time, as
the conventions' Status classes says. Run `list statuses` on the todo list and
show, in one short list, which class each status falls in; the guide says how.
Blocked means a status literally named Blocked. If there's none, say the
$pending-shipment label and blocked-by links cover the same ground.

## Labels

Show the defaults in one table, each with its one-line meaning from the
conventions' System labels: $no-autoschedule, $pending-shipment,
$has-amazon-alert, $amazon-unavailable, $price-watch. A plain "ok" keeps every
name; record any rename.

Then `list labels`, task and project sets. Offer to create each missing label
with `create label`, under its settled name, with its one-line meaning as the
description. Where the backend keeps project labels as their own set,
$price-watch and $no-autoschedule are project labels too, so projects can carry
them.

If a price watch project was chosen, create it now with `create project`,
carrying both project labels. If it already exists, make sure it carries both;
the guide says whether `labels` replaces the set.

## Databases

The system keeps its own records in four databases on the todo list, each under
a fixed title: Pauses, Message history, Task review log, Price watch stores.
`read database` each by its title. Found: keep it. Missing: ask whether they
already keep it under another title. If so, tell them to add that title under
Deviations with `/ntm:settings`; if not, create it with `create database`:

- **pauses:** `## Pauses`, with `None.` under it.
- **message history:** starts with the frontmatter below.
- **task review log:** `## How you work` and `## Estimates`, both empty.
- **price watch stores:** only with a price watch project, and created in it.
  Headings `## Seed`, `## Vouched` and `## Blocked`.

```
---
Keep: 60 entries or 8 weeks
---
```

For Seed, ask for a few stores by category, with their domains, or leave it
empty and say the first price watch run will report it. Vouched and Blocked
start empty.

## Planning

How `ntm:plan` works the todo list. Show the excluded labels default in one
line, with what it's for; a plain "ok" keeps it, and they change it in their own
words:

- **Excluded labels from automatic scheduling:** $no-autoschedule,
  $pending-shipment, by the names settled above. Labels planning never picks,
  each checked on the task and its project.

Estimate pattern is a question, not a default: how would they like to estimate
their tasks? Only if they want more detail, send the estimator agent its Explain
estimating request and pass its ways on; if the agent isn't available, follow
its file as the conventions' "Chat, jobs and agents" says. Their answer, in
their words, is Estimate pattern.

Which days get planned, how many tasks each gets, how big they should be and
what the weekly message covers aren't settings. Each job's prompt says what
differs from the defaults in `ntm:plan`, and `/ntm:configure-schedule` writes it
with the user.

Then ask once: anything else about how they want planning done ("nothing heavy
on Fridays", "garage work only on weekends")? It goes below the lines as
written; "nothing" leaves it blank.

## Shopping

Only with a price watch project; otherwise skip it and return no Shopping
section. How the shopper judges a deal, settled the same way as Planning:

- **Condition:** new, unless a task says otherwise.
- **Delivery:** online only, to their country (from About you).
- **A deal:** at or near the task's target, or well below the usual price. What
  gets them an alert.
- **Amazon interface:** how `/ntm:sync-price-watch-to-amazon` reaches Amazon:
  Claude's built-in browser, their own browser through the Claude extension, or
  off (no Amazon alerts). Blank means it asks.

Then ask once: anything else about how they shop? Stores they always or never
use go in the price watch stores database (Seed above), not here. It goes below
the lines as written; "nothing" leaves it blank.

## Returning the sections

Fill these shapes, the ones `ntm-user:settings` uses, with what you settled,
defaults included where they kept them. Leave a line blank only where its shape
allows it. For their own backend, the operations prose follows the Todo list
lines. Show the sections and let them react.

```
## Todo list

- Backend: <linear | the name they gave>
- List name: <as the backend names it>
- List id: <blank if the backend needs none>

<for their own backend: how each operation in the contract is done, in their
words>

## Labels

The real name on your todo list for each label the system uses.

- no-autoschedule: <real name; default no-autoschedule>
- pending-shipment: <real name; default pending-shipment>
- has-amazon-alert: <real name; default has-amazon-alert>
- amazon-unavailable: <real name; default amazon-unavailable>
- price-watch: <real name; default price-watch>

## Planning

How your todo list is planned. Read by `ntm:plan` and the conventions;
Estimate pattern by the estimator agent.

- Estimate pattern: <how they size their tasks and what to do with that, in
  their words; with the list's point for each estimate when the list needs one>
- Excluded labels from automatic scheduling: <default no-autoschedule,
  pending-shipment>

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

- From `ntm:configure`: return the sections to it; it packages once at the end.
- Run directly: load `ntm:settings` and follow its Regenerating
  `ntm-user.plugin` section with these sections.

Last, for every backend: once `ntm-user` is installed, the user runs
`/ntm:self-test` in a new chat. It starts with `ready-check`, exercises the
operations the jobs use on a throwaway task, and is the smoke test for the
guide. Run directly, tell them now. From `ntm:configure`, return that line with
the sections so `configure` says it at its end.
