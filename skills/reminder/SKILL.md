---
name: reminder
description: >-
    Sends one of the user's reminders, morning, afternoon or evening, the week
    in review and ahead, or what got done over a span: gets the tasks from
    ntm-user:backend, sends nothing when there's nothing to remind about, and
    otherwise hands them to the messenger agent, which writes the message in the
    user's style and sends it. Run by a job, as /ntm:reminder --type morning,
    afternoon, evening, week or completed.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
/ntm:reminder --type <week|completed> --span <span in words>
```

The type picks the facts and the message. It is also the job's key, which the
messenger gets as `job:`. With `--type morning`, read `references/morning.md`
first; with `--type week`, `references/week.md`; with `--type completed`,
`references/completed.md`. No other type loads them.

`--span`: the days a week or completed reminder looks back on, ending today,
today included: "the last 7 days" is 7; "since Oct 1" counts from that day.
Without one, return `Reminder FAILED: no --span given`.

## The facts

Ask `ntm-user:backend` for today's open items. For the evening, also ask it for
the items done today. If a request fails, or `ntm-user:backend` answers
`Backend CAN'T: <why>`, stop and return `Reminder FAILED: <what failed>`.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate. On an open task, add `(was <date>)` when its planned
date is before today, and `(started)` when its status is in the started class.
Remind about every open task, whatever its labels or status, even on a paused
day: the user dated it.

- afternoon: one `open:` line per open task, or `open: none`.
- evening: one `done:` line per task done today, or `done: none`; then one
  `open:` line per open task, or `open: none`.

## When to send nothing

Send nothing, and end the run with the line given, when:

- morning or afternoon, no open tasks, and today is paused:
  `Nothing sent: today is paused.`
- evening, nothing done and nothing open, a day off:
  `Nothing sent: nothing done or open today.`

Otherwise send: an empty morning or afternoon still gets its message.

Check the pause only when a morning or afternoon has no open tasks: ask
`ntm-user:backend` to read the `Paused dates` database. Today is paused when a
line's day or range covers it; a missing database means no pauses. If the read
fails, return `Reminder FAILED: <why>`; an unreadable database never counts as
not paused.

## The message

Ask the messenger agent, with the type, the job's key and the facts:

```
reminder: <type>
job: <type>
<the facts>
```

When the messenger agent isn't available in this session, read
`agents/messenger.md` from the newest installed `ntm` and follow it yourself.

## Result

Return what the messenger returned, as it came: `Sent: <title>` (with its
`List:` lines when the push couldn't carry the list), the delivery block, or its
`… FAILED` or `Messenger NEEDS` line.
