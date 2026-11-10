---
name: pause
description: >-
    The days when nothing gets planned automatically on the user's todo list.
    See or change them with the user in chat ("pause Friday", "unpause next
    week", "show my pauses"), or check whether days are paused. Run by the user,
    and loaded by ntm:plan.
---

# ntm:pause

A pause is a day, or a range of days, when nothing gets planned automatically. A
task the user plans on a paused day themselves still gets its reminders.

## Setup

Load `ntm-user:backend` to read the user's conventions, then read the user's
`Paused dates` database. The comments in its template,
`references/databases/paused-dates.md` in the newest installed `ntm`, say how
its pauses are written and kept. Follow them whenever you save it.

## Usage

```
Usage:
    /ntm:pause [<what to see or change>]

Inputs:
    <what to see or change>  in the user's words, such as "pause Friday",
                             "unpause next week" or "show my pauses"
```

With nothing after it, show the user their pauses and ask what they'd like to
change. Days can be written any way a person would (`2026-11-13`, `Nov 13`,
`Friday`).

## Seeing and changing pauses

### 1. Make the changes

Make the changes the user asks for, if any, and save the database without asking
them to approve: they said what they want. A new pause's reason is a few of the
user's words, or `paused` when they give none.

### 2. Show the pauses

Show the pauses that haven't ended, each date with its weekday so a wrong guess
is visible, such as:

> - 2026-11-13 (Friday): dentist
> - 2026-12-24 (Thursday) to 2027-01-02 (Saturday): holidays

### 3. Replan around a new pause

If a day the user just paused has tasks planned on it, those tasks need new
days: load `ntm:plan` and replan them with the user, as its With the user in
chat section says.

## Checking days

A day is paused when a pause in the database covers it, a range covering both
its first and last days. A check only reads the database.

## Result

The pauses, shown to the user. If the `Paused dates` database can't be read, say
what went wrong instead.
