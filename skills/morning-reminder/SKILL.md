---
name: morning-reminder
description: >-
    The morning reminder for the user's todo list: what's on the table today.
    Carries stale planned work to today, plans today if it's empty, and sends
    the morning message in the user's style. Run by a job, or by hand ("run the
    morning reminder now").
---

# neurodivergent-task-manager:morning-reminder

The morning reminder: what's on the table today, said the way the user reads.
`neurodivergent-task-manager:plan` makes today ready and returns the facts; the
messenger agent writes and sends the message. This skill names the steps, the
handoff and what ends the run. When the messenger agent isn't available in this
session, do what the conventions' "Chat, jobs and agents" says: read its file
from the installed plugin and follow it yourself.

# 1: Ready check

Run `/ntm:ready-check --notify-failure morning-reminder`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `neurodivergent-task-manager:plan` and run
`/neurodivergent-task-manager:plan --auto day`. It carries stale work to today,
plans today if it's empty, and returns the facts as lines.

Read what comes back:

- `paused`: the user has paused today. STOP and send nothing.
- `today:` lines, or `today: none`: the facts for the message. Leave `kept:` and
  `couldn't move:` lines out of what you hand the messenger; they're for the
  final reply.
- Any `… FAILED` line: ERROR HANDLING.

# 3: The message

Ask the messenger agent, with the reminder, the job and the facts:

```
reminder: morning
job: morning-reminder
<the facts>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't
carry the list), a delivery block, or a `… FAILED` line.

# FINAL REPLY

When the messenger returned a delivery block, the final reply is the title line
and the message, verbatim, then any `kept:` and `couldn't move:` lines from plan
as they came, and nothing else. Otherwise, unless reporting an error, end the
run with one short line saying what happened, such as "Sent the morning
reminder." or "Paused today; nothing sent.", then any `kept:` and
`couldn't move:` lines. That line is for the Pushover case; when the messenger
returned lines after `Sent:` (the list the push couldn't carry), they follow it.

# ERROR HANDLING

If step 1 fails, end with what the ready check returned, and nothing more; that
is what reaches the user. For any later error, including a `… FAILED` line from
plan or the messenger, never use `/ntm:notify`. End the run with the error
stated plainly in your final reply; the scheduled task's own completion push
carries it.
