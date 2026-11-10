---
Keep: 8 weeks
---

# Message history

<!--
For the agent: what the user's reminders have said, so the next ones don't
repeat it and a task that keeps slipping climbs the style's levels. Its shape
and its `Keep:` line are ntm's suggested defaults, which the user can customize:
they can edit, delete or add parts, and you find each part by its name. Setup
creates this database from this template, without these comments: they are for
you, never for the user. `ntm:style` keeps it; everything else only reads it.
The `Keep:` line in the frontmatter says how much history to keep. The user
changes it to keep more or less; without it, keep 8 weeks.
-->

## Entries

<!--
One line per message sent, newest first: the date it went out, the task ids it
names, and its line, the sentences as sent without the list. The ids are how a
slipping task's days get counted. After each new entry, drop the ones older
than the `Keep:` line allows. A line looks like
{"date":"2026-11-09","ids":["HOME-3"],"line":"Gutters, day three. They are not cleaning themselves."}
-->

```jsonl

```
