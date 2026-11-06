---
name: evening
description: The evening check-in for the user's nudge board. Asks the planner how today went, what closed and what's still open, and has the messenger send tonight's check-in in the user's voice: an affirmation, or a nudge about what's still open. Run by the "Evening check-in" job, or by hand ("run the evening check-in now").
---

# nudge:evening

Evening check-in for the user's board. Each step names a skill or an agent: load the skill and follow it, or ask the agent and read what it returns. Skills and agents return text; you decide what reaches the user. If an agent can't be spawned, read its file in the plugin's `agents/` folder (beside `skills/`: `agents/planner.md`, `agents/messenger.md`), load the skills it names, and follow its section for the request yourself.

# 1: Load the board rules
Load `nudge:board` before anything else: it holds the board's rules, and every later step follows them.

# 2: Verify the tracker connection
Run `/nudge:ping --notify --job "Evening check-in"`.
**If this fails, STOP: end the run with its result line and nothing more.**

# 3: How did today go
Ask the planner agent: `how did today go`. It returns `/nudge:recap today, include open tickets`'s result: everything closed today under `Done`, and everything still open that was planned for today under `Still open`. A `… FAILED` line: ERROR HANDLING.

# 4: If nothing came back
If nothing was closed and nothing is open, assume today was a day off. STOP and send nothing.

# 5: Send the evening message
Ask the messenger agent with the beat, the job name and the facts, one per line:

```
evening: Evening check-in
done: ABC-12 Order storage boxes <url>
open: ABC-9 Clear the garage shelf <url>
```

One `done:` line per ticket closed today, or `done: none` when nothing was closed (never infer it from absence); then one `open:` line per ticket still open, or `nothing open` when there are none. The messenger writes the message in the user's voice, sends it, and returns `Sent: <title>`, a delivery block starting `NOTIFY VIA FINAL REPLY`, or `Send FAILED: …`.

# FINAL REPLY
Unless reporting an error, end the run with one short line saying what happened, such as "Sent the evening push." or "Day off; nothing sent." When the messenger returned a delivery block, the final reply is everything after its first line, verbatim, as the board rules' Results say.

# ERROR HANDLING
If step 2 fails, end with the ping's result line and nothing more; that line is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, don't use `/nudge:notify`: end the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
