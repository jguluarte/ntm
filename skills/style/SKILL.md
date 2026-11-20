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
them is written. This skill reads `%Theme` and `%Message-history`. The writer
agent reads the parts of `%Theme` a message needs, and never `%Message-history`.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line. Then read `%Theme` and `%Message-history`: the theme the
sender names, or else this week's theme, as `%Settings` names it, and that
theme's history, found by its name, such as `Casebook-message-history.md`.

## What you write from

The sender hands over the facts, as its own file says. They hold what the
message must cover, and may hold its tasks and what's known of each, and
anything else its rule asks of the message, such as tone or length.

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

When it ends with `Nothing to refresh:`, the theme isn't built for the picker:
pick both yourself from the theme, from different kinds, and keep no line. That
isn't a failure. When it ends with a failure line, pick both yourself the same
way, and keep that line for the result.

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

The task that slipped most sets the `escalation` level. Slips from a while back
weigh less: a task picked up again after a long gap counts for less than its
slips, as you judge it.

When the root gives a ladder as one paragraph, that ladder has no level name.
Hand the writer what you called in its place, in plain words: for `escalation`,
a task slipped or kept slipping; for `finishing_tasks`, a task done, a win or a
big win.

A win is any of these: more tasks finished than planned this week, a task
finished after slipping for days, or a task you judge big or hard. Only the
weekly setup's message counts the week; a reminder looks only at the day. A big
win is a whole project finished: the project itself closes as done. It's rare.
Call either only from the facts you were handed, and look nothing else up. Call
each once, in the first message after it happens: a win that a
`%Message-history` entry already celebrated, with `win` or `big_win` in its
`type`, isn't called again.

Work out the message's type: each value below that holds, with commas between
them, such as `evening,slipped`.

| Value                               | When                                   |
| ----------------------------------- | -------------------------------------- |
| `morning`, `afternoon` or `evening` | `ntm:reminder` runs with that `--type` |
| `weekly`                            | It's the weekly setup's message        |
| `slipped`                           | A task in the facts slipped            |
| `done`                              | A task in the facts is done            |
| `win`                               | You called a win                       |
| `big_win`                           | You called a big win                   |

The self-test's message, and one written in chat, take none of the first two
rows' values.

### 3. Write

Start the `ntm:writer` agent, and hand it the facts, the levels, the reminder,
such as `morning` or `self-test`, the theme's name, and the perspective and the
reference, each as `<kind>/<slug>`. It reads the theme itself. It returns 5
versions, each with a title, a message, and a probability from 0 to 1 of how
likely a reader would be to predict it.

A slipped task goes in the facts as slipped, without its slip count or the dates
it slipped from: the `escalation` level, or the call in its place, carries
those.

When it returns `Writer FAILED:`, end with that line. When this session can't
start it, end with `Writer FAILED: can't start the writer`.

### 4. Choose

Take the version with the lowest probability whose first five words aren't any
entry's `opening`. Its title and message are what gets sent, and step 1's pick
goes into its entry.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry as the first line of the Entries part's `jsonl`
block, in the history Setup read. An entry is one JSON line, written compact,
with no spaces or line breaks added, and only the fields that have a value:

```
{"sent":"2026-11-13 08:45","reminder":"self-test","picks":{"perspective":"cast/chief","reference":"scenes/fog"}}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `reminder`: which message it is: the reminder's type, such as `morning`, or
  `weekly`, or `self-test`
- `type`: the message's type from step 2, exactly as built, such as
  `evening,done,win`, only when it has one
- `levels`: step 2's level on each ladder by name, only the ladders that have
  one, such as
  `"levels":{"escalation":"raised_eyebrow","finishing_tasks":"case_closed"}`
- `picks`: step 1's `perspective` and `reference`, as the picker printed them,
  or by name when you picked them yourself
- `opening`: the message's first five words, as sent
- `tasks`: each task the message is about, with its planned date when it has
  one, such as `"tasks":[{"id":"ABC-12","planned":"2026-11-13"}]`
- `feedback`: the user's word on it, `keep` or `stale`
- `verdict`: `acted` or `ignored`, written by the weekly setup job

Then drop the entries older than the `Keep:` line, and save.

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
