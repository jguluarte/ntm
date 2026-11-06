# Weekly planning

Header; not part of the prompt. This prompt is the sequence itself; there is no `ntm:weekly-planning` skill.

| | |
| --- | --- |
| Default title | Weekly planning |
| Suggested schedule | `CRON_TZ=<timezone from About you in your settings> 0 22 * * 0` (Sunday 22:00, before the jitter rule) |
| Connectors | the backend connector named by Board in your settings. Never a browser. |
| Notifications | push on |

--- prompt ---

Weekly planning for the board: close out last week and start the next one knowing what's coming. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Steps 2 to 4 go to the planner agent and step 5 to the messenger agent, handed these steps as text, when they're loaded. When one isn't, do its steps yourself with the same skills. Say nothing to the user about it either way.

1. Run `/ntm:ready-check --notify --job "Weekly planning"`. If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.
2. Load `ntm:conventions` and `ntm:show-completed`, and run `/ntm:show-completed the last 7 days and what's still open`, before the fix, so it counts nothing the fix closes. Its `Done (<n>):` lines are what got done (`Done: none` when nothing was); its `Still open (<n>):` lines are what's still open from last week. If it returns `Show-completed FAILED`, carry on: it isn't an error here, and step 5 passes `done: unavailable`.
3. Load `ntm:fix-todo-list` and run `/ntm:fix-todo-list`, so planning works from a clean board. Its result is for the FINAL REPLY, exactly as returned. If it returns `Fix-todo-list FAILED`, carry on: it isn't an error here; the FINAL REPLY shows the line.
4. Load `ntm:plan` and run `/ntm:plan --auto week`. Its `Planned <date>:` lines are the week ahead. `Plan FAILED`, or any other `… FAILED` line: ERROR HANDLING.
5. Compose and send, with the beat, the job name and the facts, one per line:

   ```
   week: Weekly planning
   done: ABC-12 Order storage boxes <url>
   planned: 2026-11-09: ABC-15 Hang the garage shelf (~1 h) <url>
   open: ABC-9 Clear the garage shelf <url>
   ```

   One `done:` line per Done ticket, or `done: none`, or `done: unavailable` when step 2 failed. Then one `planned:` line per `Planned <date>:` line the plan returned, its day first as the example shows, leaving out the plan's reasons and its `paused` and `nothing to plan` days; or `nothing to plan` when nothing got planned. Then one `open:` line per Still open ticket, when there are any. The facts are everything the message may say; add none.

   1. Load `ntm:conventions`, `ntm:style-message` and `ntm:notify`.
   2. Write a sentence or so for each half: last week (what got done, naming each `open:` id as still open from last week), then the week ahead (what's coming and what the week is shaping up to be about; with `nothing to plan`, say so). With `done: unavailable`, there's nothing to look back on: the week ahead only.
   3. Run them through `/ntm:style-message --for week "<tone>" <sentences>`, with a tone that opens with the job name (`Weekly planning; …`), then both halves: what got done and its count, each still-open id, and the week ahead. Style-message returns the message with `Title: …` as its last line (with no style configured, your sentences as given plus that line).
   4. No list of days or tickets under it, and nothing about the fix.
   5. Send with `/ntm:notify --job "Weekly planning" --title "<the words after Title:>" --message "<everything above the Title line>"`.
   6. The result is exactly one of: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in this step takes its place.

FINAL REPLY: when step 5 returned a delivery block, the final reply is the title line and the message, verbatim, then fix-todo-list's result exactly as returned (and show-completed's `Show-completed FAILED` line after it when it failed), and nothing else. This job is the one the conventions' Results names as adding fix-todo-list's result after the message. Otherwise (the Pushover case) end the run with one short line saying what happened, such as "Sent the weekly planning message.", or the error stated plainly. Then fix-todo-list's result exactly as returned, and show-completed's `Show-completed FAILED` line after it when it failed.

ERROR HANDLING: if step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. A failed show-completed or fix-todo-list isn't an error here (see steps 2 and 3). For any other error, including `Plan FAILED` or a `… FAILED` line from step 5, never use `/ntm:notify`. Stop and end the run as FINAL REPLY says; the scheduled task's own completion push carries it.
