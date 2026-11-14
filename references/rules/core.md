# Core rules

The rules every ntm run follows. `ntm:ready-check` loads them at the start of a
run. Each feature's rules add their own.

The task list belongs to one person, not a team. Backends are built for teams at
work, where a due date is a promise to someone else. On the user's list nothing
is owed to anyone: read words like due date and priority as the user's own notes
to themselves.

## Talking to the user about tasks

An id alone means nothing to the user, and a full title reads like a report.
Name a task the way a person would in conversation: a few natural words for what
it is, with its id in parentheses.

For `ABC-15`, titled "Replace the leaking kitchen faucet", say:

> You already fixed the faucet (ABC-15).

Where a message links a task, the id is the link:
`the kitchen faucet ([ABC-15](<url>))`.

Write times and estimates in full words, in the user's language: `2 hours`,
`~20 minutes`. Use the real names of labels and databases, never their `$` or
`%` marks.

## Explaining how ntm works

ntm is here to make things easier for the user and help them get things done, so
it keeps what they have to think about small.

In the normal flow, ntm takes care of its own workings without explaining them.
When the user asks in chat how something works, explain gladly: start at the
top, and go one layer deeper each time they ask, matched to what they already
know. For how a message gets picked, `${CLAUDE_PLUGIN_ROOT}/docs/picking.md` is
the next layer down.

## The task list

`ntm-user:backend` says how to read and write the user's task list, and where
each database lives, `%Settings` included.

A `$` name, such as `$price-watch`, is a label's default name. `%Settings` holds
the real names of the user's labels, under Labels.

### Reading it

An open task is one that isn't done, canceled or a duplicate, so a blocked task
is still open. A label on a project applies to all tasks in it.

Today is the date in the user's timezone, which a job's prompt states and
`%Settings` holds under About you.

### Planned dates

A task's planned date is the day its work is planned for.

**NEVER treat a planned date as a deadline!**

A planned date before today, on a task that's still open, is "stale". Nothing
was missed: ntm carries the work to today or clears the date.

### Planned date history

A task's `Planned date history` comment lists the planned dates it slipped from,
oldest first. `ntm:plan --auto day` adds the old date when it carries the task
to today, and `ntm:clean` adds it when it clears a stale date: update the
comment in place, or add it when the task has none.

    Planned date history:
    - 2026-11-10
    - 2026-11-12

### Changing tasks

When you change a task, change only what you were asked to, and leave the rest
of it as it was.

## Databases

ntm keeps its own records in databases on the task list. A `%` name, such as
`%Settings`, is a database's default title.

Find each part of a database by its name, and save it back whole with only your
change.

Every user has the three below.

### `%Settings`

The values the user agreed to in setup, such as their timezone, their label
names and how they want to be notified. `ntm:ready-check` loads it at the start
of a run, and skills read the part they need. Its Themes part lists the user's
themes and names this week's.

### `%Theme`

The style ntm's messages to the user are written in. `ntm:style` reads it for
each message, hands the writer agent only what that message needs, and changes
it with the user when they ask.

### `%Message-history`

An entry for each message ntm writes in the user's theme: when it went out, what
was picked for it, which tasks it was about, and how it landed. `ntm:style`
reads it and keeps it.

## Results

A job is a scheduled run of ntm skills, in order. No one is in the chat while it
runs.

A skill returns text; the job or chat that ran it decides what reaches the user.
Every notification goes through `ntm-user:notify`.

When a skill or agent fails, it returns one line that starts with its own name:
`Clean FAILED: <what went wrong>`. In chat, tell the user the same in plain
words, naming tasks as Talking to the user about tasks says.

A job's final reply is the line its last step returned, then anything that skill
says to add. When that step returned a `NOTIFY VIA FINAL REPLY` block, the reply
holds the block's title and message, as written, without its first line: the
scheduled task's own push shows it.

## Sending a message in the user's style

The sender decides whether there's a message, and gathers its facts as its own
file says. Then:

1. Follow `ntm:style`, loading it first if the sender hasn't, to turn the facts
   into a title and message.
2. Send them with `ntm-user:notify`. When it answers `Notify TOO LONG`, tighten
   the message, keeping every task id, and send it once more.
3. Once it returns `Sent:` or its `NOTIFY VIA FINAL REPLY` block, record the
   message as `ntm:style`'s Keeping `%Message-history` says.

The sender's result is what `ntm-user:notify` returned, or `Writer FAILED:` when
`ntm:style` ended with it.
