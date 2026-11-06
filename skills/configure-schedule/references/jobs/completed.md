# Completed this week / Completed this month

Header; not part of the prompt. Off by default: offer it, and create it only when the user wants it. This prompt is the sequence itself; there is no skill for it.

| | |
| --- | --- |
| Default title | Completed this week (weekly) or Completed this month (monthly) |
| Suggested schedule | weekly: `CRON_TZ=<timezone from About you in your settings> 0 20 * * 0` (Sunday 20:00); monthly: `CRON_TZ=<timezone from About you in your settings> 0 20 1 * *` (the 1st, 20:00); both before the jitter rule |
| Span | weekly: `the last 7 days`; monthly: `last month`. The prompt below is the weekly one; for monthly, replace every `Completed this week` with the monthly title, every `this week` with `this month`, and `the last 7 days` with `last month`. |
| Connectors | the backend connector named by Board in your settings. Never a browser. |
| Notifications | push on |

--- prompt ---

Completed this week: what got done on the board. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Step 2 goes to the planner agent and step 3 to the messenger agent, handed these steps as text, when they're loaded. When one isn't, do its steps yourself with the same skills. Say nothing to the user about it either way.

1. Run `/ntm:ready-check --notify --job "Completed this week"`. If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.
2. Load `ntm:conventions` and `ntm:show-completed`, and run `/ntm:show-completed the last 7 days`. Its `Done (<n>):` lines are what got done; `Done: none` means nothing was. `Show-completed FAILED`: ERROR HANDLING.
3. Compose and send, with the job name and the facts, one per line:

   ```
   completed: Completed this week
   done: ABC-12 Order storage boxes <url>
   ```

   One `done:` line per Done ticket, or `done: none`. The facts are everything the message may say; add none.

   1. Load `ntm:conventions`, `ntm:style-message` and `ntm:notify`.
   2. Write a sentence or so on what got done over the span, with the count; with `done: none`, that nothing closed, plainly.
   3. Run it through `/ntm:style-message --stay-fresh "<tone>" <sentence>`, with a tone that opens with the job name (`Completed this week; …`), then the count and what got done. Style-message returns the message (with no style configured, your sentence as given).
   4. Under the styled line, what got done, one line each: the ticket id linked to its url, worded as the conventions' "Talking to the user about tickets" says. With `done: none`, no list.
   5. Send with `/ntm:notify --job "Completed this week" --title "Completed this week" --message "<the styled line, with the list under it>"`.
   6. The result is exactly one of: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in this step takes its place.

FINAL REPLY: when step 3 returned a delivery block, the final reply is the title line and the message, verbatim, and nothing else, as the conventions' Results say. Otherwise (the Pushover case) end the run with one short line saying what happened, such as "Sent what got done this week.", or the error stated plainly.

ERROR HANDLING: if step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. For any other error, including `Show-completed FAILED` or a `… FAILED` line from step 3, never use `/ntm:notify`. Stop and end the run as FINAL REPLY says; the scheduled task's own completion push carries it.
