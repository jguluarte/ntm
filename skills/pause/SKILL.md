---
name: pause
description: >-
    The user's pauses, the days that get nothing new planned on their task list
    automatically. Pauses or unpauses days, or shows the pauses, with the user
    in chat ("pause Friday", "pause next week", "unpause the 12th", "show my
    pauses").
---

# ntm:pause

A pause is a day, or a range of days, that gets nothing new planned
automatically.

## Usage

```
/ntm:pause [<what to change, in words>]
```

With nothing after it, take off any pauses that have ended, save if that changed
the list, and show the pauses. With words, change the pauses as they say, then
show them.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

Read the Paused dates part of `%Paused-dates`. Today is the date in the timezone
under About you in `%Settings`.

## Keeping `%Paused-dates`

The Paused dates part holds one list item per pause, in date order:

| A pause                 | Its list item                |
| ----------------------- | ---------------------------- |
| One day                 | `- 2026-11-27`               |
| A range                 | `- 2026-12-21 to 2026-12-31` |
| With a reason they gave | `- 2026-11-26: Thanksgiving` |
| No pauses               | `None.`, or an empty part    |

A range includes both its ends. A pause comes off the list once it has ended.

## Changing pauses

### 1. Work out the days

Read the user's words as a person would: "Friday" is the coming one.

### 2. Change the list

Add, shorten, split or remove pauses as they say. Their words are the go-ahead;
don't ask for approval.

### 3. Save

Save the list.

### 4. Planned work on paused days

Look at what's already planned on the newly paused days, and handle it as fits
the case. For one day, saying what's planned and asking if they want to change
it may be enough. For several days, ask if they want those dates cleared too,
and show what was planned if they'd like to see it. Be flexible.

## Result

Show the user their pauses, each date with its day of the week.
