# Message history

<!--
What ntm's messages have said, so the next ones don't repeat it and a task that
keeps slipping climbs the levels in their `%Theme`. `ntm:style` keeps it. Setup
creates this database from this template, and writes it without these comments:
they are for you, never for the user. The user can edit, delete or add any part,
and you find each part by its name.

`Keep:` is how much history to keep. After each new entry, drop the entries
older than that.
-->

Keep: 8 weeks

## Entries

<!--
One JSON line per message sent, newest first: the date it went out; its type;
the ids of the tasks it's about, `[]` when sent without `record_task_ids`; what
the user's `%Theme` says an entry records, `{}` when it says nothing; and the
message as sent. The ids are how `ntm:reminder` counts the days a task has
slipped. A line looks like
{"date":"2026-11-09","type":"weekly","ids":[],"record":{"motif":"storm"},"line":"Storm warning: the gutters (ABC-12)."}
-->

```jsonl

```
