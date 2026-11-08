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

Settles Todo list, Labels, Planning and Shopping in `ntm-user:settings` with the
user and returns their text. Everything here is an agreement with a proposed
default: show the default in one line, take their answer, record it. Everything
happens in chat, in short rounds: you bring proposals, they react. Never hand
them a form. This skill never writes a file.

Which path runs is a matter of context:

- `ntm-user:settings` won't load, or `ntm:configure` is running this: the setup
  walk, which returns the Todo list, Labels, Planning and Shopping sections.
- Configured: the re-run path (Before you start, step 2), which changes those
  settings: a backend, a label name, an excluded label, what counts as a deal.

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
   here. There is a predefined guide for linear.app, as well as the contract
   required to use a different backend.
    - If using Linear: `references/linear.md`
    - Otherwise use `references/backend-contract.md`
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
names. If it isn't there, ask them to connect it on the Connectors tab and come
back, and stop with
`Configure-todo-list FAILED: <backend> connector not attached`.

For their own backend, go through the contract with them before Statuses. Its
section Setting something up with the user says how. After that, Statuses,
Labels and Databases do their steps with the tools they named for the setup
operations.

## Statuses

Nothing to store: each status's class is read from the backend at run time, as
the conventions' Status classes says. `list statuses` on the todo list and show
in one short list which class each status falls in (the guide says how). Blocked
is the status named Blocked. For their own backend, the mapping they gave goes
in the Status classes paragraph under Todo list (see Returning the sections). If
there's no blocked status, say the $pending-shipment label and blocked-by links
cover the same ground.

## Labels

Show the defaults in one table, with the one-line meaning of each from the
conventions' System labels: $no-autoschedule, $pending-shipment,
$has-amazon-alert, $amazon-unavailable, $price-watch. A plain "ok" keeps every
name; record any rename.

Then `list labels`, task and project sets. For each label the todo list lacks,
offer to create it with `create label` under its settled name, with its one-line
meaning as the description. Project labels are their own set where the backend
keeps one: $price-watch and $no-autoschedule as project labels, so projects can
carry them.

Then the price watch project, when one was chosen: create it now with
`create project`, carrying both project labels. If it already exists, make sure
it carries both; the guide says whether `labels` replaces the set.

## Databases

The system keeps its own records in four databases on the todo list, each under
a fixed title: Pauses, Message history, Task review log, Price watch stores. For
each, `read database` by its title. Found: keep it. Missing: ask whether they
already keep it under another title. If so, say to add that title under
Deviations with `/ntm:settings`; if not, create it with `create database`:

- **pauses:** `## Pauses` with `None.` under it.
- **message history:** its first content is this frontmatter:

    ```
    ---
    Keep: 60 entries or 8 weeks
    ---
    ```

- **task review log:** `## How you work` and `## Estimates`, both empty.
- **price watch stores:** only when a price watch project was chosen; created in
  that project, with the headings `## Seed`, `## Vouched`, `## Blocked`. Ask for
  a few seed stores by category to put under Seed, with their domains, or leave
  Seed empty and say the first price watch run will report it. Vouched and
  Blocked start empty.

## Planning

How `ntm:plan` works the todo list. Show the defaults as one short list, one
line each, and say what each is for in a few words; a plain "ok" keeps them all,
and they change any line in their own words:

- **Estimate pattern:** asked on its own, below.
- **Excluded labels from automatic scheduling:** $no-autoschedule,
  $pending-shipment. Labels planning never picks, each checked on the task and
  its project; name the labels by the names settled above.

Which days get planned, how many tasks each gets, how big they should be and
what the weekly message covers aren't settings: each job's prompt says what
differs from the defaults in `ntm:plan`, and `/ntm:configure-schedule` writes it
with the user.

Estimate pattern gets its own question, one high-level question: how would they
like to estimate their tasks? Only if they want more detail, ask the estimator
agent's Explain estimating request and pass its ways on; when the agent isn't
available, follow its file as the conventions' "Chat, jobs and agents" says.
Record their answer as Estimate pattern, in their words.

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

<for their own backend: how each operation in the contract is done, in their
words, one short paragraph per contract heading>

## Labels

The real name on your todo list for each label the system uses.

- no-autoschedule: <real name; default no-autoschedule>
- pending-shipment: <real name; default pending-shipment>
- has-amazon-alert: <real name; default has-amazon-alert>
- amazon-unavailable: <real name; default amazon-unavailable>
- price-watch: <real name; default price-watch>

## Planning

How your todo list is planned. Read by `ntm:plan` and the conventions;
Estimate pattern by the estimator agent and `ntm:review-todo-list`.

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

- Run from `ntm:configure`: return the sections to the caller, which packages
  once at the end.
- Run directly: load `ntm:settings` and follow its Regenerating
  `ntm-user.plugin` section with the section text you produced.

One more line, for every backend: once `ntm-user` is installed, run
`/ntm:self-test` in a new chat. It starts with `ready-check` and exercises the
operations the jobs use on a throwaway task, and is the smoke test for the
guide. Say it now when run directly. When run from `ntm:configure`, return it
with the sections so `configure` says it at its end.
