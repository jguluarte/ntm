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

| Input             | What it is                                                                      |
| ----------------- | ------------------------------------------------------------------------------- |
| The core message  | What to say, in plain words                                                     |
| The type          | `freeform`, or the message rule it's for, such as `weekly`                      |
| The task ids      | The tasks the message is about                                                  |
| Days slipped      | How many days each task has slipped, and any marked to press harder, when given |
| `record_task_ids` | Whether the history entry records the task ids; `false` when not given          |
| The tone          | Your read of today's facts                                                      |

## Writing the message

### 1. Find each task's level

For each task given with its days slipped, the theme's Responding to
procrastination part gives its level for that count; a task marked to press
harder may go a level up. A done task has no level. A message without days
slipped skips this step: its tasks have no level.

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
final reply, add its entry: one JSON line at the top of the Entries part.

| Field  | What it holds                                                                     |
| ------ | --------------------------------------------------------------------------------- |
| `date` | The date it went out, such as `2026-11-09`                                        |
| `ids`  | The task ids when `record_task_ids` is true, such as `["ABC-12"]`; otherwise `[]` |
| `line` | The message as sent                                                               |

Then drop the entries older than the `Keep:` line, and save.

## In chat

When the user asks for something in their style, write it the same way and show
it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes.
