# Message rules

<!--
What each reminder's message says, for the messenger agent. A skill asks the
messenger for a type such as `reminders.morning`, and the type is the path to
its rule: Reminders > Morning. Rules are found by those names, so keep them. How
a message sounds is `%Theme`'s job.

Setup creates this database from this template. The user edits a rule, adds to
it, or deletes it to go back to this template's. These comments are for the
agent, and are never written into the user's database.
-->

## Reminders

<!--
What every reminder shares. Each reminder's own part below adds to it, and wins
where they differ. A reminder's facts are the ones its skill hands the
messenger: keep them as they are, since the skill sends exactly those. The rest
is the user's to change: what the message says, the list under it, and when no
notification is needed.
-->

| Fact      | Holds                                           |
| --------- | ----------------------------------------------- |
| `open:`   | the open tasks planned for today                |
| `done:`   | the tasks done today                            |
| `paused:` | `yes` when today is in `%Paused-dates`, or `no` |

List: the `open:` tasks.

No notification: when `paused: yes` and `open: none`.

### Morning

Facts: `today:` in place of `open:`, and `paused:`.

Message: what's planned for today, naming each carried-over task with the date
it was carried over from. With `today: none`, nothing plannable is left on the
task list: suggest a review with `/ntm:review-todo-list`.

### Afternoon

Facts: `open:` and `paused:`.

Message: a tap on the shoulder about what's still open, naming each started task
as started. Never a dig. With `open: none`, quick props, nothing more.

### Evening

Facts: `done:` and `open:`.

Message: how the day went. A final push on what's still open, with what got done
in a clause; with `open: none`, a celebration of what got done.

No notification: when `done:` and `open:` are both `none`.

### Week

Facts: `done:` and `open:` over the past week instead of today, and `planned:`,
the tasks planned for the week ahead.

Message: the past week, then the week ahead, a sentence or so each. The past
week: what got done, as a count and a theme, and what's still open. The week
ahead: what's planned, as a count and a theme. Name only the still-open tasks.

List: none.

No notification: when `done:`, `open:` and `planned:` are all `none`.
