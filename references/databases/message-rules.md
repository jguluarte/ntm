# Message rules

<!--
For the agent: these rules are ntm's suggested defaults for what each
reminder's message says, set up as a database of the user's own so they can
customize them. They edit a rule to change its message, or delete it to go back
to ntm's default. Write the database with the rules only, without these
comments: they are for you, never for the user. A rule's place under Types is
its type: `type: reminders.morning` is Types > Reminders > Morning. Each rule
holds the facts the messenger is given, what the sentences say and what the
list under them holds. How the message sounds is the style's job, not this
database's.
-->

## Types

<!--
The Fact table is what ntm hands the messenger: keep it as it is. The user
changes the sentences and the list.
-->

### Reminders

#### Morning

| Fact     | Holds                         |
| -------- | ----------------------------- |
| `today:` | one open task each, or `none` |

The sentences: today's tasks, naming each carried-over task with the date it
had, as given. With `today: none`, the todo list has nothing left to plan: ask
them to review it with `/ntm:review-todo-list`.

When today is paused and nothing is planned, no notification is needed.

The list: the `today:` tasks. `today: none` carries no list.

#### Afternoon

| Fact    | Holds                         |
| ------- | ----------------------------- |
| `open:` | one open task each, or `none` |

The sentences: a tap on the shoulder about what's still open, naming a
`(started)` task as started. With `open: none`, quick props, nothing more. Never
a dig, whatever the history says.

The list: the `open:` tasks. `open: none` carries no list.

#### Evening

| Fact    | Holds                               |
| ------- | ----------------------------------- |
| `done:` | one task done today each, or `none` |
| `open:` | one open task each, or `none`       |

The sentences: how the day went: what's still open, naming each that was carried
over with the date it had, as given, and what closed in a clause; or, with
`open: none`, what got done. The style decides how hard a carried-over task gets
it, from its own count of the days.

The list: the `open:` tasks. `open: none` carries no list.

#### Week

| Fact              | Holds                                                                      |
| ----------------- | -------------------------------------------------------------------------- |
| `done:`           | one task done last week each, `none` or `unavailable`                      |
| `open:`           | one task still open from last week each, or `none`                         |
| `planned:`        | one task planned for the week ahead each, or `none`                        |
| `weekly message:` | which halves the user wants, from the job's prompt or `ntm:plan`'s default |

The sentences: two halves, a sentence or so each. Last week: what got done, as a
count and a theme, and what's still open. With `done: none` and open tasks, say
nothing closed and what's still open. The week ahead: what's coming, as a count
and a theme; with `planned: none`, say so. With `done: unavailable`, the week
ahead only.

Name only the still-open tasks, by id, written plain (`(HOME-3)`), no links.

No list.

#### Completed

| Fact    | Holds                                                   |
| ------- | ------------------------------------------------------- |
| `span:` | `<first day> to <last day>`                             |
| `done:` | one task done in the span each, oldest first, or `none` |

The sentences: what got done over the span, with the count. With `done: none`,
that nothing closed, plainly.

The list: the `done:` tasks. `done: none` carries no list.
