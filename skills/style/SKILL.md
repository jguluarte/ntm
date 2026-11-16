---
name: style
description: >-
    Turns a message's facts into a finished message in the user's style: picks
    what it draws on from their `%Theme`, sets the tone, has the writer agent
    write versions, chooses one, and records it in `%Message-history` once it's
    sent. Loaded for every message ntm sends in the user's style. In chat,
    writes something in the user's style when they ask, changes their theme with
    them ("make my reminders meaner"), and notes it when the user says a message
    is a keeper or has gone stale ("keep that one", "that one's stale").
---

# ntm:style

The user's style is their `%Theme`, the database that says how every message to
them is written. This skill reads `%Theme` and `%Message-history`. The writer
agent reads only the parts of `%Theme` this skill points it to, and never
`%Message-history`.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line. Then read `%Theme` and `%Message-history`: this week's
theme, as `%Settings` names it, and that theme's history, found by its name,
such as `Casebook-message-history`.

## What you write from

The sender hands over the facts, as its own file says. They hold what the
message must cover, and may hold its tasks and what's known of each, and
anything else its rule asks of the message, such as tone or length.

## Writing a message

### 1. Pick

Pick one hook, the idea this message builds on: one entry of the theme, drawn by
the picker as The picker, below, says. Hand it the message's type: each value
below that holds, with commas between them, such as `evening,slipped`.

| Value                               | When                                     |
| ----------------------------------- | ---------------------------------------- |
| `morning`, `afternoon` or `evening` | `ntm:reminder` runs with that `--type`   |
| `weekly`                            | It's the weekly setup's message          |
| `slipped`                           | A task in the facts slipped              |
| `done`                              | A task in the facts is done              |
| `win`                               | The facts show a win, as step 2 says     |
| `big_win`                           | The facts show a big win, as step 2 says |

The self-test's message, and one written in chat, take none of the first two
rows' values. With no value at all, leave `--type` out.

The hook comes back as `<kind>/<slug>`. Its entry is under `<kind>`, keyed
`<slug>`, in the file the `<kind>` pool names in `%Theme-options`.

When the picker fails, pick the hook yourself: one motif, or one line from the
theme's examples. Take one that no recent `%Message-history` entry used, from
each entry's `hook`, or for an older entry, judging from its `line` which motif
it used. Recent entries are those from the last two weeks, or from the span the
theme's `Repeat limit:` line gives, when it has one.

Pick a speaker, the person in the theme who says the message, only when the
theme names people who talk.

The theme material is what the writer gets of the theme: its guidance, which is
every part that says how to write (its registers, its levels, its flow), and the
entries for the hook and the speaker.

### 2. Set the tone

Read the facts against the theme's guidance and set the tone: how hard each
slipped task is pressed, a nod for what's done, and anything the facts ask of
the tone. Call for a celebration only for a win or a big win. A win is any of
these: more tasks finished than planned this week, a task finished after
slipping for days, or a task you judge big or hard. A big win is a whole project
finished: the last open task in a project closes. Call either only from the
facts you were handed; look nothing else up. A big win is rare: when the facts
don't plainly show a whole project finished, it isn't one. An ordinary day of
doing what was planned gets a nod. Slips from a while back weigh less: a task
picked up again after a long gap is pressed less than its count of slips, as you
judge it.

### 3. Write

Start the `ntm:writer` agent, and hand it the facts, the tone, the hook, the
speaker, and the theme material, as text or as exactly which parts of `%Theme`
to read. It returns 5 versions, each with a title, a message, and a probability
from 0 to 1 of how likely a reader would be to predict it.

When it returns `Writer FAILED:`, end with that line. When this session can't
start it, end with `Writer FAILED: can't start the writer`.

### 4. Choose

Take the version with the lowest probability whose first five words aren't the
`opening` of a recent entry, or the start of an older entry's `line`. Its title
and message are what gets sent, and step 1's hook and speaker go into its entry.

## The picker

The picker is a script in this skill that draws a hook from the theme's options
file. It reads that file from a path and touches no backend, and
`%Theme-options` lives in the user's backend, so hand it over this way.

A theme without `%Theme-options` isn't built for the picker: pick the hook
yourself, as step 1 says, and keep no line. That isn't a failure.

Read `%Theme-options` and take the text of its `yaml` block. Write that text to
a file named for the theme, such as `Casebook-options.yaml`, in this session's
working folder, exactly as read: never retype it from memory or summarize it.
Then run the picker on that file, with the message's type from step 1:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/picker.py hook \
    --options <the file> --type <the message's type>
```

It prints one line: `hook: <kind>/<slug>`, the hook it drew.

It needs Python 3 with PyYAML and jsonschema, and nothing guarantees them where
this runs: without them, the script stops with a Python error. Any other output,
or a part of this you can't do, means the picker failed. Keep one line for the
result: the `Picker FAILED: <failure>: <why>` line it printed, or else
`Picker FAILED: <why>`, with the last line it printed or what you couldn't do.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry at the top of the Entries part of the history Setup
read. An entry is one JSON line, written compact, with no spaces or line breaks
added, and only the fields that have a value:

```
{"sent":"2026-11-13 08:45","reminder":"morning","hook":"scenes/dawn","tasks":[{"id":"ABC-12","planned":"2026-11-13"}]}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `reminder`: which message it is: the reminder's type, such as `morning`, or
  `weekly`, or `self-test`
- `hook`: what step 1 picked, as the picker printed it, such as `scenes/dawn`,
  or by its name when you picked it yourself, such as `launch`
- `speaker`: who step 1 picked, only when it picked one
- `opening`: the message's first five words, as sent
- `tasks`: each task the message is about, with its planned date when it has one
- `feedback`: the user's word on it, `keep` or `stale`
- `verdict`: the nightly rater's

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
