---
name: reminder
description: >-
    Sends one of the user's daily reminders about their todo list, morning,
    afternoon or evening: checks that ntm can run, gathers today's tasks and how
    many days each has slipped, then hands them to the messenger agent, which
    follows the user's message rule for it, writes the message in the user's
    style and sends it. Run by a job, as /ntm:reminder --type morning, afternoon
    or evening.
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

Then load the user's `%Message-rules`.

## The facts

Today is the date in the timezone under About you in `%Settings`.

Load what the Reminders part of `%Message-rules` says to load. Today's tasks are
every task planned for today, open and done, so an evening where everything got
done still gets its message.

A task has slipped one day for each date its `Planned date history` comment
lists, as ntm's core rules describe it; a task with no comment hasn't slipped.
Dates from a while back weigh less: a task picked up again after a long gap gets
fewer days slipped than its dates, as you judge it.

## The message

Hand the messenger agent `type: reminders.<type>`, such as `reminders.morning`,
with today's date and today's tasks, each with whether it's done, its days
slipped and the dates from its `Planned date history`. It sends the message for
that type, as the user's message rules say. Hand it over even when there are no
tasks; the messenger decides when there's nothing to send.

## Result

Return what the messenger returned. For a delivery block, end the run with its
title and message, without the `NOTIFY VIA FINAL REPLY` line.

The reply shows the message's title and message as sent, so the user can answer
it in this chat.
