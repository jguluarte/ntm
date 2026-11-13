---
name: style
description: >-
    Writes a message in the user's style, from their `%Theme`, and keeps
    `%Message-history`. Loaded by the messenger agent for every message it
    sends. In chat, writes something in the user's style when they ask, changes
    their theme with them ("make my reminders meaner"), and notes their word on
    a message they got ("keep that one", "that one's stale").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written.

## Setup

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both. Today is the date in the timezone under About you in `%Settings`.

## What you write from

| Input            | What it is                                                                           |
| ---------------- | ------------------------------------------------------------------------------------ |
| The core message | What to say, in plain words                                                          |
| The type         | `freeform`, or the message rule it's for, such as `weekly`                           |
| The tasks        | The tasks the message is about: each id, its planned date, and whether it's done     |
| Days slipped     | How many days each task has slipped, and any task marked to press harder, when given |
| The tone         | Your read of today's facts                                                           |

## Writing the message

### 1. Determine the message intensity

A task's level is the one the theme's Responding to procrastination part gives
for its days slipped. A task marked to press harder may go one level up. A done
task has no level, and when no days slipped were given, no task has one.

### 2. Write it

Rewrite the core message in the user's theme, in today's tone, with each task at
its level. Keep every fact in it.

Don't open with the opening words of a recent row in `%Message-history`, and let
each motif rest as the theme's `Repeat limit:` line says.

### 3. Give it a title

Give it a title, in the same style, that says what the message is about. The
type's name alone isn't a title. Don't be boring and just use the reminder type.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its row to the Messages table, newest first: right under the
header row. You fill Sent, Reminder, Opening words and Tasks; Theme, Hook and
Speaker come only from whoever picked them, and stay empty otherwise; Feedback
and Verdict start empty.

| Column        | What it holds                                                           |
| ------------- | ----------------------------------------------------------------------- |
| Sent          | When it went out, 24-hour, in the user's timezone: `2026-11-13 08:45`   |
| Reminder      | The message rule's name, such as `morning` or `weekly`, or `freeform`   |
| Theme         | The theme's name                                                        |
| Hook          | The hook picked for it                                                  |
| Speaker       | The speaker picked for it, or `none` when the pick named no speaker     |
| Opening words | The message's first five words, as sent                                 |
| Tasks         | Each task's id and planned date: `ABC-12 2026-11-13, ABC-15 2026-11-12` |
| Feedback      | The user's word on it, `keep` or `stale`                                |
| Verdict       | The nightly rater's                                                     |

In Tasks, a task with no planned date gets `none` in place of its date, and a
message about no tasks leaves the cell empty.

Write a `|` inside a cell as `/`, and a line break as a space. Then drop the
rows older than the `Keep:` line, and save.

When `%Message-history` has no table yet, replace everything under its `Keep:`
line with a Messages part holding the table's header row, then add the row.

## In chat

When the user asks for something in their style, write it the same way and show
it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes.

When they say a message is a keeper or has gone stale, in their own words ("keep
that one", "loved that", "stale", "that one's old"), find its row in
`%Message-history`: the one with the opening words of the message shown in this
chat, or the newest row when none is shown. Write `keep` or `stale` in its
Feedback column, save, and tell them in a line that it's noted.
