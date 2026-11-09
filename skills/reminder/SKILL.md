---
name: reminder
description: >-
    Sends one of the user's reminders, morning, afternoon or evening, the week
    in review and ahead, or what got done over a span: finds the tasks on the
    todo list, sends nothing when there's nothing to remind about, and otherwise
    hands them to the messenger agent, which writes the message in the user's
    style and sends it. Run by a job, as /ntm:reminder --type morning,
    afternoon, evening, week or completed.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
/ntm:reminder --type <week|completed> --span <span in words>
```

The type picks the facts and the message. With `--type week`, read
`references/week.md` first; with `--type completed`, `references/completed.md`.
No other type loads them.

`--span`: the days a week or completed reminder looks back on, ending today,
today included: "the last 7 days" is 7; "since Oct 1" counts from that day.
Without one, end with `Reminder FAILED: no --span given`.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## The facts

Find all open and completed (non-cancelled) tasks with today's date. If the task
list can't be read, terminate with `Reminder FAILED: <error msg>`.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate, and `(started)` on an open task when work on it has
begun.

- morning: one `today:` line per open task, or `today: none`.
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

To check the pause, run `/ntm:pause --check`; today is paused when its line for
today ends `true`. If it fails, end with `Reminder FAILED: <what went wrong>`; a
failed check never counts as not paused.

## The message

Ask the messenger agent:

```
reminder: <type>
job: <type>
<the facts>
```

When the messenger agent isn't available in this session, read
`agents/messenger.md` from the newest installed `ntm` and follow it yourself.

## Result

Return what the messenger returned, as it came.
