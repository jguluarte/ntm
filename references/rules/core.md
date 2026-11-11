# Core rules

The rules every ntm run follows, whatever features the user picked. Each
feature's rules add their own.

The task list belongs to one person, not a team. Backends are built for teams at
work; read their words, such as due date and priority, without that weight.

## Talking to the user about tasks

An id alone means nothing to the user, and a full title reads like a report.
Name a task the way a person would in conversation: a few natural words for what
it is, with its id in parentheses, never its full title.

For `ABC-15`, titled "Replace the leaking kitchen tap", say:

> You already finished the kitchen tap (ABC-15).

Where a message links a task, the id is the link:
`the kitchen tap ([ABC-15](<url>))`.

Write times and estimates in full words, in the user's language: `2 hours`,
`~20 minutes`. Use the real names of labels and databases, never their `$` or
`%` marks.

## The task list

`ntm-user:backend` says how to read and write the user's task list, the real
names of their labels, and where each database lives.

### Reading it

An open task is one that isn't done, canceled or a duplicate, so a blocked task
is still open. A label on a project counts on every task in it.

Today is the date in the user's timezone, which a job's prompt states and
`%Settings` holds under About you.

### Planned dates

A planned date is the day the user means to do the work.

**NEVER treat a planned date as a deadline.**

A planned date before today, on a task that's still open, is "stale". Nothing
was missed: ntm carries the work to today or clears the date.

### Writing back

Write only what the run is for, and leave the rest of each task as it was.

The user often adds a task just so they don't forget it; what it takes gets
worked out later. When they ask for one, make what they asked for, in their
words, and add no meaning they didn't give it. File it in a project that fits,
or in none.

## Databases

ntm keeps its own records in databases on the task list. A `%` name, such as
`%Settings`, is a database's default title; `ntm-user:backend` gives its real
title and where it lives.

Find each part of a database by its name, and save it back whole with only your
change.

Every user has the three below.

### `%Settings`

The values the user agreed to in setup, such as their timezone, their label
names and how they want to be notified. Skills read the part they need.

### `%Theme`

The style ntm's messages to the user are written in. `ntm:style` reads it before
each message, and changes it with the user when they ask.

### `%Message-history`

What ntm's messages have said, so the next ones don't repeat it. `ntm:style`
keeps it.

## Results

A skill returns text; the job or chat that ran it decides what reaches the user.
Only `ntm-user:notify` sends anything.

When a skill fails, it returns one line that starts with its own name:
`Fix-task-list FAILED: <what went wrong>`. In chat, tell the user the same in
plain words, naming tasks as Talking to the user about tasks says.

A job's final reply is what its last step returned, in one line. When a step
returned a `NOTIFY VIA FINAL REPLY` block, the final reply is instead everything
after that line, as written, and nothing else: the scheduled task's own push
shows it.
