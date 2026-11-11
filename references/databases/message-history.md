# Message history

<!--
For the agent: what the user's reminders have said, so the next ones don't
repeat it and a task that keeps slipping climbs the levels in their `%Theme`.
`ntm:style` keeps it. Setup creates this database from this template, and
writes it without these comments: they are for you, never for the user. The
user can edit, delete or add any part, and you find each part by its name.

`Keep:` is how much history to keep. After each new entry, drop the entries
older than that.
-->

Keep: 8 weeks

## Entries

<!--
One row per message sent, newest first: the date it went out, the ids of the
tasks it names, and the message as sent, without its list. The ids are how
`ntm:style` counts the days a task has slipped. A row looks like
| 2026-11-09 | ABC-12 | The gutters (ABC-12), day three. Still waiting. |
-->

| Date | Tasks | Message |
| ---- | ----- | ------- |
