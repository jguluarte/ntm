---
name: evening-reminder
description: >-
    The evening reminder for the user's todo list: a friend asking how the day
    went. What closed, what's still open, and the evening message in the user's
    style. Run by a job, or by hand ("run the evening reminder now").
---

# ntm:evening-reminder

The evening reminder: a friend asking how the day went. `ntm:show-completed`
gives the facts; the messenger agent writes and sends the message. This skill
names the steps, the handoff and what ends the run. When the messenger agent
isn't available in this session, do what the conventions' "Chat, jobs and
agents" says: read its file from the installed plugin and follow it yourself.

# 1: Ready check

Run `/ntm:ready-check --notify-failure evening-reminder`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `ntm:show-completed` and run
`/ntm:show-completed today, and what's still open, planned today or earlier`.

- Nothing done and nothing still open: assume a day off. STOP and send nothing.
- Otherwise the facts are one `done:` line per Done task, or `done: none`; then
  one `open:` line per Still open task, with `was` its planned date when that's
  before today, or `open: none`. Each task is a task line, as the messenger
  agent's "What you're given" says, with no estimate.
- `Show-completed FAILED`: ERROR HANDLING.

# 3: The message

Ask the messenger agent, with the reminder, the job and the facts:

```
reminder: evening
job: evening-reminder
<the facts>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't
carry the list), a delivery block, or a `… FAILED` line.

# FINAL REPLY

When the messenger returned a delivery block, the final reply is the title line
and the message, verbatim, and nothing else, as the conventions' Results say.
Otherwise, unless reporting an error, end the run with one short line saying
what happened, such as "Sent the evening reminder." That line is for the
Pushover case; when the messenger returned lines after `Sent:` (the list the
push couldn't carry), they follow it.

# ERROR HANDLING

If step 1 fails, end with what the ready check returned, and nothing more; that
is what reaches the user. For any later error, including a `… FAILED` line from
show-completed or the messenger, never use `/ntm:notify`. End the run with the
error stated plainly in your final reply; the scheduled task's own completion
push carries it.
