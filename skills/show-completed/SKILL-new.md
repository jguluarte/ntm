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
/ntm:show-completed [<span in words>] [<what else, in words>] [--notify]
```

The span is a run of days ending today, read the way a person would, such as
`today`, `last week` or `since Oct 1`. Without one, it's `last week`.

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

Find every task done in the span, and whatever else the words ask for. If the
task list can't be read, return `Show-completed FAILED: <what went wrong>`.

### 2. Return the result

In chat, tell the user what got done, and whatever else the words asked for, in
plain words, as the conventions' "Talking to the user about tasks" says.

For a job, return the span, with the scope after it when the words narrow it,
then a task line per task, oldest first, as the messenger agent's "What you're
given" says, with no estimate. A still open task planned before today gets
`(was <date>)`.

```
span: 2026-11-04 to 2026-11-10, the garage
done: Order storage boxes ([ABC-12](<url>))
canceled: none
duplicate: Buy shelf brackets ([ABC-14](<url>))
open: Clear the garage shelf ([ABC-9](<url>)) (was 2026-11-06)
```

`done:` lines always come, the others only when the words ask for them. A key
with no tasks is one line, such as `canceled: none`.

### 3. Send it, with --notify

Ask the messenger agent, with the result's `span:` and `done:` lines:

```
type: reminders.completed
job: show-completed
span: 2026-11-04 to 2026-11-10
done: Order storage boxes ([ABC-12](<url>))
```

Return what the messenger returned, as it came, in place of the result.
