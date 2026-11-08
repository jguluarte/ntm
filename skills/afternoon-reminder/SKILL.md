---
name: afternoon-reminder
description: >-
    The afternoon reminder for the user's todo list: a tap on the shoulder about
    what's still open today, with started work marked; never a dig. Run by the
    "Afternoon reminder" job, or by hand ("run the afternoon reminder now").
---

# ntm:afternoon-reminder

`ntm:today` gives the facts; the messenger agent writes the message in the
user's style and sends it. If the messenger isn't available in this session,
read its file from the installed plugin and follow it yourself (see "Chat, jobs
and agents" in `ntm:conventions`).

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
when the `/ntm:today` output marks the task started.

Remind about everything listed, whatever its labels or status, even on a paused
day: the user dated it.

When it lists nothing, run `/ntm:pause --check`. If it reports today as paused
(the line for today ends `true`), STOP and send nothing. Otherwise the facts are
`open: none`.

On any `… FAILED` line, go to ERROR HANDLING.

# 3: The message

Ask the messenger agent:

```
reminder: afternoon
job: Afternoon reminder
<the facts>
```

It returns one of:

- `Sent: <title>`, followed by a `List:` line and the list when the push
  couldn't carry it.
- A delivery block: `NOTIFY VIA FINAL REPLY`, then the title and the message.
- A `… FAILED` line: go to ERROR HANDLING.

# FINAL REPLY

Unless reporting an error:

- Delivery block: the title line and the message, verbatim, and nothing else, as
  Results in `ntm:conventions` says.
- `Sent:`: one short line, such as "Sent the afternoon reminder.", then the
  `List:` line and the list, verbatim, if the messenger returned them.
- Paused today: one short line, such as "Paused today; nothing sent."

# ERROR HANDLING

After step 1, never use `/ntm:notify` for an error, including a `… FAILED` line
from a skill or the messenger. End the run with the error stated plainly in your
final reply; the scheduled task's own completion push carries it.
