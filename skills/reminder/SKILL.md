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

`--job` is the key of the job that ran it, such as `morning-reminder` or `plan`.

## The facts

| Type      | Lines                                                                            |
| --------- | -------------------------------------------------------------------------------- |
| morning   | the `today:` lines the job handed                                                |
| afternoon | `open:` per open task planned today or earlier                                   |
| evening   | `done:` per task done today, then `open:` per open task planned today or earlier |
| week      | the `done:`, `open:`, `planned:` and `weekly message:` lines the job handed      |

A key with no tasks gets the single line `<key>: none`.

## Steps

### 1. Gather, for afternoon and evening

Load `ntm-user:backend` to read the user's conventions, then find the type's
tasks. If the todo list can't be read, stop with `Reminder FAILED: <why>`.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate. Add `(was <date>)` on a task planned before today, and
`(started)` on an open task when work on it has begun.

### 2. Hand over

Ask the messenger agent:

```
kind: <type>
job: <the --job key>
<the facts>
```

## Result

Return what the messenger returned, as it came.
