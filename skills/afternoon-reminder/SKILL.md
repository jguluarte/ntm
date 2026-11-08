---
name: afternoon-reminder
description: >-
    The afternoon reminder for the user's todo list: a tap on the shoulder about
    what's still open today, with started work marked; never a dig. Run by the
    "Afternoon reminder" job, or by hand ("run the afternoon reminder now").
---

# ntm:afternoon-reminder

A tap on the shoulder about what's still open today. `ntm:today` gives the
facts; the messenger agent writes and sends the message. If the messenger isn't
available in this session, follow the conventions' "Chat, jobs and agents".

# 1: Ready check

Run `/ntm:ready-check --notify-failure "Afternoon reminder"`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `ntm:today` and `ntm:pause`, and run `/ntm:today`.

When it lists tasks, the facts are one line per task:

```
open: <id> <title> <url>
```

Add ` (was <date>)` when the planned date is before today, then ` (started)`
when `ntm:today` marked the task started. Remind about everything listed,
whatever its labels or status, even on a paused day: the user dated it.

When it lists nothing, run `/ntm:pause --check`. If today is paused (its line
ends `true`), STOP and send nothing. Otherwise the facts are `open: none`.

On any `… FAILED` line, go to ERROR HANDLING.

# 3: The message

Ask the messenger agent:

```
reminder: afternoon
job: Afternoon reminder
<the facts>
```

It returns `Sent: <title>`, followed by `List:` lines when the push couldn't
carry the list; a delivery block; or a `… FAILED` line.

# FINAL REPLY

- Delivery block: the title line and the message, verbatim, and nothing else, as
  the conventions' Results say.
- `Sent:`: one short line, such as "Sent the afternoon reminder.", then any
  `List:` lines the messenger returned.
- Paused today: one short line, such as "Paused today; nothing sent."

# ERROR HANDLING

After step 1, never use `/ntm:notify` for an error, including a `… FAILED` line
from a skill or the messenger. End the run with the error stated plainly in your
final reply; the scheduled task's own completion push carries it.
