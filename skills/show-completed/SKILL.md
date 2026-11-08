---
name: show-completed
description: >-
    Reports what the user got done on their todo list over a span of time they
    or a job describes ("what did I finish last week", "what got done this
    month"), and, when asked, what's still open from it; --notify sends it as a
    message in the user's style. Run by the evening reminder, by the "Completed
    this week" job, or by the user.
---

# ntm:show-completed

```
/ntm:show-completed <span in words> [--notify]
```

## The request

The request is in plain words and must give a span. Without one, ask the user
for it; never assume one. It can also ask for:

- what's still open ("and what's still open")
- canceled or duplicate tasks
- a narrower scope, such as "the garage" or "the Office project"; take whatever
  scope it describes, and never ask for one

A span is a number of days ending today, today included. "Today" is 1 day; "the
last 7 days" and "last week" are 7; "since Oct 1" counts from that day. "Last
month" is as many days as the previous calendar month had: 31 at the start of
November, and 28 or 29 at the start of March, by that year's February. No
calendar weeks, no overlap logic.

`--notify` also sends the result as a message (see Notify). Name the job from
the span: `Completed this week` for a week (any 7-day span),
`Completed this month` for a month, else `Completed`.

## Setup

With `--notify`, start with:

```
/ntm:ready-check --notify-failure "<job name>"
```

`Ready-check FAILED` ends the run with what it returned. Then:

1. Load `ntm:conventions`, and compute `TODAY` as its Dates section says.
2. Fetch done tasks with the guide's `fetch closed`, adding canceled and
   duplicate ones only when asked for. When asked for open tasks, also run the
   guide's `fetch open`, keeping excluded tasks.
3. Keep the tasks completed in the span, in the user's timezone. Done tasks of
   any kind count, price watch buys included.
4. When the request narrows the scope, keep only the tasks that match it, by
   project, parent, label or title.

If a step fails, stop and return `Show-completed FAILED: <what failed>`.

## Result

Return plain text; the caller decides what to tell the user. Write each task as
`<id> <title> <url> <date>`: the completion date for Done and the other closed
sections, the planned date for Still open.

- `<first day> to <last day>`, plus the scope when it's narrowed
- `Done (<count>):` tasks completed in the span, oldest first, sub-tasks
  indented under their parent when it's listed too; or `Done: none`
- `Canceled (<count>):` and `Duplicate (<count>):` when asked for
- `Still open (<count>):` when asked for: open tasks planned in the span, or in
  the range the request names, such as "planned today or earlier"

The raw lines are for skills and jobs. Typed in chat, present the result as the
conventions' "Talking to the user about tasks" says.

## Notify

With `--notify`, after the result, ask the messenger agent. Hand it
`reminder: completed`, `job:` with the job name, `span:` with the result's first
line, and one `done: <id> <title> <url>` line per Done task, sub-tasks included,
or `done: none`:

```
reminder: completed
job: Completed this week
span: 2026-10-31 to 2026-11-06
done: ABC-12 Order storage boxes <url>
```

The conventions' "Chat, jobs and agents" covers the `wording:` line, a
`Messenger NEEDS: …` reply, and a messenger that isn't available. The messenger
returns one of:

- **A delivery block:** that is the final reply, verbatim, and nothing else.
- **`Sent: <title>`:** end with one short line on what happened, then any lines
  the messenger returned after `Sent:` (the list the push couldn't carry).
- **A `… FAILED` line:** never use `/ntm:notify`; end with the error stated
  plainly.
