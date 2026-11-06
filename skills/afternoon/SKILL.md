---
name: afternoon
description: The afternoon nudge for the user's nudge board. Asks the planner what's still planned for today and has the messenger send a midday reminder in the user's voice; never escalates. Run by the "Afternoon nudge" job, or by hand ("run the afternoon nudge now").
---

# nudge:afternoon

Afternoon nudge for the user's board. Each step names a skill or an agent: load the skill and follow it, or ask the agent and read what it returns. Skills and agents return text; you decide what reaches the user. If an agent can't be spawned, read its file in the plugin's `agents/` folder (beside `skills/`: `agents/planner.md`, `agents/messenger.md`), load the skills it names, and follow its section for the request yourself.

# 1: Load the board rules
Load `nudge:board` before anything else: it holds the board's rules, and every later step follows them.

# 2: Verify the tracker connection
Run `/nudge:ping --notify --job "Afternoon nudge"`.
**If this fails, STOP: end the run with its result line and nothing more.**

# 3: What's still open
Ask the planner agent: `what's due`. It returns `/nudge:due`'s result and, when nothing is due, the days-off check for today. Read it:
- Anything listed: nudge about it, whatever its labels or status, even on a day off: the user dated it themselves, so it should just work. The board rules' exclusions are for picking work, not for reminders about work they dated. Each due line ends with the ticket's labels in brackets; leave out any ticket whose brackets hold the config's `deadline label` and whose planned date is before today.
- `Nothing due today.` and the days-off line ends `true`: the user is taking the day off. STOP and send nothing.
- `Nothing due today.` otherwise: they already handled today; step 4 sends quick props.
- Any `… FAILED` line: ERROR HANDLING.

# 4: Send the nudge
Ask the messenger agent with the beat, the job name and the facts, one per line:

```
afternoon: Afternoon nudge
open: ABC-9 Clear the garage shelf <url> (started)
```

One `open:` line per ticket still open, marked `(started)` when its status is the config's `started status`; or the single line `nothing open`. The messenger writes the message in the user's voice, sends it, and returns `Sent: <title>`, a delivery block starting `NOTIFY VIA FINAL REPLY`, or `Send FAILED: …`.

# FINAL REPLY
Unless reporting an error, end the run with one short line saying what happened, such as "Sent the afternoon nudge." or "Day off; nothing sent." When the messenger returned a delivery block, the final reply is everything after its first line, verbatim, as the board rules' Results say.

# ERROR HANDLING
If step 2 fails, end with the ping's result line and nothing more; that line is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, don't use `/nudge:notify`: end the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
