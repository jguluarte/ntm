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
available in this session, read its file from the installed plugin and follow it
yourself, as the conventions' "Chat, jobs and agents" says.

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

`Show-completed FAILED`: see ERROR HANDLING.

Otherwise the facts are:

- one `done: <id> <title> <url>` line per task under Done, or `done: none`
- one `open: <id> <title> <url>` line per task under Still open, or
  `open: none`; add ` (was <date>)` when its planned date is before today

# 3: The message

Ask the messenger agent:

```
reminder: evening
job: Evening reminder
<the facts>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't
carry the list), a delivery block (a title line and the message text), or a
`… FAILED` line.

# FINAL REPLY

On an error, see ERROR HANDLING. Otherwise:

- Delivery block: the title line and the message, verbatim, and nothing else, as
  the conventions' Results say.
- `Sent:`: one short line, such as "Sent the evening reminder.", then any
  `List:` lines the messenger returned.
- Day off: one short line, such as "Day off; nothing sent."

# ERROR HANDLING

For any error after step 1, including a `… FAILED` line from show-completed or
the messenger, never use `/ntm:notify`. End the run with the error stated
plainly; the scheduled task's own completion push carries it.
