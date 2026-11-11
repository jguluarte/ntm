# Backend contract

What ntm needs from the backend that holds the user's task list, and how a
backend other than Linear qualifies. Skills call the operations below by these
names, and a backend's guide says how each one is done on it: `linear.md`,
beside this file, is Linear's. Any backend works that can do every operation, as
long as how is written down or discoverable from its connector.

## What a backend needs

- Tasks with an id, a title, a description, a status, labels, a date field to
  use as the planned date, sub-tasks, and a web link.
- A way to group tasks, such as projects or folders.
- A connector Claude can use to read and write them.

A backend can't go without a planned date or a way to tell open tasks from
closed. It can go without anything else; the guide says what's missing, and
skills do without it:

- No blocked-by relation: planning and reviews work from titles and
  descriptions.
- No labels on groups: the user puts labels on tasks directly.
- No documents: each database is kept in a task, as Databases says.

## Task list

The guide names the user's list, `<List name>`, and the id calls take,
`<List id>`, blank when they take none. Where the backend has no lists, the
whole account is the task list. The guide also says how projects carry labels.

An estimate is never a backend field: it's the `Estimate:` line at the end of
the task's description, on every backend.

## Status classes

How each status maps to the rules' classes: plannable (with started), blocked,
done, canceled and duplicate. The guide says how to read a task's class, filter
by it, and set a status in it. A backend with only open and closed maps open to
plannable and closed to done.

## Operations

### `ping`

One read that proves the connector works and sees the task list. The guide says
how to tell apart the failures `ntm:ready-check` reports (sign-in expired, wrong
account and backend error) and what a connector waiting on a sign-in looks like.

### `fetch open`

Every open task, blocked ones included, with the standard fields: id, title,
link, status, status class, priority, estimate, planned date, labels, project,
parent id, completed at and updated at. Also every project with its name and
labels, and its summary when a skill asks. The guide says which priority is
highest and which means none.

### `fetch closed`

Closed tasks with when each closed: done, plus canceled and duplicate when
asked. The guide says how to limit them to a span and to one label.

### `read task`

One task with its description and blocked-by relations.

### `read comments` / `write comment` / `update comment`

Reads a task's comments, adds one, and changes one in place. A backend that
can't change a comment deletes it and adds the new text.

### `set planned date` / `clear planned date`

Sets or clears a task's planned date, and nothing else.

### `set status`

Moves a task to a status in a given class.

### `add labels` / `remove labels`

Adds or removes labels, keeping the others.

### `mark duplicate of`

Marks a task a duplicate of another. Without a duplicate relation, it sets the
duplicate status and comments with the original's id.

### `create task`

A new task with a title, description, project, parent, blocked-by and labels,
after checking that no matching task exists.

### `update task`

Changes a task's title, description, estimate or project, removes its project,
or adds a blocked-by link, and nothing else.

## Databases

The documents ntm keeps its records in, on the task list, each found by its
title. Each operation takes an optional project, for a database kept in one.

### `read database`

Returns its content, or says it's missing.

### `write database`

Replaces its content, creating it when it's missing.

### `create database`

Creates it with its first content, leaving one that exists alone.

A backend with no documents keeps each database in the description of an open
task titled with the database's title, with the `$no-autoschedule` label and no
planned date, so planning never picks it.

## Writing

How the backend says whether a write succeeded, so the rules' retry rule
applies.

## Setup operations

Setup uses these to connect the backend and save the features.

### `list todo-lists`

The lists the connector can see, by name and id.

### `list projects`

Every project with its name, id and labels.

### `create label`

A label by name, with a description, for tasks and, where projects keep their
own set, for projects; one that exists is left alone.

### `create project`

A project by name carrying the given labels, or those labels added to an
existing one.

## Your own backend

For a user who doesn't want Linear. Their backend has no guide file: the guide
you write with them here is its guide.

### 1. Find one

Ask what they keep tasks in today, or would like to. Two ways always work: a
list built inside Claude, such as a Claude Doc made with them here, or an app
they use, reached through a Claude connector. Search with them: ToolSearch for
connectors already attached, and the web for a tool's connector and what it can
do. Hold each option up to What a backend needs, in a line or two, until they're
content with one. If it isn't connected yet, they add it on the Connectors tab
in Claude's settings; ToolSearch again before going on.

### 2. Define each operation

Walk this file with them, heading by heading. For each operation, name the tool
and the values that do it, read from the tool's schema, never guessed: which
date field is the planned date, how results page, whether labels add or replace.
Where the connector's own tool descriptions make an operation plain, naming the
tool is enough. Where a choice is theirs, such as which grouping is a project,
propose one and let them react.

A missing planned date, or no way to tell open from closed, gets covered before
going on: a field, status or label they can repurpose, or a list built inside
Claude instead.

### 3. Ping it

Once `ping` is defined, run it. Fix what fails with them; if it won't pass, say
so and stop, since every later step needs the list. The other operations wait
for `/ntm:self-test`.

### 4. Record it

Write the guide in the shape of `linear.md` from Task list on, each operation's
tool and values under its name, in their words where they gave them. It goes
into `ntm-user:backend` in place of Linear's, where every later run reads it.
Once `ntm-user` is installed, `/ntm:self-test` proves it.
