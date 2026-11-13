---
name: reminder
description: >-
    Sends one of the user's daily reminders about their todo list, morning,
    afternoon or evening: checks that ntm can run, gathers today's tasks and how
    many days each has slipped, works out from the user's message rule what the
    reminder says, has ntm:style write it in the user's style, and sends it. Run
    by a job, as /ntm:reminder --type morning, afternoon or evening.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
```

The type picks the user's message rule, which says what the message holds.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

Then load the user's `%Message-rules`, then `ntm:style`, and follow its Setup.

## The facts

Today is the date in the timezone under About you in `%Settings`.

Load what the Reminders part of `%Message-rules` says to load. Today's tasks are
every task planned for today, open and done, so an evening where everything got
done still gets its message.

A task has slipped one day for each date its `Planned date history` comment
lists, as ntm's core rules describe it; a task with no comment hasn't slipped.
Dates from a while back weigh less: a task picked up again after a long gap gets
fewer days slipped than its dates, as you judge it.

For the afternoon and evening, the rule compares against the tasks today's
earlier reminders covered: the task ids in today's `%Message-history` entries,
from `ntm:style`'s reading of them.

## The message rule

The rule for this reminder is the Reminders part of `%Message-rules` and the
reminder's own part, such as Morning. The reminder's own part adds to the
Reminders part, and wins where they differ.

Apply it to the facts. When it leaves nothing to send, such as no tasks, end the
run with `Not sent: <why>`.

## The message

Send it as the core rules' Sending a message in the user's style says. Its facts
are:

- what the message must cover, as the rule says, in plain words
- today's tasks, each with its id and title, whether it's done, its days slipped
  and the dates from its `Planned date history`
- for the afternoon and evening, the tasks the earlier reminders covered
- anything the rule asks for about tone

## Result

What `ntm-user:notify` returned, `Writer FAILED: <why>`, or `Not sent: <why>`.
For a `NOTIFY VIA FINAL REPLY` block, end the run with its title and message,
without that line.
