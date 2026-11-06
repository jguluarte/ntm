---
name: days-off
description: Days off for the user's nudge board, the days when nothing gets planned automatically. Set or change them in chat ("pause Friday", "unpause next week", "show my days off"), or check whether days are days off.
---

# nudge:days-off

A day off is a day or a date range when nothing new gets planned automatically. Work the user dated themselves for a day off still gets its reminders.

"Pause Friday" or "unpause next week" means adding or ending a day off. Automation only uses `--check`, and reads its answer as whether each day is a day off.

## Where days off live

The note named by the config's `days off note`, one line per day off under its `## Days off` heading, sorted by start date:

- `YYYY-MM-DD: note` for a single day
- `YYYY-MM-DD to YYYY-MM-DD: note` for a range
- `None.` when there are none

Read it with the adapter's `read note`. A missing note, or one with no day-off lines, means there are no days off. If the read itself fails, stop and return `Days off FAILED: <why>`, so a caller never takes an unreadable note for "not a day off".

A line whose dates have no year is invalid. Whenever the note is read, for any reason, ignore those lines and remove them on the next save.

To save, use the adapter's `write note` and change only the lines under `## Days off`, with `None.` if nothing is left. Days off never overlap: before saving, merge any that overlap into one line covering all their days, with their notes joined by `; ` in start-date order. When the note is missing, `write note` creates it, with the `## Days off` heading.

## Usage

```
/nudge:days-off
/nudge:days-off --check [START] [--until END]
```

- No flags, or the user asking in chat to add, end or see their days off: review or change them with the user.
- `--check`: are these days off? It checks `START` through `END`, both included. `START` defaults to `TODAY`, and `END` defaults to `START`, so `--check` alone checks today, `--check --until 2026-10-15` checks today through the 15th, and `--check 2026-10-14 --until 2026-10-15` checks just those two days.

Dates passed to `--check` can be in any form a person would write (`2026-10-15`, `Oct 15`, `Friday`); interpret them as the Dates section says. The output always uses `YYYY-MM-DD`.

## Dates

Load `nudge:board` and compute `TODAY` as its Dates section says. A range covers both its start and end days. A date given without a year, by the user or a caller, means the next such date on or after `TODAY`.

## With `--check`

1. Read the note. If any day off ended before `TODAY`, or any line is invalid, remove those lines and save.
2. Return one line per day from `START` to `END`, in order, and nothing else, as Result says.

## Without flags

If a job calls this without flags, change nothing and say this needs a chat with the user.

1. Read the note. Drop every day off that ended before `TODAY` and every invalid line, and tell the user which ones went.
2. Show the user the remaining days off, then make the changes they ask for, if any. New days off get a short note in the user's words, or `day off` if they give none. To end a range early, set its end to the last day off; if that's before `TODAY` (as with ending it today), remove the line.
3. If anything changed, step 1 included, save and show the user the saved list.

## Result

Plain text for whoever called the skill.

- With `--check`: one line per day, in order, and nothing else: `YYYY-MM-DD: true` when that day is a day off, or `YYYY-MM-DD: false` when it isn't, so it can be planned automatically.
- Without flags: the days off as saved, shown to the user.
- `Days off FAILED: <why>` when the note can't be read. A missing note isn't a failure: it means there are no days off.
