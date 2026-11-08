---
name: show-completed
description: >-
    Reports what the user got done on their todo list over a span of time they
    or a job describes ("what did I finish last week", "what got done this
    month"), and, when asked, what's still open from it; --notify sends it as a
    message in the user's style. Run by the evening reminder, by ntm:plan, by a
    job, or by the user.
---

# ntm:show-completed

## Usage

```
/ntm:show-completed <span in words> [--notify]
```

What to look at is a description in plain words:

- **Span** (required): a number of days ending today, today included. "Today" is
  1; "the last 7 days" is 7; "last week" is 7; "last month" is as many days as
  the previous calendar month of that year had (31 at the start of November; 28
  or 29 at the start of March, by that year's February); "since Oct 1" counts
  from that day. No calendar weeks, no overlap logic.
- **Open tasks** (optional): ask for them ("and what's still open") to add a
  Still open section.
- **Canceled or duplicate tasks** (optional): ask for them to add their own
  sections.

The description can also narrow the scope, such as "the garage" or "the Office
project". Take whatever scope it describes; never ask for one.

Without a span, ask the user what span they want. Never assume one.

`--notify`: also send the result as a message, through the messenger agent (see
Notify below). `--notify` starts with
`/ntm:ready-check --notify-failure show-completed`, before Setup;
`Ready-check FAILED` ends the run with what it returned.

## Setup

1. Load `ntm:conventions`.
2. Work out the span as Usage says: it ends today.
3. Fetch with the guide's `fetch closed`: done tasks, adding canceled and
   duplicate ones only when the request asks for them. Add the guide's
   `fetch open`, keeping excluded tasks, only when it asks for open tasks.
4. Keep the tasks completed in the span. Done tasks of any kind count, price
   watch buys included.
5. When the description narrows the scope, keep only the tasks that match it, by
   project, parent, label or title.

If any step fails, stop and return `Show-completed FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it
decides what to tell the user and how. Write each task as
`<id> <title> <url> <date>`, the date on the same line: the completion date for
Done, the planned date for Still open.

- `<first day> to <last day>`, plus the scope when it's narrowed.
- `Done (<count>):` the tasks completed in the span, oldest first, with
  sub-tasks indented under their parent when it's listed too; or `Done: none`.
- Canceled and duplicate tasks, when asked for, in their own
  `Canceled (<count>):` and `Duplicate (<count>):` sections, written the same
  way.
- `Still open (<count>):` when asked for: open tasks planned in the span, or in
  the range the request names for them ("planned today or earlier").

Typed in chat, present the result as the conventions' "Talking to the user about
tasks" says (natural words, the id in parentheses); the raw lines are for skills
and jobs.

## Notify

With `--notify`, after the result, ask the messenger agent, with the reminder
`completed`, the job `show-completed`, a `span:` line (the result's first line)
and one `done:` line per Done task (`done: <id> <title> <url>`), or
`done: none`:

```
reminder: completed
job: show-completed
span: 2026-10-31 to 2026-11-06
done: ABC-12 Order storage boxes <url>
```

When the messenger agent isn't available in this session, do what the
conventions' "Chat, jobs and agents" says: read `agents/messenger.md` from the
installed plugin and follow it yourself. It returns `Sent: <title>`, a delivery
block, or a `… FAILED` line. A delivery block is the final reply, verbatim, and
nothing else; otherwise one short line on what happened, then any lines the
messenger returned after `Sent:` (the list the push couldn't carry). A
`… FAILED` line: never use `/ntm:notify`; end with the error stated plainly.
