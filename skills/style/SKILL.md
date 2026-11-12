---
name: style
description: >-
    Writes a message in the user's style, from their `%Theme`, and keeps
    `%Message-history`. Loaded by the messenger agent for every message it
    sends, and in chat when the user asks for something in their style.
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written.

## Setup

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both. Today is the date in the timezone under About you in `%Settings`.

## What you write from

| Input            | What it is                                                        |
| ---------------- | ----------------------------------------------------------------- |
| The core message | What to say, in plain words                                       |
| The type         | `freeform`, or the message rule it's for, such as `weekly`        |
| The task ids     | The tasks the message is about; none when the user's rule says so |
| The tone         | Your read of today's facts                                        |

## Writing the message

### 1. Count the days each task has carried over

For each task id you were given, count the days before today that have an entry
whose `ids` hold it, never reading ids from an entry's line. The theme's
Responding to procrastination part gives the task's level for that count.

### 2. Write it

Write the core message as `%Theme` says for its type, in the tone, with each
task at its level. Keep every fact it holds.

Don't reuse a line, an opener or a shape from recent entries, and let each motif
rest as the theme's `Repeat limit:` line says.

### 3. Give it a title

A title in the same style that says what the message is about, never just the
type's name.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry: one JSON line at the top of the Entries part.

| Field  | What it holds                                                       |
| ------ | ------------------------------------------------------------------- |
| `date` | The date it went out, such as `2026-11-09`                          |
| `ids`  | The task ids you were given, such as `["ABC-12"]`, or `[]` for none |
| `line` | The message as sent                                                 |

Then drop the entries older than the `Keep:` line, and save.

## In chat

When the user asks for something in their style, write it the same way and show
it to them.
