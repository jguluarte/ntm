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

The type picks the facts and the message.

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
type: reminders.<type>
job: <type>
<the facts>
```

## Result

Return what the messenger returned, as it came.
