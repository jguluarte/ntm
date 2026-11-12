---
name: reminder
description: >-
    Sends one of the user's daily reminders about their todo list, morning,
    afternoon or evening: checks that ntm can run, then hands the reminder to
    the messenger agent, which follows the user's message rule for it, writes
    the message in the user's style and sends it. Run by a job, as /ntm:reminder
    --type morning, afternoon or evening.
---

# ntm:reminder

## Usage

```
/ntm:reminder --type <morning|afternoon|evening>
```

The type picks the user's message rule, which says what the message holds.

## Setup

Load `ntm-user:backend` and their `%Message-rules`. Then run `/ntm:ready-check`.
If it fails, end the run with its result line.

## The message

Hand the messenger agent `type: reminders.<type>`, such as `reminders.morning`.
It sends the message for that type, as the user's message rules say.

## Result

Return what the messenger returned, as it came.
