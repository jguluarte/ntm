---
name: recap
description: Reports what the user got done on their nudge board over a span of time they or a job describes ("what did I finish last week", "what got done this month"), and, when asked, what's still open from it. Run by jobs, or by the user.
---

# nudge:recap

## Usage

```
/nudge:recap <what to look at>
```

What to look at is a description in plain words:

- **Span** (required): such as "the last 7 days", "this month" or "since Oct 1".
- **Open tickets** (optional): ask for them to add a Still open section.
- **Canceled or duplicate tickets** (optional): ask for them to add their own sections.

The description can also narrow the scope, such as "the garage" or "the Office project". Take whatever scope it describes; never ask for one.

Without a span, ask the user what span they want. Never assume one.

## Setup

1. Load `nudge:board`.
2. Compute `TODAY` as the board rules' Dates section says, and work out the span, which ends now.
3. Fetch with the adapter's `fetch closed`: done tickets, adding canceled and duplicate ones only when the request asks for them. Add the board rules' Scheduling fetch (`fetch open`), keeping excluded tickets, only when it asks for open tickets.
4. Keep the tickets completed in the span, in the config's `timezone`.
5. When the description narrows the scope, keep only the tickets that match it, by project, parent, label or title.

If any step fails, stop and return `Recap FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write each ticket as `<id> <title> <url>`, followed by its date.

- `<first day> to <last day>`, plus the scope when it's narrowed.
- `Done (<count>):` the tickets completed in the span, oldest first, with sub-tickets indented under their parent when it's listed too; or `Done: none`.
- Canceled and duplicate tickets, when asked for, in their own `Canceled (<count>):` and `Duplicate (<count>):` sections, written the same way.
- `Still open (<count>):` when asked for: open tickets planned in the span.
