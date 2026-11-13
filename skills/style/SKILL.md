---
name: style
description: >-
    Turns a message's facts into a finished message in the user's style: picks
    what it draws on from their `%Theme`, sets the tone, has the writer agent
    write versions, chooses one, and records it in `%Message-history` once it's
    sent. Loaded for every message ntm sends in the user's style. In chat,
    writes something in the user's style when they ask, or changes their theme
    with them ("make my reminders meaner").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written. `%Theme` and `%Message-history` are read only through this
skill; the writer agent reads neither.

## Setup

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both. Today is the date in the timezone under About you in `%Settings`.

## What you write from

| Input             | What it is                                                             |
| ----------------- | ---------------------------------------------------------------------- |
| The facts         | Whatever the sender provides, as its own file says                     |
| `record_task_ids` | Whether the history entry records the task ids; `false` when not given |

The facts hold what the message must cover, and may hold its tasks and what's
known of each, and anything the sender's rule asks for.

## Writing a message

### 1. Pick

Pick what this message draws on from `%Theme`: one hook, a motif, reference or
line from the theme, and a speaker when the theme has them and one fits. Steer
away from what recent `%Message-history` entries used, and let each motif rest
as the theme's `Repeat limit:` line says, when it has one.

The pick gives the hook, the speaker or none, and the theme material: the
theme's guidance for writing in it, and its entries for the hook and the
speaker.

### 2. Set the tone

Read the facts against the theme's guidance and set the tone: how hard each
slipped task is pressed, a win for what's done, and anything the facts ask of
the tone. A slip is a planned date that moved on; nothing was missed.

### 3. Write

Hand the writer agent the facts, the tone, the hook, the speaker and the theme
material. It returns 5 versions, each with a title, a probability and a message,
or `Writer FAILED:`, which the sender ends with.

### 4. Choose

Take the version with the lowest probability whose opening words don't open a
recent `%Message-history` entry. Its title and message are what the sender
sends.

### 5. Record

Once the sender has sent it, add its entry as Keeping `%Message-history` says.

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

When the user asks for something in their style, write it with steps 1 to 4 and
show it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes. For a
whole new theme or a rebuild, load `ntm:theme-builder` and follow it instead.
