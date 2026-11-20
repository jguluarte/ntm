---
name: style
description: >-
    Turns a message's facts into a finished message in the user's style: picks
    what it draws on from their `%Theme`, works out the message's levels, has
    the writer agent write versions, chooses one, and records it in
    `%Message-history` once it's sent. Loaded for every message ntm sends in the
    user's style. In chat, writes something in the user's style when they ask,
    changes their theme with them ("make my reminders meaner"), and notes it
    when the user says a message is a keeper or has gone stale ("keep that one",
    "that one's stale").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line. Then read `%Theme` and `%Message-history`: the theme the
sender names, or else this week's theme, as `%Settings` names it, and that
theme's history, found by its name, such as `Casebook-message-history.md`.

## Writing a message

### 1. Pick

The message is built on one pick: a perspective and a reference, two entries of
the theme. The perspective is who or what tells the message: a speaker, or a
piece of the world that tells it, such as a scene. The reference is another
piece of the world it draws on.

Take the first pick from the theme's picks list, `<Theme>-picks.yaml`, such as
`Casebook-picks.yaml`, and save the list without it. The list is a YAML list,
each item a `perspective:` and a `reference:`. When there is no list, or it's
empty, load `ntm:refresh-picks` and follow it, then take the first pick from the
new list.

When it ends with `Nothing to refresh:` or a failure line, pick both yourself
from the theme, from different kinds, and keep a failure line for the result.

### 2. Work out the levels

The theme's root gives two ladders, `escalation` and `finishing_tasks`, each a
set of levels from the first up, keyed by name. Work out one level on each from
the facts, judged against the ladder's own words:

| Ladder            | When                 | Level                       |
| ----------------- | -------------------- | --------------------------- |
| `escalation`      | Nothing slipped      | The first                   |
| `escalation`      | A task slipped       | Higher                      |
| `escalation`      | A task kept slipping | Higher still, up to the top |
| `finishing_tasks` | Nothing is done      | None                        |
| `finishing_tasks` | A task is done       | The first                   |
| `finishing_tasks` | A win                | The second                  |
| `finishing_tasks` | A big win            | The third                   |

The task that slipped most sets the `escalation` level, and slips from a while
back weigh less, as you judge it.

When the root gives a ladder as one paragraph, that ladder has no level name.
Hand the writer what you called in its place, in plain words: for `escalation`,
a task put off, or put off again and again; for `finishing_tasks`, a task done,
a win or a big win.

A win is more tasks finished than planned this week, which only the weekly
setup's message counts; a task finished after slipping for days; or a task you
judge big or hard. A big win, which is rare, is a whole project closed as done.
Call each only from the facts you were handed, and once: skip one a
`%Message-history` entry already called, with `win` or `big_win` in its `type`.

### 3. Write

Start the `ntm:writer` agent, and hand it the facts, as below, the levels, the
reminder, such as `morning`, `weekly` or `self-test`, the theme's name, and the
perspective and the reference, each as `<kind>/<slug>`. Hand it too the caps
`ntm-user:notify` gives on a title and a message: read `ntm-user:notify` for
them, without sending anything. The writer reads the theme itself. It returns 5
versions, each with a title and a message.

For a reminder, the writer gets less than the sender gathered: what the rule
asks of the message; each task by its title and whether it's done; and, for the
afternoon and evening, what changed among today's tasks since the earlier
reminders, by title: a task added, done or moved off today. Nothing more. A
slipped task goes over as one the user meant to do earlier and hasn't. Tasks
that belong together, such as sub-tasks of one task, go over as one group: what
they share and how many, in place of their titles. How hard to press goes over
only as the `escalation` level, or the call in its place.

Any other message's facts go over as its sender gathered them, with each task by
its title.

When it returns `Writer FAILED:`, end with that line. When this session can't
start it, end with `Writer FAILED: can't start the writer`.

### 4. Choose

Among the versions within the caps whose first five words aren't any entry's
`opening`, take the one most likely to get a reaction out of the user, a laugh
or a sting alike: the one they'd want to show someone. Its title and message are
what gets sent, as the writer wrote them, and step 1's pick goes into its entry.

## Keeping `%Message-history`

Once the message is sent, or handed back for the job's final reply, add its
entry as the first line of the Entries part's `jsonl` block, in the history
Setup read: one compact JSON line, with only the fields that have a value.

```
{"sent":"2026-11-13 08:45","type":"win","picks":{"perspective":"characters/detective","reference":"scenes/stakeout"}}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `type`: the wins step 2 called: `win`, `big_win`, or both as `win,big_win`
- `picks`: step 1's `perspective` and `reference`, as the picker printed them or
  as you named them
- `opening`: the message's first five words, as sent
- `tasks`: each task the message is about, with its planned date when it has
  one, such as `[{"id":"ABC-12","planned":"2026-11-13"}]`
- `feedback`: the user's word on it, `keep` or `stale`
- `verdict`: `acted` or `ignored`, written by the weekly setup job

Then drop the entries older than the history's `Keep:` line, such as
`Keep: 8 weeks`, and save.

## In chat

When the user asks for something in their style, write it with steps 1 to 4 and
show it to them.

When they ask to change how their messages read, find the part of `%Theme` they
mean, draft the change with them, show it, and save it when they say yes. For a
whole new theme or a rebuild, load `ntm:theme-builder` and follow it instead.

When they say a message is a keeper or has gone stale, in their own words ("keep
that one", "loved that", "stale", "that one's old"), find its entry in
`%Message-history`: the one with the opening words of the message shown in this
chat, or the newest entry when none is shown. Set its `feedback` to `keep` or
`stale`, save, and tell them in a line that it's noted.
