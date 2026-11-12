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

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend` and `%Settings`; if it fails, end the run with its result
line.

Then load the user's `%Message-rules`.

## The facts

Gather what the Reminders part of `%Message-rules` asks for. Today's tasks are
every task planned for today, open and done, so an evening where everything got
done still gets its message.

A task has slipped one day for each earlier day with an entry that lists its id
in `ids` in `%Message-history`. You may raise a task's count when something on
it warrants upping the ante.

## The message

Hand the messenger agent `type: reminders.<type>`, such as `reminders.morning`,
with `record_task_ids: true` and today's tasks, each with the days it has
slipped. It sends the message for that type, as the user's message rules say.

## Result

Return what the messenger returned, as it came.
