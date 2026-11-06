---
name: morning
description: The morning plan for the user's nudge board. Has the planner carry missed work to today and plan today if it's empty, then has the messenger send the morning message in the user's voice. Run by the "Morning plan" job, or by hand ("run the morning plan now").
---

# nudge:morning

Morning plan for the user's board. Each step names a skill or an agent: load the skill and follow it, or ask the agent and read what it returns. Skills and agents return text; you decide what reaches the user. If an agent can't be spawned, read its file in the plugin's `agents/` folder (beside `skills/`: `agents/planner.md`, `agents/messenger.md`), load the skills it names, and follow its section for the request yourself.

# 1: Load the board rules
Load `nudge:board` before anything else: it holds the board's rules, and every later step follows them.

# 2: Verify the tracker connection
Run `/nudge:ping --notify --job "Morning plan"`.
**If this fails, STOP: end the run with its result line and nothing more.**

# 3: Make today ready
Ask the planner agent: `make today ready`. It carries missed work to today, plans today if it's empty, and returns `/nudge:due`'s result, any `Moved to today:` and `Couldn't move:` lines, and `/nudge:plan --daily`'s result when it ran. Read it:
- Today's tasks: the due lines planned for today, the tickets in `Moved to today:` (each with the date it had), and plan's picks. Anything in `Couldn't move:` stays out of the message.
- `No task today: day off.` with nothing moved to today: STOP and send nothing. The user is taking the day off.
- `No task today: nothing to plan.`: the board has nothing left to plan; step 4 nudges them to groom instead of writing about an empty day.
- Any `… FAILED` line: ERROR HANDLING.

# 4: Send the morning message
Ask the messenger agent with the beat, the job name and the facts, one per line:

```
morning: Morning plan
today: ABC-12 Order storage boxes (~10 min) <url>
today: ABC-9 Clear the garage shelf <url> (was 2026-11-03)
```

One `today:` line per task, spelled as plan does, `<id> <title> (~<time>) <url>`, keeping plan's `(~<time>)` where it gave one, with `(was <date>)` after on each carried-over ticket; or the single line `nothing to plan`. The messenger writes the message in the user's voice, sends it, and returns `Sent: <title>`, a delivery block starting `NOTIFY VIA FINAL REPLY`, or `Send FAILED: …`.

# FINAL REPLY
Unless reporting an error, end the run with one short line saying what happened, such as "Sent the morning push." or "Day off; nothing sent." When the messenger returned a delivery block, the final reply is everything after its first line, verbatim, as the board rules' Results say.

# ERROR HANDLING
If step 2 fails, end with the ping's result line and nothing more; that line is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, don't use `/nudge:notify`: end the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
