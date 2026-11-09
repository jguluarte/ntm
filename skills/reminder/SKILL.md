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
/ntm:reminder --type <morning|afternoon|evening|week>
```

## Setup

Load `ntm-user:backend` to read the user's conventions.

## The facts

| Type      | Lines                                                                       |
| --------- | --------------------------------------------------------------------------- |
| morning   | `today:` per open task planned today or earlier                             |
| afternoon | `open:` per open task planned today                                         |
| evening   | `done:` per task done today, then `open:` per open task planned today       |
| week      | the `done:`, `open:`, `planned:` and `weekly message:` lines the job handed |

A line with no tasks is written once, as `none` (`today: none`).

## Steps

### 1. Gather

For week, take the job's lines as they came and go to step 2.

Find the type's tasks. If the todo list can't be read, stop with
`Reminder FAILED: <why>`.

Write each task as a task line, as the messenger agent's "What you're given"
says, with no estimate. Add `(was <date>)` on a morning task planned before
today, and `(started)` on an open task when work on it has begun.

### 2. Hand over

Ask the messenger agent:

```
kind: <type>
job: <type>
<the facts>
```

## Result

Return what the messenger returned, as it came.
