---
name: reminder
description: >-
    Gathers the facts for one of the user's reminders, morning, afternoon,
    evening or week, and hands them to the messenger agent, which decides
    whether and how the message goes. Run by a job, as /ntm:reminder --type
    morning, afternoon, evening or week.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening|week> --job <key>
```

`--job` is the key of the job that ran it, such as `morning-reminder` or `week`.

## The facts

| Type      | Lines                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------- |
| morning   | `today:` per open task planned today or earlier                                                           |
| afternoon | `open:` per open task planned today or earlier                                                            |
| evening   | `done:` per task done today, then `open:` per open task planned today or earlier                          |
| week      | `done:` per Done task, `open:` per Still open task, then the job's `planned:` and `weekly message:` lines |

A key with no tasks gets the single line `<key>: none`.

## Steps

### 1. Gather

For morning, afternoon and evening, load `ntm-user:backend` to read the user's
conventions, then find the type's tasks. If the todo list can't be read, stop
with `Reminder FAILED: <why>`.

For week, the tasks are in the show-completed result the job handed: its Done
and Still open sections. When it handed `Show-completed FAILED`, the lines are
`done: unavailable` and `open: none`; when it handed no show-completed result,
leave out `done:` and `open:`. The `planned:` lines come from what plan
returned, as they are.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate. Add `(was <date>)` on a task planned before today, and
`(started)` on an open task when work on it has begun.

### 2. Hand over

Ask the messenger agent:

```
reminder: <type>
job: <the --job key>
<the facts>
```

When the job gives a Pushover app token, add `app token: <token>` as the last
line.

## Result

Return what the messenger returned, as it came.
