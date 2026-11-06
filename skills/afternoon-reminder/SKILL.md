---
name: afternoon-reminder
description: The afternoon reminder for the user's ntm board. Lists what's still open for today, started work marked, and sends a tap on the shoulder in the user's style; never escalates. Run by the "Afternoon reminder" job, or by hand ("run the afternoon reminder now").
---

# ntm:afternoon-reminder

Afternoon reminder for the user's board. Each step names a skill: load it and follow it. Skills return text; you decide what reaches the user. Steps 2 and 3 hand their numbered steps to an agent as text when it's loaded. When it isn't, do the same steps yourself with the same skills. Say nothing to the user about it either way.

# 1: Ready check
Run `/ntm:ready-check --notify --job "Afternoon reminder"`.
**If it returns `Ready-check FAILED`, STOP: end the run with what it returned and nothing more.**

# 2: What's still open
Hand the planner agent these steps, or do them yourself:

1. Load `ntm:conventions`, `ntm:todo-list` and `ntm:pause`. Compute `TODAY` as the conventions' Dates section says.
2. Run `/ntm:todo-list` and return its result.
3. When it's `Nothing planned for today.`, also run `/ntm:pause --check` and return its line for today.

Read what comes back:
- Anything listed: remind about it, whatever its labels or status, even on a paused day. The user dated it themselves, so it should just work. The conventions' exclusions are for picking work, not for reminders about work they dated. Each line ends with the ticket's labels in brackets; leave out any ticket whose brackets hold the `deadline` label (its real name from Labels in your settings) and whose planned date is before today.
- `Nothing planned for today.` and the pause line ends `true`: today is paused. STOP and send nothing.
- `Nothing planned for today.` otherwise: they already handled today; step 3 sends quick props.
- Any `… FAILED` line: ERROR HANDLING.

# 3: Send the afternoon message
Hand the messenger agent these steps, with the beat, the job name and the facts, one per line:

```
afternoon: Afternoon reminder
open: ABC-9 Clear the garage shelf (~1 h) <url> (started)
```

One `open:` line per ticket still open, `<id> <title> (~<time>) <url>`, or the single line `nothing open`. After the url: `(was <date>, carried <n> days)` when its planned date is before `TODAY` (`n` being `TODAY` minus that date in calendar days; `carried 1 day` when it's one), then `(started)` when todo-list marked it so. `(~<time>)` is your rough guess from the title. The facts are everything the message may say; add none.

The messenger's steps, or do them yourself:

1. Load `ntm:conventions`, `ntm:style-message` and `ntm:notify`.
2. Write one or two sentences for the afternoon: a tap on the shoulder about what's still open, naming a `(started)` ticket as started. With `nothing open`, quick props and nothing more.
3. Run them through `/ntm:style-message --for afternoon "<tone>" <sentences>`, with a tone that opens with the job name (`Afternoon reminder; …`), then what's still open and which of it is started, or that nothing is open. The afternoon never escalates: whatever the history says, this beat gets the style's first level, and `style-message` keeps it there. When the style's What gets you to read names a scoreboard (load `ntm-user:style` and read its What gets you to read), load `ntm:show-completed`, run `/ntm:show-completed this week`, and put its Done count in the tone. Style-message returns the message with `Title: …` as its last line (with no style configured, your sentences as given plus that line).
4. Under the styled lines, what's still open, one line each: the ticket as a linked ticket, exactly as the conventions' "Talking to the user about tickets" says, with its `(~<time>)`, its `(was <date>, carried <n> days)` when given, and `(started)` as given, in that order. With `nothing open`, no list.
5. Send with `/ntm:notify --job "Afternoon reminder" --title "<the words after Title:>" --message "<everything above the Title line, with the list under it>"`.
6. Return exactly one of these, unchanged, and nothing else: `Sent: <title>`; the delivery block starting `NOTIFY VIA FINAL REPLY`, verbatim; `Notify FAILED: <why>`. A `<Skill> FAILED: …` line from a skill in these steps comes back the same way, in place of the send.

# FINAL REPLY
When the messenger returned a delivery block, the final reply is the title line and the message, verbatim, and nothing else, as the conventions' Results say. Otherwise, unless reporting an error, end the run with one short line saying what happened, such as "Sent the afternoon reminder." or "Paused today; nothing sent." That line is for the Pushover case.

# ERROR HANDLING
If step 1 fails, end with what the ready check returned, and nothing more; that is what reaches the user. For any later error, including a `… FAILED` line from the planner or the messenger, never use `/ntm:notify`. End the run with the error stated plainly in your final reply; the scheduled task's own completion push carries it.
