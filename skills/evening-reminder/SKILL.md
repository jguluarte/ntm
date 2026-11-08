---
name: evening-reminder
description: >-
    The evening reminder for the user's todo list: a friend asking how the day
    went. What closed, what's still open, and the evening message in the user's
    style. Run by the "Evening reminder" job, or by hand ("run the evening
    reminder now").
---

# ntm:evening-reminder

A friend asking how the day went. `ntm:show-completed` gives the facts; the
messenger agent writes and sends the message. If the messenger agent isn't
available in this session, follow the conventions' "Chat, jobs and agents".

# 1: Ready check

Run `/ntm:ready-check --notify-failure "Evening reminder"`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `ntm:show-completed` and run:

```
/ntm:show-completed today, and what's still open, planned today or earlier
```

Nothing done and nothing still open: assume a day off. STOP and send nothing.

Otherwise the facts are:

- one `done: <id> <title> <url>` line per Done task, or `done: none`
- one `open: <id> <title> <url>` line per Still open task, with ` (was <date>)`
  added when its planned date is before today; or `open: none`

# 3: The message

Ask the messenger agent:

```
reminder: evening
job: Evening reminder
<the facts>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't
carry the list), a delivery block, or a `… FAILED` line.

# FINAL REPLY

A delivery block is the final reply: the title line and the message, verbatim,
and nothing else. Otherwise end with one short line on what happened, such as
"Sent the evening reminder.", then any lines the messenger returned after
`Sent:`.

# ERROR HANDLING

For any error after step 1, including a `… FAILED` line from show-completed or
the messenger, never use `/ntm:notify`. End the run with the error stated
plainly; the scheduled task's own completion push carries it.
