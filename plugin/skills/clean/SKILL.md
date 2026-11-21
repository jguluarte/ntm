---
name: clean
user-invocable: false
description: >-
    Clears dates on previously planned tasks that didn't finish, removes pause
    dates that have since passed, and takes closed tasks out of their projects
    when your task list app counts them against its limits. Your weekly setup
    runs it for you. It reports back how much it changed.
---

# ntm:clean

Cleans up stale information in the backend.

## Usage

```
/ntm:clean
```

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

## Clean

Find all non-closed tasks which have a planned date in the past. For each, add
that stale date to its `Planned date history` comment, then clear the date.

Read the Paused dates part of `%Paused-dates`, and find the paused dates that
have passed: a day, or a range's last day, before today. Take those off the
list. With none left, the part says `None.`

Then do the cleanup `ntm-user:backend` lists, if any.

## Result

For a job, return one line of counts, with each of the backend's cleanup counts
last:
`Cleaned <today>: cleared <n> planned dates, removed <n> paused dates, <backend's counts>`

Leave out a count of none. When every count is none, return `Nothing to clean.`;
when the task list can't be read, `Clean FAILED: <what went wrong>`. In chat,
tell the user the same in plain words.
