---
name: morning-reminder
description: >-
    The morning reminder for the user's todo list: what's on the table today.
    Carries stale planned work to today, plans today if it's empty, and sends
    the morning message in the user's style. Run by the "Morning reminder" job,
    or by hand ("run the morning reminder now").
---

# ntm:morning-reminder

What's on the table today, in the user's style. `ntm:plan` makes today ready and
lists today's tasks; the messenger agent writes and sends the message. If the
messenger isn't available in this session, follow the conventions' "Chat, jobs
and agents".

# 1: Ready check

Run `/ntm:ready-check --notify-failure "Morning reminder"`.

**If it returns `Ready-check FAILED`, STOP: end the run with what it returned
and nothing more.**

# 2: Today's plan

Load `ntm:plan` and run `/ntm:plan --auto day`. It carries stale work to today,
plans today if it's empty, and returns lines:

- `paused`: today is paused. Send nothing: skip step 3 and go to FINAL REPLY.
- `today:` lines, or `today: none`: what the message is about.
- `kept:` and `couldn't move:` lines: keep these for the final reply; don't hand
  them to the messenger.
- Any `… FAILED` line: go to ERROR HANDLING.

# 3: The message

Ask the messenger agent:

```
reminder: morning
job: Morning reminder
<the today: lines>
```

It returns one of:

- `Sent: <title>`: the notification went out. `List:` lines follow when it was
  too short for the list.
- A delivery block: the title line and the message text, returned when no
  notification was sent.
- A `… FAILED` line.

# FINAL REPLY

If nothing failed, start with one of these:

- Delivery block: the title line and the message, verbatim.
- `Sent:`: one short line, such as "Sent the morning reminder.", then any
  `List:` lines the messenger returned.
- Paused today: one short line, such as "Paused today; nothing sent."

Then add any `kept:` and `couldn't move:` lines from plan as they came, and
nothing else. On a `… FAILED` line, see ERROR HANDLING instead.

# ERROR HANDLING

After step 1 (which notifies on its own), never use `/ntm:notify` for an error,
including a `… FAILED` line from plan or the messenger. End the run with the
error stated plainly in your final reply; the notification the scheduled task
sends when it finishes carries it.
