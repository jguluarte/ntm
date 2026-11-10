---
name: show-completed
description: >-
    Reports what the user got done on their task list over a span of days, and
    what's still open from it when asked; --notify sends what got done to them
    as a message. Run by a job, such as the weekly one, or by the user ("what
    did I finish last week", "what got done on my todo list this month").
---

# ntm:show-completed

## Setup

Load `ntm-user:backend` to read the user's conventions.

## Usage

```
/ntm:show-completed <span in words> [<what else, in words>] [--notify]
```

The span is a run of days ending today, today included: `today` is one day,
`last week` is seven, and `last month` is as many as last month had.
`since Oct 1` starts on that day. Without a span, ask the user for one.

The words can ask for more:

| For example                       | Adds                                                           |
| --------------------------------- | -------------------------------------------------------------- |
| and what's still open             | open tasks planned in the span, or in the range the words name |
| and what I canceled               | canceled tasks                                                 |
| and the duplicates                | duplicate tasks                                                |
| the garage, or the Office project | only the tasks that match, by project, parent, label or title  |

`--notify` also sends what got done to the user, as step 3 says.

## Steps

### 1. Find the tasks

Find every task done in the span, price watch buys included, and whatever else
the words ask for. If the task list can't be read, return
`Show-completed FAILED: <what went wrong>`.

### 2. Return the result

Return plain text, one task per line as `<id> <title> <url> <date>`: the day it
closed, or for a still open task, its planned date.

| Line                                          | Holds                                                                                     |
| --------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `<first day> to <last day>`                   | the span, then the scope when the words narrow it                                         |
| `Done (<count>):`                             | the done tasks, oldest first, a sub-task indented under its parent when that's listed too |
| `Canceled (<count>):`, `Duplicate (<count>):` | when asked for, written like Done                                                         |
| `Still open (<count>):`                       | when asked for                                                                            |

A section with no tasks is one line, such as `Done: none`.

### 3. Send it, with --notify

Ask the messenger agent, with the span and one `done:` line per done task,
written like the one below, or `done: none`:

```
type: reminders.completed
job: show-completed
span: 2026-11-04 to 2026-11-10
done: Order storage boxes ([ABC-12](<url>))
```

Return what the messenger returned, as it came, in place of the result.
