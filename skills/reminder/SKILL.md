---
name: reminder
description: >-
    Sends one of the user's daily reminders, morning, afternoon or evening:
    finds the day's tasks on the todo list, sends nothing when there's nothing
    to remind about, and otherwise hands them to the messenger agent, which
    writes the message in the user's style and sends it. Run by a job, as
    /ntm:reminder --type morning, afternoon or evening.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
```

The type picks the facts and the message. It is also the job's key, which the
messenger gets as `job:`.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## The facts

Find the open tasks planned for today and, for the evening, the tasks done
today. Remind about every open task, whatever its labels, even on a paused day:
the user dated it. If the todo list can't be read, stop and end with
`Reminder FAILED: <what went wrong>`.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate, and `(started)` when work on it has begun.

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

Check the pause only when a morning or afternoon has no open tasks: run
`/ntm:pause --check`. Today is paused when its line for today ends `true`. If it
fails, end with `Reminder FAILED: <what went wrong>`; a failed check never
counts as not paused.

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
