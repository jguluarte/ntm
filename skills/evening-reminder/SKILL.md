---
name: evening-reminder
description: The evening reminder for the user's ntm board. Looks at how today went, what closed and what's still open, and sends tonight's message in the user's style: an affirmation when nothing is open, otherwise what the style says about work that keeps slipping. Run by the "Evening reminder" job, or by hand ("run the evening reminder now").
---

# ntm:evening-reminder

Evening reminder for the user's board, a friend asking how the day went. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Steps 2 and 4 hand their numbered steps to an agent as text when it's loaded. When it isn't, do the same steps yourself with the same skills. Say nothing to the user about it either way.

# 1: Ready check
Run `/ntm:ready-check --notify --job "Evening reminder"`.
**If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.**

# 2: How did today go
Hand the planner agent these steps, or do them yourself:

1. Load `ntm:conventions` and `ntm:show-completed`. Compute `TODAY` as the conventions' Dates section says.
2. Run `/ntm:show-completed today and what's still open` and return its result.

Read what comes back: the `Done (<n>):` lines are what closed today (`Done: none` when nothing did); the `Still open (<n>):` lines are what's still open that was planned for today. Any `… FAILED` line: ERROR HANDLING.

# 3: If nothing came back
If nothing closed today and nothing is still open, assume today was paused. STOP and send nothing.

# 4: Send the evening message
Hand the messenger agent these steps, with the beat, the job name and the facts, one per line:

```
evening: Evening reminder
done: ABC-12 Order storage boxes <url>
open: ABC-9 Clear the garage shelf <url>
```

One `done:` line per ticket closed today, or `done: none` when nothing closed (never infer it from absence). Then one `open:` line per ticket still open, `<id> <title> <url>`, or `nothing open` when there are none. An open ticket gets `(was <date>, carried <n> days)` after it when its planned date is before `TODAY` (`n` being `TODAY` minus that date in calendar days; `carried 1 day` when it's one). The facts are everything the message may say; add none.

The messenger's steps, or do them yourself:

1. Load `ntm:conventions`, `ntm:style-message` and `ntm:notify`.
2. Write one or two sentences for the evening: with open tickets, how the day went and what's still open, naming each open id; with `nothing open`, an affirmation for the day, naming what got done.
3. Run them through `/ntm:style-message --for evening "<tone>" <sentences>`, with a tone that opens with the job name (`Evening reminder; …`), then each still-open id with its `(was <date>, carried <n> days)` when given, or that nothing is open and what got done. What each open ticket gets is the style's When something keeps slipping, by the history count `style-message` computes; nothing open gets the register of its "nothing open" example. When the style's What gets you to read names a scoreboard (load `ntm-user:style` and read its What gets you to read), load `ntm:show-completed`, run `/ntm:show-completed this week`, and put its Done count in the tone. Style-message returns the message with `Title: …` as its last line (with no style configured, your sentences as given plus that line).
4. Under the styled lines, what's still open, one line each: the ticket as a linked ticket, exactly as the conventions' "Talking to the user about tickets" says, with its `(was <date>, carried <n> days)` when given. With `nothing open`, no list.
5. Send with `/ntm:notify --job "Evening reminder" --title "<the words after Title:>" --message "<everything above the Title line, with the list under it>"`.
6. Return exactly one of these, unchanged, and nothing else: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in these steps comes back the same way, in place of the send.

# FINAL REPLY
When the messenger returned a delivery block, the final reply is the title line and the message, verbatim, and nothing else, as the conventions' Results say. Otherwise, unless reporting an error, end the run with one short line saying what happened, such as "Sent the evening reminder." or "Paused today; nothing sent." That line is for the Pushover case.

# ERROR HANDLING
If step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, never use `/ntm:notify`. End the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
