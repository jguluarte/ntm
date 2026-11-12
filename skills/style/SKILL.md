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

| Input            | What it is                                                 |
| ---------------- | ---------------------------------------------------------- |
| The core message | What to say, in plain words                                |
| The type         | `freeform`, or the message rule it's for, such as `weekly` |
| The task ids     | The tasks the message is about                             |
| The tone         | Your read of today's facts                                 |

## Writing the message

### 1. Count the days each task has carried over

In a reminder, for each task id you were given, count the earlier days with an
entry that lists it in `ids`. The theme's Responding to procrastination part
gives the task's level for that count; any other message has no levels.

### 2. Write it

Rewrite the core message in the user's theme, in today's tone, with each task at
its level. Keep every fact in it.

Don't reuse a line, an opener or a shape from recent entries, and let each motif
rest as the theme's `Repeat limit:` line says.

### 3. Give it a title

Give it a title in the same style that says what the message is about. The
type's name alone isn't a title.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry: one JSON line at the top of the Entries part.

| Field  | What it holds                                              |
| ------ | ---------------------------------------------------------- |
| `date` | The date it went out, such as `2026-11-09`                 |
| `ids`  | The task ids you were given, such as `["ABC-12"]`, or `[]` |
| `line` | The message as sent                                        |

A reminder, a `reminders.*` type, records its task ids, so a task that keeps
slipping changes how the reminders talk to the user; any other message records
`[]`.

Then drop the entries older than the `Keep:` line, and save.

## In chat

When the user asks for something in their style, write it the same way and show
it to them.

When they ask to change how their messages read, work out with them the change
to the part of `%Theme` their words are about, show it, and save it when they
say yes.
