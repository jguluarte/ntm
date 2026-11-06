---
name: afternoon-reminder
description: The afternoon reminder for the user's todo list: a tap on the shoulder about what's still open today, with started work marked; never a dig. Run by the "Afternoon reminder" job, or by hand ("run the afternoon reminder now").
---

# ntm:afternoon-reminder

The afternoon reminder: a tap on the shoulder about what's still open. Two agents do the work: the planner gathers the facts, the messenger writes and sends the message. This skill names the request, the handoff and what ends the run. When an agent isn't available in this session, do what the conventions' "Chat, jobs and agents" says: read its file from the installed plugin and follow it yourself.

# 1: Ready check
Run `/ntm:ready-check --notify-failure --job "Afternoon reminder"`.
**If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.**

# 2: The facts
Ask the planner agent: **what's still open** (its request of that name in `agents/planner.md`). It returns the facts as lines.

Read what comes back:
- `paused`: nothing open and the user has paused today. STOP and send nothing.
- `open:` lines, or `open: none`: the facts for the message.
- Any `… FAILED` line: ERROR HANDLING.

# 3: The message
Ask the messenger agent, with the beat, the job and the planner's lines:

```
beat: afternoon
job: Afternoon reminder
<the planner's lines>
```

It returns `Sent: <title>` (followed by `List:` lines when the push couldn't carry the list), a delivery block, or a `… FAILED` line.

# FINAL REPLY
When the messenger returned a delivery block, the final reply is the title line and the message, verbatim, and nothing else, as the conventions' Results say. Otherwise, unless reporting an error, end the run with one short line saying what happened, such as "Sent the afternoon reminder." or "Paused today; nothing sent." That line is for the Pushover case; when the messenger returned lines after `Sent:` (the list the push couldn't carry), they follow it.

# ERROR HANDLING
If step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, never use `/ntm:notify`. End the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
