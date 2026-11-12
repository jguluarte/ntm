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

Today is the date in the timezone under About you in `%Settings`.

Load what the Reminders part of `%Message-rules` says to load. Today's tasks are
every task planned for today, open and done, so an evening where everything got
done still gets its message.

A task's days slipped are the earlier days with a `%Message-history` entry whose
`ids` list it. When something on a task warrants upping the ante, you may also
mark it to press harder.

## The message

Hand the messenger agent `type: reminders.<type>`, such as `reminders.morning`,
with `record_task_ids: true`, today's date, and today's tasks, each with the
days it has slipped and any mark to press harder. It sends the message for that
type, as the user's message rules say. Hand it over even when there are no
tasks; the messenger decides when there's nothing to send.

## Result

Return what the messenger returned, as it came. A delivery block ends the run as
its title and message, without the `NOTIFY VIA FINAL REPLY` line.
