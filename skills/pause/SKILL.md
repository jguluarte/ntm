---
name: pause
description: >-
    Pauses for the user's todo list, the days when nothing gets planned
    automatically. See or change them in chat ("pause Friday", "unpause next
    week", "show my pauses"), or check whether days are paused.
---

# ntm:pause

A pause is a day or a date range when nothing new gets planned automatically.
Work the user dated themselves for a paused day stays; the messenger agent
decides that day's messages from the user's Message rules.

"Pause Friday" or "unpause next week" means adding or ending a pause. Outside a
chat with the user (`ntm:plan`, the messenger agent), callers use only `--check`
and read its answer as whether each day is paused.

## Setup

Load `ntm-user:backend` to read the user's conventions.

## Where pauses live

The `Paused dates` database opens with the line
`The days when nothing gets planned automatically.` Under its `## Paused dates`
heading it holds one line per pause, sorted by start date. Each line is bare,
with no list marker: `YYYY-MM-DD: <why>` for a single day, or
`YYYY-MM-DD to YYYY-MM-DD: <why>` for a range; the single line `None.` when
there are none.

A missing database, or one with no pause lines, means there are no pauses. If
the read itself fails, stop and return `Pause FAILED: <why>`, so a caller never
takes an unreadable database for "not paused".

A line whose dates have no year is invalid. Whenever the database is read, for
any reason, ignore those lines and remove them on the next save.

To save, write the whole content, only the lines under `## Paused dates` changed
(`None.` if nothing is left); when the database is missing, the content is the
opening line, the `## Paused dates` heading and the lines. Pauses never overlap:
before saving, merge any that overlap into one line covering all their days,
with their reasons joined by `; ` in start-date order.

## Usage

```
/ntm:pause
/ntm:pause <words>
/ntm:pause --check [<day>] [--until <day>]
```

- Bare: ask the user whether they want to see the pause schedule or change it,
  then do that with them.
- Words ("Friday", "next week", "remove the 12th", "show my pauses"): follow
  them; see or change the pauses with the user.
- `--check`: are these days paused? It checks the first day through the
  `--until` day, both included. The first day defaults to today, and the
  `--until` day defaults to the first. So `--check` alone checks today,
  `--check --until 2026-10-15` checks today through the 15th, and
  `--check 2026-10-14 --until 2026-10-15` checks just those two days.

Dates passed to `--check` can be in any form a person would write (`2026-10-15`,
`Oct 15`, `Friday`); interpret them as the Dates section says. The output always
uses `YYYY-MM-DD`.

## Dates

A range covers both its start and end days. A weekday name means the next one,
today included when today is that day (the example below was typed on a
Thursday); "next <weekday>" means that weekday of next week (weeks start on
Monday); a date without a year is the next one. Show the resolved date in the
reply (`Paused 2026-11-13 (Friday).`) so a wrong guess is visible; there is no
confirmation round-trip before saving.

## With `--check`

1. Read the database. If any pause ended before today, or any line is invalid,
   remove those lines and save.
2. Return one line per day from the first day to the `--until` day, in order,
   and nothing else, as Result says.

## Bare, or with words

If a job calls this without `--check`, change nothing and say this needs a chat
with the user.

1. Read the database. Drop every pause that ended before today and every invalid
   line, and tell the user which ones went.
2. Show the user the remaining pauses, then make the changes they ask for, if
   any, without an approval round-trip: they said what they want. When a day
   they pause holds planned work, clear those dates and load `ntm:plan` to
   replan the rest of the week with them, in chat. A new pause gets a short
   reason in the user's words, or `paused` if they give none. To end a range
   early, set its end to the last paused day; if that's before today (as with
   ending it today), remove the line.
3. If anything changed, step 1 included, save and show the user the saved list.

## Result

A save `--check` makes while tidying ended or invalid lines doesn't change the
answer; if it fails, answer anyway.

Plain text for whoever called the skill.

- With `--check`: one line per day, in order, and nothing else:
  `YYYY-MM-DD: true` when that day is paused, or `YYYY-MM-DD: false` when it
  isn't, so it can be planned automatically.
- Bare, or with words: the pauses as saved, shown to the user.
- `Pause FAILED: <why>` when the database can't be read. A missing database
  isn't a failure: it means there are no pauses.
