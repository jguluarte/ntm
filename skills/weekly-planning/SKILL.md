---
name: weekly-planning
description: The weekly planning for the user's ntm board. Closes out last week (what got done, what's still open), tidies the board, plans the week ahead, and sends one message with both halves in the user's style. Run by the "Weekly planning" job, or by hand ("run the weekly planning now").
---

# ntm:weekly-planning

Weekly planning for the user's board: close out last week and start the next one knowing what's coming. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Steps 2 and 3 hand their numbered steps to an agent as text when it's loaded. When it isn't, do the same steps yourself with the same skills. Say nothing to the user about it either way.

# 1: Ready check
Run `/ntm:ready-check --notify --job "Weekly planning"`.
**If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.**

# 2: Close out last week and plan the next
Hand the planner agent these steps, or do them yourself:

1. Load `ntm:conventions` and `ntm:show-completed`, and run `/ntm:show-completed the last 7 days and what's still open`, before the fix, so it counts nothing the fix closes. Its `Done (<n>):` lines are what got done (`Done: none` when nothing was); its `Still open (<n>):` lines are what's still open from last week. `Show-completed FAILED` isn't an error here: carry on, and return the line where its result would go.
2. Load `ntm:fix-todo-list` and run `/ntm:fix-todo-list`, so planning works from a clean board. `Fix-todo-list FAILED` isn't an error here either: carry on.
3. Load `ntm:plan` and run `/ntm:plan --auto week`. Its `Planned <date>:` lines are the week ahead.
4. Return show-completed's result, then fix-todo-list's result exactly as returned, then plan's result. When plan returns `Plan FAILED: …`, return that line where its result would go and stop there.

Read what comes back:
- What got done: the `Done` lines, or none, or unavailable when show-completed failed. What's still open: the `Still open` lines.
- The week ahead: the `Planned <date>:` lines, leaving out the plan's reasons and its `paused` and `nothing to plan` days; or nothing to plan when it planned nothing.
- Fix-todo-list's result is for the FINAL REPLY, exactly as returned.
- `Plan FAILED`, or any other `… FAILED` line but show-completed's and fix-todo-list's: ERROR HANDLING.

# 3: Send the weekly message
Hand the messenger agent these steps, with the beat, the job name and the facts, one per line:

```
week: Weekly planning
done: ABC-12 Order storage boxes <url>
planned: 2026-11-09: ABC-15 Hang the garage shelf (~1 h) <url>
open: ABC-9 Clear the garage shelf <url>
```

One `done:` line per Done ticket, or `done: none`, or `done: unavailable` when show-completed failed. Then one `planned:` line per `Planned <date>:` line, its day first as the example shows; or `nothing to plan`. Then one `open:` line per Still open ticket, when there are any. The facts are everything the message may say; add none.

The messenger's steps, or do them yourself:

1. Load `ntm:conventions`, `ntm:style-message` and `ntm:notify`.
2. Write a sentence or so for each half: last week (what got done, naming each `open:` id as still open from last week), then the week ahead (what's coming and what the week is shaping up to be about; with `nothing to plan`, say so). With `done: unavailable`, there's nothing to look back on: the week ahead only.
3. Run them through `/ntm:style-message --for week "<tone>" <sentences>`, with a tone that opens with the job name (`Weekly planning; …`), then both halves: what got done and its count, each still-open id, and the week ahead. Style-message returns the message with `Title: …` as its last line (with no style configured, your sentences as given plus that line).
4. No list of days or tickets under it, and nothing about the fix.
5. Send with `/ntm:notify --job "Weekly planning" --title "<the words after Title:>" --message "<everything above the Title line>"`.
6. Return exactly one of these, unchanged, and nothing else: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in these steps comes back the same way, in place of the send.

# FINAL REPLY
When the messenger returned a delivery block, the final reply is the title line and the message, verbatim, then fix-todo-list's result exactly as returned (and show-completed's `Show-completed FAILED` line after it when it failed), and nothing else. This is the one job the conventions' Results names as adding fix-todo-list's result after the message. Otherwise, unless reporting an error, end the run with one short line saying what happened, such as "Sent the weekly planning message.", then fix-todo-list's result exactly as returned, and show-completed's `Show-completed FAILED` line after it when it failed. That line is for the Pushover case.

# ERROR HANDLING
If step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. A failed show-completed or fix-todo-list isn't an error here (see step 2). For any other error, including `Plan FAILED` or a `… FAILED` line from the messenger, never use `/ntm:notify`. End the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
