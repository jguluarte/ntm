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

## Today's tasks

Load what the Reminders part of `%Message-rules` says to load. Where it says
today's tasks, that is every task planned for today, open and done, so an
evening where everything got done still gets its message.

A task slipped once for each date its `Planned date history` comment lists, as
ntm's core rules describe it; a task with no comment hasn't slipped.

For the afternoon and evening, the rule compares against the tasks today's
earlier reminders covered. `ntm:style`'s Setup read today's `%Message-history`
entries, and their `ids` are those tasks. Look up each one's title and where
it's planned now.

## The message rule

The rule for this reminder is the Reminders part of `%Message-rules` and the
reminder's own part, such as Morning. The reminder's own part adds to the
Reminders part, and wins where they differ.

Apply it to today's tasks. With none, end the run with
`Not sent: no tasks planned today`, unless the rule asks for a message anyway.

## The message

Send it as the core rules' Sending a message in the user's style says. Its facts
are:

- what the message must cover, as the rule says, in plain words
- today's tasks, each with its id and title, whether it's done, how many times
  it slipped, and the dates it slipped from
- for the afternoon and evening, the tasks the earlier reminders covered, each
  with its id, title and where it's planned now
- anything else the rule asks of the message, such as tone or length, already
  decided for today

## Result

`Not sent: no tasks planned today`, or the sender's result the core rules'
Sending a message in the user's style gives.
