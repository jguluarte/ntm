# Message rules

<!--
What each reminder's message says, for the messenger agent. A skill asks the
messenger for a type such as `reminders.morning`, and the type is the path to
its rule under Types: Types > Reminders > Morning. Rules are found by those
names, so keep them. How a message sounds is `%Theme`'s job, not this
database's.

Setup creates this database from this template. The user edits a rule, adds to
it, or deletes it to go back to this template's. These comments are for the
agent, and are never written into the user's database.
-->

## Types

<!--
Each rule opens with its Fact table, the facts its skill hands the messenger:
keep it as it is, since the skill sends exactly those. The rest of a rule is
the user's to change: what the message says, the list under it, and when no
notification is needed.
-->

### Reminders

#### Morning

| Fact      | Holds                                           |
| --------- | ----------------------------------------------- |
| `today:`  | the open tasks planned for today                |
| `paused:` | `yes` when today is in `%Paused-dates`, or `no` |

Message: what's planned for today, naming each carried-over task with the date
it was carried over from. With `today: none`, nothing plannable is left on the
task list: suggest a review with `/ntm:review-todo-list`.

List: the `today:` tasks.

No notification: when `paused: yes` and `today: none`.

#### Afternoon

| Fact      | Holds                                           |
| --------- | ----------------------------------------------- |
| `open:`   | the open tasks planned for today                |
| `paused:` | `yes` when today is in `%Paused-dates`, or `no` |

Message: a tap on the shoulder about what's still open, naming each started task
as started. Never a dig. With `open: none`, quick props, nothing more.

List: the `open:` tasks.

No notification: when `paused: yes` and `open: none`.

#### Evening

| Fact    | Holds                            |
| ------- | -------------------------------- |
| `done:` | the tasks done today             |
| `open:` | the open tasks planned for today |

Message: how the day went. A final push on what's still open, with what got done
in a clause; with `open: none`, a celebration of what got done.

List: the `open:` tasks.

No notification: when `done: none` and `open: none`.

#### Week

| Fact       | Holds                                             |
| ---------- | ------------------------------------------------- |
| `done:`    | the tasks done in the past week                   |
| `open:`    | the tasks planned in the past week and still open |
| `planned:` | the tasks planned for the week ahead              |

Message: the past week, then the week ahead, a sentence or so each. The past
week: what got done, as a count and a theme, and what's still open. The week
ahead: what's planned, as a count and a theme. Name only the still-open tasks.

List: none.

No notification: when `done:`, `open:` and `planned:` are all `none`.
