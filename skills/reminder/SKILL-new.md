---
name: reminder
description: >-
    Sends one of the user's daily reminders, morning, afternoon or evening:
    gathers the day's tasks from their todo list and hands them to the messenger
    agent, which writes the message in the user's style and sends it. Run by a
    job, as /ntm:reminder --type morning, afternoon or evening.
---

# ntm:reminder

The user's daily reminders. This skill gathers the facts its type needs from the
task list as it stands, and the messenger agent turns them into the message.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
```

The morning job hands over the `today:` lines `/ntm:plan --auto day` returned.

## Steps

### 1. Gather the facts

When the job hands over `today:` lines, they're the facts, as written,
`(was <date>)` and `(started)` included.

Otherwise, find the type's tasks. If the task list can't be read, return
`Reminder FAILED: <why>`.

| Type      | Fact     | One line per                |
| --------- | -------- | --------------------------- |
| morning   | `today:` | open task planned for today |
| afternoon | `open:`  | open task planned for today |
| evening   | `done:`  | task done today             |
| evening   | `open:`  | open task planned for today |

Write each task as a task line, as the messenger agent's "What you're given"
says, without its estimate. A fact with no tasks is the single line
`<fact>: none`, such as `open: none`.

### 2. Hand them to the messenger

Ask the messenger agent:

```
type: reminders.<type>
job: <type>
<the facts>
```

## Result

Return what the messenger returned, as it came.
