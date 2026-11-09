---
name: today
description: >-
    Lists what's planned on the user's todo list, by default every open task
    planned for today or earlier, or whatever scope the user or a job describes
    ("what's on today", "what's planned this week"). Read-only. Run by jobs, or
    by the user.
---

# ntm:today

## Usage

```
/ntm:today [<scope in words>]
```

With nothing after it, list every open task with a planned date of today or
earlier. A planned date is all it takes: labels and status don't matter.

With words, list the open tasks planned within the span they describe. Narrow to
any scope they name, such as "the garage". Take whatever they describe; never
ask.

This skill only reads the todo list. It never changes a task.

## Setup

```
/ntm-user:backend find open items planned for today.
[<include scope from the user>]
```

If that fails, or `ntm-user:backend` answers `Backend CAN'T: <why>`, explain
what happened to the user. Run by a job, end with `Today FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it
decides what to tell the user and how. Write one task per line, oldest planned
date first; same date: started first, then by id. Each line is
`<id> <title> <url> <planned date> <status> <estimate or -> [label, label]`.
When the task's status is in the started class, add `(started)` after the
status. The brackets hold the task's labels, inherited ones included, and stay
empty (`[]`) when it has none.

Typed in chat, word each task as `ntm-user:backend` says to talk to the user
about tasks; the raw lines are for skills and jobs.

- With nothing after `/ntm:today`: `Planned by <today> (<count>):` then the
  tasks, or `Nothing planned for today.`
- With words: `Planned <first day> to <last day> (<count>):`, plus the scope
  when it's narrowed, then the tasks, or
  `Nothing planned <first day> to <last day>.`, plus the scope when it's
  narrowed.
