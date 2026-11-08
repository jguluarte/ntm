---
name: weekly-planning
description: >-
    The weekly planning for the user's todo list: closes out the week (what got
    done, what's still open), tidies the todo list, plans the week ahead as
    Planning in the user's settings defines it, and sends one message with both
    halves in the user's style. Run by the "Weekly planning" job, or by hand
    ("run the weekly planning now").
---

# ntm:weekly-planning

The weekly planning: close out the week and start the next one knowing what's
coming. `ntm:plan` closes out the week, plans the next and returns the facts;
the messenger agent writes and sends the message. This skill names the steps,
the handoff and what ends the run. When the messenger agent isn't available in
this session, do what the conventions' "Chat, jobs and agents" says: read its
file from the installed plugin and follow it yourself.

# 1: Ready check

Run `/ntm:ready-check --notify-failure "Weekly planning"`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: The facts

Load `ntm:plan` and run `/ntm:plan --auto week`. It reports the week, tidies the
todo list, plans the week ahead, and returns the facts as lines.

Read what comes back:

- `done:`, `open:` and `planned:` lines (or `done: none`, `done: unavailable`,
  `open: none`, `planned: none`): the facts for the message. Leave the `fix:`
  and `couldn't move:` lines out of what you hand the messenger; they're for the
  final reply.
- `Plan FAILED`: ERROR HANDLING.

# 3: The message

Ask the messenger agent, with the reminder, the job, what the weekly message
covers and the facts:

```
reminder: week
job: Weekly planning
weekly message: <from this job's prompt, or ntm:plan's default>
<the facts>
```

It returns `Sent: <title>`, a delivery block, or a `… FAILED` line.

# FINAL REPLY

When the messenger returned a delivery block, the final reply is the title line
and the message, verbatim, then every `fix:` line from plan with its `fix: `
prefix removed (fix-todo-list's result; this is the one job the conventions'
Results names as adding it after the message), then any `couldn't move:` lines,
and nothing else. Otherwise, unless reporting an error, end the run with one
short line saying what happened, such as "Sent the weekly planning message.",
then the `fix:` lines the same way and any `couldn't move:` lines. That line is
for the Pushover case.

# ERROR HANDLING

If step 1 fails, end with what the ready check returned, and nothing more; that
is what reaches the user. For any later error, including a `… FAILED` line from
plan or the messenger, never use `/ntm:notify`. End the run with the error
stated plainly in your final reply; the scheduled task's own completion push
carries it.
