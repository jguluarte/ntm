---
name: pause
description: >-
    The user's pauses, the days when nothing on their task list gets planned
    automatically. Pauses or unpauses days, or shows the pauses, with the user
    in chat ("pause Friday", "pause next week", "unpause the 12th", "show my
    pauses").
---

# ntm:pause

A pause is a day, or a span of days, when nothing gets planned automatically.

## Usage

```
/ntm:pause [<what to change, in words>]
```

With nothing after it, take off any pauses that have ended, save if that changed
the list, and show the pauses. With words, change the pauses as they say, then
show them.

## Setup

Load `ntm-user:backend` to read the user's conventions. Read the Paused dates
part of `%Paused-dates`. Today is the date in the timezone under About you in
`%Settings`.

## Keeping `%Paused-dates`

The Paused dates part holds one list item per pause, in date order:

| A pause                 | Its list item                |
| ----------------------- | ---------------------------- |
| One day                 | `- 2026-11-27`               |
| A span                  | `- 2026-12-21 to 2026-12-31` |
| With a reason they gave | `- 2026-11-26: Thanksgiving` |
| No pauses               | `None.`                      |

A span includes both its ends. A pause comes off the list once it has ended.

## Changing pauses

### 1. Work out the days

Read the user's words as a person would: "Friday" is the coming one.

### 2. Change the list

Add, shorten, split or remove pauses as they say. Their words are the go-ahead;
don't ask for approval.

### 3. Save

Save the list.

### 4. Planned work on paused days

Look at what's already planned on the newly paused days, and handle it as fits.
For one day, saying what's planned and asking if they want to change it may be
enough. For several days, ask if they want those dates cleared too; they may
want to see what was planned. Be flexible.

## Result

Show the user the pauses as they stand, each date with its weekday, so a wrong
guess about a day is easy to spot.
