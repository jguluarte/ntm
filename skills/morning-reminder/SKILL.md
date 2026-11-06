---
name: morning-reminder
description: The morning reminder for the user's ntm board. Carries stale planned work to today, plans today if it's empty, and sends the morning message in the user's style. Run by the "Morning reminder" job, or by hand ("run the morning reminder now").
---

# ntm:morning-reminder

Morning reminder for the user's board. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Steps 2 and 3 hand their numbered steps to an agent as text when it's loaded. When it isn't, do the same steps yourself with the same skills. Say nothing to the user about it either way.

# 1: Ready check
Run `/ntm:ready-check --notify --job "Morning reminder"`.
**If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.**

# 2: Make today ready
Hand the planner agent these steps, or do them yourself:

1. Load `ntm:conventions`, `ntm:todo-list` and `ntm:plan`. Compute `TODAY` as the conventions' Dates section says.
2. Run `/ntm:todo-list`. Every ticket it lists with a planned date before `TODAY` is stale. Move only tickets in the plannable class: set the planned date to `TODAY` with the guide's `set planned date` and change nothing else. Do that whatever its labels, even when one blocks another, as long as the conventions let you move that date (a deadline ticket's date never moves). A stale ticket in the blocked class keeps its date and goes to `Couldn't move: <id> (blocked)`. Do this on a paused day too: the user dated it, so it should just work.
3. If nothing is planned for `TODAY` after the moves (todo-list returned `Nothing planned for today.`, or nothing it listed could be moved), run `/ntm:plan --auto day`. It checks the pauses itself.
4. Return todo-list's result. Then, when any moved, `Moved to today: <id> (was <date>, carried <n> days), …`, `n` being `TODAY` minus the old date in calendar days (`carried 1 day` when it's one). Then, when a move failed, `Couldn't move: <id>, …` (`<id> (blocked)` for the blocked class). Then plan's result when it ran. When a skill returns `<Skill> FAILED: …`, return that line where its result would go and stop there.

Read what comes back:
- Today's tasks: the todo-list lines planned for today plus every ticket in `Moved to today:` (listed once, with its old date and days carried), and plan's `Planned <date>:` picks. Anything in `Couldn't move:` stays out of the message. A deadline ticket whose date has passed isn't moved and stays out, as it does in the afternoon.
- `No task today: paused.` with nothing moved to today: STOP and send nothing. The user has paused today.
- `No task today: nothing to plan.`: the board has nothing left to plan; step 3 asks them to groom instead of writing about an empty day.
- Any `… FAILED` line: ERROR HANDLING.

# 3: Send the morning message
Hand the messenger agent these steps, with the beat, the job name and the facts, one per line:

```
morning: Morning reminder
today: ABC-12 Order storage boxes (~10 min) <url>
today: ABC-9 Clear the garage shelf (~1 h) <url> (was 2026-11-03, carried 2 days)
```

One `today:` line per task, `<id> <title> (~<time>) <url>`, or the single line `nothing to plan`. `(~<time>)` goes on every line: plan's where it gave one, otherwise your own rough guess from the title. Each carried-over ticket gets `(was <date>, carried <n> days)` after, as `Moved to today:` gave it. The facts are everything the message may say; add none.

The messenger's steps, or do them yourself:

1. Load `ntm:conventions`, `ntm-user:style` and `ntm:notify`.
2. Write one or two sentences for the morning: today's tasks, naming each carried-over ticket id with the date it had and the days carried, as given. With `nothing to plan`, the sentences say the board has nothing left to plan and ask them to groom with `/ntm:review-todo-list`.
3. Run them through `/ntm-user:style --for morning "<tone>" <sentences>`, with a tone that opens with the job name (`Morning reminder; …`), then what's on the table: each carried-over id with its `(was <date>, carried <n> days)` as given, or that there's nothing to plan and they should groom. When the style's What gets you to read names a scoreboard (load `ntm-user:style` and read its What gets you to read), load `ntm:completed`, run `/ntm:completed this week`, and put its Done count in the tone. Style-message returns the message with `Title: …` as its last line (with no style configured, your sentences as given plus that line).
4. Under the styled lines, a blank line, then today's tasks, one per line, no bullet, single spaces: the linked ticket (as the conventions' "Talking to the user about tickets" says), then `(~<time>)`, then on a carried-over ticket `(was <date>, carried <n> days)`, as given. With `nothing to plan`, no list.
5. Send with `/ntm:notify --job "Morning reminder" --title "<the words after Title:>" --message "<everything above the Title line, with the list under it>"`.
6. Return exactly one of these, unchanged, and nothing else: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in these steps comes back the same way, in place of the send.

# FINAL REPLY
When the messenger returned a delivery block, the final reply is the title line and the message, verbatim, and nothing else, as the conventions' Results say. Otherwise, unless reporting an error, end the run with one short line saying what happened, such as "Sent the morning reminder." or "Paused today; nothing sent." That line is for the Pushover case.

# ERROR HANDLING
If step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, never use `/ntm:notify`. End the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
