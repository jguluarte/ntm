---
name: afternoon-reminder
description: >-
    The afternoon reminder for the user's todo list: a tap on the shoulder about
    what's still open today, with started work marked; never a dig. Run by a
    job, or by hand ("run the afternoon reminder now").
---

# neurodivergent-task-manager:afternoon-reminder

The afternoon reminder: a tap on the shoulder about what's still open.
`neurodivergent-task-manager:today` gives the facts; the messenger agent writes
and sends the message. This skill names the steps, the handoff and what ends the
run. When the messenger agent isn't available in this session, do what the
conventions' "Chat, jobs and agents" says: read its file from the installed
plugin and follow it yourself.

# 1: Ready check

Run `/ntm:ready-check --notify-failure afternoon-reminder`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `neurodivergent-task-manager:today` and
`neurodivergent-task-manager:pause`, and run
`/neurodivergent-task-manager:today`.

- Tasks listed: the facts are one `open:` line per task, a task line as the
  messenger agent's "What you're given" says, with no estimate, `was` its
  planned date when that's before today, and `started` when today marked it so.
  Remind about everything listed, whatever its labels or status, even on a
  paused day: the user dated it.
- Nothing listed: run `/neurodivergent-task-manager:pause --check`. Paused (its
  line for today ends `true`): STOP and send nothing. Otherwise the facts are
  `open: none`.
- Any `… FAILED` line: ERROR HANDLING.

# 3: The message

Ask the messenger agent, with the reminder, the job and the facts:

```
reminder: afternoon
job: afternoon-reminder
<the facts>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't
carry the list), a delivery block, or a `… FAILED` line.

# FINAL REPLY

When the messenger returned a delivery block, the final reply is the title line
and the message, verbatim, and nothing else, as the conventions' Results say.
Otherwise, unless reporting an error, end the run with one short line saying
what happened, such as "Sent the afternoon reminder." or "Paused today; nothing
sent." That line is for the Pushover case; when the messenger returned lines
after `Sent:` (the list the push couldn't carry), they follow it.

# ERROR HANDLING

If step 1 fails, end with what the ready check returned, and nothing more; that
is what reaches the user. For any later error, including a `… FAILED` line from
a skill or the messenger, never use `/ntm:notify`. End the run with the error
stated plainly in your final reply; the scheduled task's own completion push
carries it.
