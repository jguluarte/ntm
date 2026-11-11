---
name: reminder
description: >-
    Sends one of the user's reminders about their todo list, morning, afternoon,
    evening or weekly: checks that ntm can run, then hands the reminder to the
    messenger agent, which follows the user's message rule for it, writes the
    message in the user's style and sends it. Run by a job, as /ntm:reminder
    --type morning, afternoon, evening or weekly.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening|weekly>
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
| `weekly`    | `weekly`              |

For `morning`, `afternoon` and `evening`, the messenger loads today's tasks
itself, as their message rules say.

The `weekly` message rule expects last week and the week ahead in hand. Earlier
in the weekly job, `show-completed` reported last week, done and still open, and
`plan --auto week` planned the week ahead: hand the messenger both, as they
came.

## Result

Return what the messenger returned, as it came.
