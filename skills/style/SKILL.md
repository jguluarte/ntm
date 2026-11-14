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

Load `ntm-user:backend`, which says where `%Theme` and `%Message-history` live,
and read both.

## What you write from

The sender hands over the facts, as its own file says. They hold what the
message must cover, and may hold its tasks and what's known of each, and
anything else its rule asks of the message, such as tone or length.

## Writing a message

### 1. Pick

Pick one hook, the idea this message builds on: one motif, or one line from the
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
the tone. Call for a celebration only for a big effort: several tasks closed in
one day that were planned across several days, a task with a big estimate
finally closed, or one that slipped many times finally closed. An ordinary day
of doing what was planned gets a nod. Slips from a while back weigh less: a task
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
and message are what gets sent, and step 1's hook and speaker go into its entry
with the theme's name.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry at the top of the Entries part. An entry is one JSON
line, written with only the fields that have a value. Spread over lines here:

```json
{
    "sent": "2026-11-13 08:45",
    "reminder": "morning",
    "theme": "Deep space",
    "hook": "the launch window",
    "opening": "Shelf day, one bracket first",
    "tasks": [{ "id": "ABC-12", "planned": "2026-11-13" }]
}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `reminder`: which message it is: the reminder's type, such as `morning`, or
  `weekly`, or `self-test`
- `theme`: the theme's name
- `hook`, `speaker`: what step 1 picked; `speaker` only when it picked one
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
