---
name: style
description: >-
    Writes a message in the user's style, from their `%Theme`, and keeps
    `%Message-history`. Loaded by the messenger agent for every message it
    sends. In chat, writes something in the user's style when they ask, or
    changes their theme with them ("make my reminders meaner").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written.

## Setup

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both. Today is the date in the timezone under About you in `%Settings`.

## What you write from

| Input             | What it is                                                                           |
| ----------------- | ------------------------------------------------------------------------------------ |
| The core message  | What to say, in plain words                                                          |
| The type          | `freeform`, or the message rule it's for, such as `weekly`                           |
| The task ids      | The tasks the message is about, and which of them are done                           |
| Days slipped      | How many days each task has slipped, and any task marked to press harder, when given |
| `record_task_ids` | Whether the history entry records the task ids; `false` when not given               |
| The tone          | Your read of today's facts                                                           |

## Writing the message

### 1. Determine the message intensity

A task's level is the one the theme's Responding to procrastination part gives
for its days slipped. A task marked to press harder may go one level up. A done
task has no level, and when no days slipped were given, no task has one.

### 2. Write it

Rewrite the core message in the user's theme, in today's tone, with each task at
its level. Keep every fact in it.

Don't reuse a line, an opener or a shape from recent entries, and let each motif
rest as the theme's `Repeat limit:` line says.

### 3. Give it a title

Give it a title, in the same style, that says what the message is about. The
type's name alone isn't a title. Don't be boring and just use the reminder type.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry at the top of the Entries part. An entry is one JSON
line, written with only the fields that have a value. Spread over lines here:

```json
{
    "sent": "2026-11-13 08:45",
    "reminder": "morning",
    "opening": "Shelf day, one bracket first",
    "tasks": [{ "id": "ABC-12", "planned": "2026-11-13" }]
}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `reminder`: the message rule's name, such as `morning` or `weekly`, or
  `freeform`
- `theme`, `hook`, `speaker`: from whoever picked them, as handed
- `opening`: the message's first five words, as sent
- `tasks`: each task the message is about, with its planned date when it has one
- `feedback`: the user's word on it, `keep` or `stale`
- `verdict`: the nightly rater's

Then drop the entries older than the `Keep:` line, and save.

## In chat

When the user asks for something in their style, write it the same way and show
it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes.

When they say a message is a keeper or has gone stale, in their own words ("keep
that one", "loved that", "stale", "that one's old"), find its entry in
`%Message-history`: the one with the opening words of the message shown in this
chat, or the newest entry when none is shown. Set its `feedback` to `keep` or
`stale`, save, and tell them in a line that it's noted.
