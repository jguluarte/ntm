---
name: today
description: >-
    Lists what's planned on the user's todo list, by default every open task
    planned for today, optionally whatever scope the user or a job describes
    ("what's due today", "what's on tap?", "tasks today"). Read-only. Run
    manually, and from scheduled jobs.
---

# ntm:today

## Setup

Load `/ntm-user:backend` to read the user's conventions

## Usage

```
/ntm:today [<scope in words>]
```

With nothing after it, list every open task with a planned date of "today" in
the user's timezone.

If the user provides scope, limit the results based on their request. IE: if the
user says `/ntm:today errands`, look for things assigned today that have to do
with errands.

## Result

Conversationally return information to the user describing the data you found,
or lack thereof.

### example: nothing found

#### without scope

> No open tasks found

#### with scope "errands"

> No open errands for today.

### example: things found

#### no scope

> Found two tasks for today:
>
> - Drop off package at UPS (ABC-123)
> - Do the laundry (ABC-90)

#### with scope "errands"

> Found two tasks for today, one is an errand:
>
> - Drop off package at UPS (ABC-123)
