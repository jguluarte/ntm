---
name: reminder
description: >-
    Sends one of the user's daily reminders about their todo list, morning,
    afternoon or evening: checks that ntm can run, then hands the reminder to
    the messenger agent, which follows the user's message rule for it, writes
    the message in the user's style and sends it. Run by a job, as /ntm:reminder
    --type morning, afternoon or evening.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
```

The type picks the user's message rule, which says what the message holds.

## Setup

Run `/ntm:ready-check --notify-failure reminder`. If it fails, end the run with
its result line.

## The message

Ask the messenger agent for the reminder, with the `type:` for its rule:

| `--type`    | `type:`               |
| ----------- | --------------------- |
| `morning`   | `reminders.morning`   |
| `afternoon` | `reminders.afternoon` |
| `evening`   | `reminders.evening`   |

The messenger loads today's tasks itself, as the message rules say.

## Result

Return what the messenger returned, as it came.
