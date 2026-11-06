---
name: completed
description: Reports what the user got done on their ntm board over a span of time they or a job describes ("what did I finish last week", "what got done this month"), and, when asked, what's still open from it; --notify sends it as a message in the user's style. Run by the planner agent, by the "Completed this week" job, or by the user.
---

# ntm:completed

## Usage

```
/ntm:completed <span in words> [--notify]
```

What to look at is a description in plain words:

- **Span** (required): such as "the last 7 days", "this month" or "since Oct 1".
- **Open tickets** (optional): ask for them ("and what's still open") to add a Still open section.
- **Canceled or duplicate tickets** (optional): ask for them to add their own sections.

The description can also narrow the scope, such as "the garage" or "the Office project". Take whatever scope it describes; never ask for one.

Without a span, ask the user what span they want. Never assume one.

`--notify`: also send the result as a message, through the messenger agent (see Notify below). The "Completed this week" and "Completed this month" jobs run `/ntm:completed the last 7 days --notify` and `/ntm:completed last month --notify`. In a job, `--notify` starts with the ready check: run `/ntm:ready-check --notify-failure --job "<job>"` before Setup; `Ready-check FAILED` ends the run with its line.

## Setup

1. Load `ntm:conventions`.
2. Compute `TODAY` as the conventions' Dates section says, and work out the span, which ends now.
3. Fetch with the guide's `fetch closed`: done tickets, adding canceled and duplicate ones only when the request asks for them. Add the guide's `fetch open`, keeping excluded tickets, only when it asks for open tickets.
4. Keep the tickets completed in the span, in the timezone from About you in your settings. Done tickets of any kind count, price watch buys included.
5. When the description narrows the scope, keep only the tickets that match it, by project, parent, label or title.

If any step fails, stop and return `Completed FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write each ticket as `<id> <title> <url>`, followed by its date.

- `<first day> to <last day>`, plus the scope when it's narrowed.
- `Done (<count>):` the tickets completed in the span, oldest first, with sub-tickets indented under their parent when it's listed too; or `Done: none`.
- Canceled and duplicate tickets, when asked for, in their own `Canceled (<count>):` and `Duplicate (<count>):` sections, written the same way.
- `Still open (<count>):` when asked for: open tickets planned in the span.

Typed in chat, present the result as the conventions' "Talking to the user about tickets" says (natural words, the id in parentheses); the raw lines are for skills and jobs.

## Notify

With `--notify`, after the result, ask the messenger agent, with the beat `completed`, the job name (`Completed this week` for a span of a week, `Completed this month` for a month, else `Completed`) and one `done:` line per Done ticket (`done: <id> <title> <url>`), or `done: none`:

```
beat: completed
job: Completed this week
done: ABC-12 Order storage boxes <url>
```

When the messenger agent isn't available in this session, read `agents/messenger.md` from the installed plugin (`find ~/.claude/plugins -path '*/ntm/agents/messenger.md'`) and do what it says yourself. It returns `Sent: <title>`, a delivery block, or a `… FAILED` line. A delivery block is the final reply, verbatim, and nothing else; otherwise one short line on what happened. A `… FAILED` line: never use `/ntm:notify`; end with the error stated plainly.
