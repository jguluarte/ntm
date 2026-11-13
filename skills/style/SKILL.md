---
name: style
description: >-
    Turns what a message says into a finished message in the user's style: picks
    what it draws on from their `%Theme`, has the writer agent write versions,
    chooses one, and records it in `%Message-history` once it's sent. Loaded for
    every message ntm sends in the user's style. In chat, writes something in
    the user's style when they ask, or changes their theme with them ("make my
    reminders meaner").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written. This skill is the only reader of `%Theme` and
`%Message-history`.

## Setup

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both. Today is the date in the timezone under About you in `%Settings`.

## What you write from

| Input                  | What it is                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| What this message says | What the message must cover, in plain words                                                 |
| The facts              | Each task's id and title, whether it's done, its days slipped and the dates it slipped from |
| The type               | The message's name, such as `morning`, `weekly` or `freeform`                               |
| `record_task_ids`      | Whether the history entry records the task ids; `false` when not given                      |

## Writing a message

### 1. Pick

Pick what this message draws on from `%Theme`: one hook, a motif, reference or
line from the theme, and a speaker when the theme has them and one fits. Steer
away from what recent `%Message-history` entries used, and let each motif rest
as the theme's `Repeat limit:` line says.

The pick gives the hook, the speaker or none, and the theme material: the
theme's guidance for writing in it, and its entries for the hook and the
speaker.

### 2. Write

Hand the writer agent what this message says, the facts, the hook, the speaker
and the theme material. It returns 5 versions, each with a title, a probability
and a message, or `Writer FAILED:`, which the sender ends with.

### 3. Choose

Take the version with the lowest probability whose opening words don't open a
recent `%Message-history` entry. Its title and message are what the sender
sends.

### 4. Record

Once the sender has sent it, add its entry as Keeping `%Message-history` says,
with the hook and the speaker from the pick.

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

When the user asks for something in their style, write it with steps 1 to 3 and
show it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes. For a
whole new theme or a rebuild, load `ntm:theme-builder` and follow it instead.
