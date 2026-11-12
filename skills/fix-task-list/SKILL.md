---
name: fix-task-list
description: |-
    Tidies the user's task list by:
    - Clearing stale planned dates
    - Removing paused dates that have passed from `%Paused-dates`

    This is run via scheduled job. It reports back the things it changed.
---

# ntm:fix-task-list

Cleans up stale information in the backend.

## Usage

```
/ntm:fix-task-list
```

## Fix

Load `ntm-user:backend`, and then find all non-closed tasks which have a planned
date in the past. Clear the date on all of those tasks.

Read the Paused dates part of `%Paused-dates`, and find the paused dates that
have passed: a day, or a range's last day, before today. Take those off the
list. With none left, the part says `None.`

## Result

For a job, return these lines, with one `Cleared` line per date cleared and one
`Removed` line per paused date removed:

```
Fixed <today>:
Cleared <id> <title> <url> (was <date>)
Removed paused date <as the list had it>
```

When there were none, return `Nothing to fix.`; when the task list can't be
read, `Fix-task-list FAILED: <what went wrong>`. In chat, tell the user the same
in plain words.
