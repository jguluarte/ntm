---
name: week
description: The weekly recap and plan for the user's nudge board. Has the planner recap the week, clean up the board and plan the week ahead, then has the messenger send one message in the user's voice. Run by the "Weekly recap and plan" job on Sunday night, or by hand ("run the weekly recap now").
---

# nudge:week

Weekly recap and plan for the user's board, run Sunday night so the user closes out last week and starts the next one knowing what's coming. Each step names a skill or an agent: load the skill and follow it, or ask the agent and read what it returns. Skills and agents return text; you decide what reaches the user. If an agent can't be spawned, read its file in the plugin's `agents/` folder (beside `skills/`: `agents/planner.md`, `agents/messenger.md`), load the skills it names, and follow its section for the request yourself.

# 1: Load the board rules
Load `nudge:board` before anything else: it holds the board's rules, and every later step follows them.

# 2: Verify the tracker connection
Run `/nudge:ping --notify --job "Weekly recap and plan"`.
**If this fails, STOP: end the run with its result line and nothing more.**

# 3: Recap, clean up, plan
Ask the planner agent: `plan the week`. It recaps the last 7 days, open tickets included, before cleanup, so the recap doesn't count anything cleanup closes; cleans up, so planning works from a clean board; then plans the week with `/nudge:plan --weekly`, and returns the three results in that order. Read it:
- The recap's `Done` lines are what the user got done. The recap's `Still open` lines are what's still open from last week. `Recap FAILED` isn't an error here: step 4 passes `no recap`.
- Cleanup's result is for FINAL REPLY, exactly as returned. `Cleanup FAILED` isn't an error here either.
- The plan is what's coming. `Plan FAILED`, or any other `… FAILED` line: ERROR HANDLING.

# 4: Send the message
Ask the messenger agent with the beat, the job name and the facts, one per line:

```
week: Weekly recap and plan
done: ABC-12 Order storage boxes <url>
planned: 2026-11-09: ABC-15 Hang the garage shelf (~1 h) <url>
open: ABC-9 Clear the garage shelf <url>
```

One `done:` line per ticket the recap lists, or `done: none`, or `no recap` when the recap failed; then one `planned:` line per ticket the plan dated, its day first as the example shows, leaving out the plan's reasons and its `day off` / `nothing to plan` days, or `nothing to plan` when nothing got planned; then one `open:` line per `Still open` ticket, when there are any. The messenger writes one message with two halves, last week then the week ahead, in the user's voice, sends it, and returns `Sent: <title>`, a delivery block starting `NOTIFY VIA FINAL REPLY`, or `Send FAILED: …`.

# FINAL REPLY
End the run with one short line saying what happened, such as "Sent the weekly recap and week ahead.", or the error stated plainly. Then add cleanup's result exactly as the planner returned it, and the recap's result line after it when the recap failed. When the messenger returned a delivery block, the final reply is instead everything after its first line, verbatim, as the board rules' Results say, and cleanup's result and the recap's result line go to this thread with SendUserMessage, so the push stays the message.

# ERROR HANDLING
If step 2 fails, end with the ping's result line as it returned it, and nothing more; that line is what reaches the user. A failed recap or cleanup isn't an error here (see step 3). For any other error, including `Plan FAILED` or a `… FAILED` line from the messenger, don't use `/nudge:notify`: stop and end the run as FINAL REPLY says; the scheduled task's own completion push carries it.
