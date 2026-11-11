# Todo list setup

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

The backend to use on a first run. Without one, suggest Linear (see The
backend).

## Before you start

1. Load `ntm:conventions`. On a first run its first step says "not configured;
   run `/ntm:configure`". That's expected: carry on with the values you settle
   here. There is a predefined guide for linear.app, as well as the contract
   required to use a different backend.
    - If using Linear: `backends/linear.md`
    - Otherwise use `backends/contract.md`
2. If `ntm-user:settings` loaded and its Todo list names a backend, this is a
   re-run. Show the current Todo list, Labels, Planning and Shopping sections,
   ask what to change, and go to the step below that owns it; everything else
   stays as it is.
3. Keep a running list of what you've settled. Produce the sections at the end,
   not as you go, so a change of mind costs nothing.

## The backend

Suggest Linear: a free account is enough, ntm ships a guide for it, and you'll
help create it and connect it now. On a yes, read the guide,
`backends/linear.md`, for its operations, and follow Linear below in order; a
part tied to a step below waits for that step.

Someone who doesn't want Linear hears that finding something else takes longer,
and that you're happy to. Then their own backend, below.

For their own backend, follow `backends/own-backend.md` before Statuses. After
that, Statuses and Labels do their steps with the tools they named for the setup
operations.

## Linear

Backend is `linear`. Walk the parts below with the user, in order. The calls are
the guide's operations and Linear setup operations, at the end.

### Starting from nothing

Only when the user doesn't have Linear yet. These happen outside the chat, on
the user's side; walk them through in order and wait for "done" before The
connector below:

1. Sign up at linear.app. The free plan is enough: one workspace, unlimited
   issues.
2. The new workspace comes with one team; that team is the todo list. Its key
   (the few capital letters Linear asks for when naming it, `HOME` for
   `HOME-12`) starts every task's id, so pick one they'll be happy reading in
   reminders.
3. A new team's statuses already match the classes: Backlog, Todo, In Progress,
   Done, Canceled and Duplicate. Nothing to change. If they want a "can't move
   right now" status, they add one named Blocked in the team's workflow
   settings; otherwise the `$pending-shipment` label and blocked-by links cover
   that ground.

Labels and the price watch project don't need to be made by hand: Labels below
creates them.

### The connector

Connect it now, before the todo list below. ToolSearch for the tool the guide's
`ping` names. If it isn't there, walk the user through it: in Claude's settings,
the Connectors tab, add Linear and sign in to their workspace, then come back
here and say so. Search again before going on.

### The todo list

`list todo-lists`; propose the team. List name is its name, List id its id.

Then `ping` that team, right away. A pass: say in a line that the list answers.
Anything else: say what failed, as the guide's `ping` words it, and fix it with
them (sign in again, or sign in with the account that holds this team). Don't go
on until it passes; if it won't, say so and stop, since every later step needs
the list.

Once the team is chosen, suggest the user turn on Parent auto-close in the
team's settings under Workflow, so a parent closes as soon as its sub-tasks are
all done.

### The price watch project

`list projects`; ask which project holds purchases waiting for a good price, or
none (no price watch; the `$price-watch` label on a project later turns it on).
If they want one that doesn't exist yet, settle its name now; it's created in
Labels, once the project labels exist.

## Statuses

Nothing to store: each status's class is read from the backend at run time, as
the conventions' Status classes says. `list statuses` on the todo list and check
that each falls in a class (the guide says how); Blocked is the status named
Blocked. When they all do, say nothing. When one doesn't, name it, and say that
what it counts as goes under Deviations with `/ntm:settings`. For their own
backend, the mapping they gave goes in the Status classes paragraph under Todo
list (see Returning the sections).

## Labels

Show the defaults in one table, with the one-line meaning of each from the
conventions' System labels: `$no-autoschedule`, `$pending-shipment`,
`$has-amazon-alert`, `$amazon-unavailable`, `$price-watch`. A simple affirmation
keeps every name; record any rename.

Then `list labels`, task and project sets. For each label the todo list lacks,
offer to create it with `create label` under its settled name, with its one-line
meaning as the description. Project labels are their own set where the backend
keeps one: `$price-watch` and `$no-autoschedule` as project labels, so projects
can carry them.

Then the price watch project, when one was chosen: create it now with
`create project`, carrying both project labels. If it already exists, make sure
it carries both; `create project` says whether `labels` replaces the set.

## Planning

How `ntm:plan` works the todo list. Show the defaults as one short list, one
line each, and say what each is for in a few words; a simple affirmation keeps
them all, and they change any line in their own words:

- **Excluded labels from automatic scheduling:** `$no-autoschedule`,
  `$pending-shipment`. Labels planning never picks, each checked on the task and
  its project; name the labels by the names settled above.

Which days get planned, how many tasks each gets, how big they should be and
what the weekly message covers aren't settings: each job's prompt says what
differs from the defaults in `ntm:plan`, and `/ntm:configure-schedule` writes it
with the user.

Estimates aren't a setting either. They're in hours, which anyone can read. A
user who wants another way says so in a review, and the estimator agent works it
out with them.

## Shopping

Only when a price watch project was chosen; otherwise skip and return no
Shopping section.

Say in one line that each watched task's description says what differs from the
defaults: the condition (new), how it reaches them (ordered online and
delivered), and what counts as a deal (at or near the target, or well below the
usual price).

Ask whether they want Amazon's own price alerts on watched items, kept in step
by `/ntm:sync-price-watch-to-amazon`. If yes, ask how it reaches Amazon:
Claude's built-in browser, or their own browser through the Claude extension.
Record it as Amazon interface; blank means it asks each time. If no, leave the
Amazon interface line out.

Then ask, once: anything else about how they shop? Stores they always or never
use go in `%Price-watch-stores` (setup's databases step offers its Seed), not
here; this is for anything that holds for every item. Capture it as written
below the lines; "nothing" leaves it blank. With no Amazon interface line and
nothing else, return no Shopping section.

## Databases

With `create database`, create each database below from its template in
`references/databases/`, in the newest installed `ntm`. Leave out the template's
`<!-- -->` comments: they're for you to build their databases.

- `%Message-rules`: everyone.
- `%Task-review-log`: task management.

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

How your todo list is planned. Read by `ntm:plan` and `ntm-user:backend`.

- Excluded labels from automatic scheduling: <default no-autoschedule,
  pending-shipment>

<anything else about how they want planning done, as written; or nothing>

## Shopping

How the price watch shops. Read by the shopper agent; Amazon interface by
`ntm:price-watch` and `ntm:sync-price-watch-to-amazon`.

- Amazon interface: <Claude's built-in browser, or your own browser through the
  Claude extension; blank asks each time; the line left out for no Amazon
  alerts>

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

## Linear setup operations

### `list todo-lists`

`list_teams`. Each comes back with its name and id.

### `create todo-list`

Not needed; Linear has teams to list.

### `list statuses`

`list_issue_statuses` with `team`. Each comes back with its name and `type`; the
guide's Status classes gives each one's class.

### `list labels`

`list_issue_labels` with `team` for issue labels; `list_project_labels` with
`team` for project labels, a separate set.

### `create label`

`save_issue_label` with `name`, `teamId: "<List id>"` and `description` for an
issue label; `save_project_label` with `name`, `teamId` and `description` for a
project label.

### `list projects`

`list_projects` with `team: "<List name>"`, `fields` `name` and `labels`. Each
comes back with its id.

### `create project`

Create the project labels it should carry first (`create label`), then
`save_project` with `name`, `addTeams` naming the todo list, and `labels`. When
updating an existing project, pass its current labels plus the missing ones.
