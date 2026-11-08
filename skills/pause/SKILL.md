---
name: pause
description: >-
    Pauses for the user's todo list, the days when nothing gets planned
    automatically. See or change them in chat ("pause Friday", "unpause next
    week", "show my pauses"), or check whether days are paused.
---

# ntm:pause

A pause is a day or a date range when nothing new gets planned automatically.
Work the user dated themselves for a paused day still gets its reminders.

## Usage

```
/ntm:pause
/ntm:pause <words>
/ntm:pause --check [<day>] [--until <day>]
```

- Bare: ask whether the user wants to see the pauses or change them, then do
  that with them.
- Words ("Friday", "next week", "remove the 12th", "show my pauses"): see or
  change the pauses as they say, with the user.
- `--check`: are these days paused?

`--check` covers the first day through the `--until` day, both included. The
first day defaults to `TODAY`, and the `--until` day defaults to the first day:

- `--check` alone checks today.
- `--check --until 2026-10-15` checks today through the 15th.
- `--check 2026-10-14 --until 2026-10-15` checks just those two days.

## Dates

Load `ntm:conventions` and compute `TODAY` as its Dates section says. Read dates
in any form a person would write (`2026-10-15`, `Oct 15`, `Friday`):

- A weekday name is the next one, today included: on a Thursday, "Friday" is
  tomorrow; on a Friday, it's today.
- "Next <weekday>" is that weekday of next week. Weeks start on Monday.
- A date without a year is the next one.
- A range includes its start and end days.

Show the resolved date in the reply, such as `Paused 2026-11-13 (Friday).`, so a
wrong guess is visible. Don't ask for confirmation before saving.

## Where pauses live

The `Pauses` database (see Databases in `ntm:conventions`) holds one bare line
per pause under its `## Pauses` heading, with no list marker, sorted by start
date. A single day, then a range:

```
YYYY-MM-DD: <why>
YYYY-MM-DD to YYYY-MM-DD: <why>
```

With no pauses, it holds the single line `None.`

Read it with the guide's `read database`. A missing database, or one with no
pause lines, means there are no pauses. If the read fails, stop and return
`Pause FAILED: <why>`, so no caller takes an unreadable database for "not
paused".

A line whose dates have no year is invalid. Ignore it whenever the database is
read, and remove it on the next save.

Save with the guide's `write database`, passing the whole content with only the
lines under `## Pauses` changed (`None.` if none are left). If the database is
missing, pass the `## Pauses` heading and the lines; `write database` creates
it. Pauses never overlap: before saving, merge any that do into one line
covering all their days, with their reasons joined by `; ` in start-date order.

## With `--check`

1. Read the database. If any pause ended before `TODAY`, or any line is invalid,
   remove those lines and save. If that save fails, answer anyway.
2. Return one line per day, as Result says.

## Bare, or with words

If a job runs this without `--check`, change nothing and say this needs a chat
with the user.

1. Read the database. Drop every pause that ended before `TODAY` and every
   invalid line, and tell the user which ones went.
2. Show the remaining pauses, then make the changes the user asks for. Don't ask
   for approval first: they said what they want.
    - A new pause gets a short reason in the user's words, or `paused` if they
      give none.
    - To end a range early, set its end to the last paused day. If that's before
      `TODAY` (as when ending it today), remove the line.
    - If a day they pause holds planned work, clear those dates.
    - Then load `ntm:plan` and replan the rest of the week with them, in chat.
3. If anything changed, step 1 included, save and show the saved list.

## Result

Plain text for whoever called the skill.

- With `--check`: one line per day, in order, and nothing else.
  `YYYY-MM-DD: true` when the day is paused, `YYYY-MM-DD: false` when it isn't
  and can be planned automatically.
- Bare, or with words: the pauses as saved, shown to the user.
- `Pause FAILED: <why>` when the database can't be read. A missing database
  isn't a failure.
