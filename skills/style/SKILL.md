---
name: style
description: >-
    Turns a message's facts into a finished message in the user's style: picks
    what it draws on from their theme, sets the tone, has the writer agent write
    versions, chooses one, and records it in `%Message-history` once it's sent.
    Loaded for every message ntm sends in the user's style. In chat, writes
    something in the user's style when they ask, changes their theme with them
    ("make my reminders meaner"), and notes it when the user says a message is a
    keeper or has gone stale ("keep that one", "that one's stale").
---

# ntm:style

The user's style is this week's theme, the one the Themes part of `%Settings`
names. A theme is a set of theme files, as
`${CLAUDE_PLUGIN_ROOT}/references/theme-files.md` describes, or, until it moves
to them, the `%Theme` database. It is in files when `ntm-user:backend` lists its
options file. This skill reads the theme and `%Message-history`. The writer
agent reads only the parts of the theme this skill points it to, and never
`%Message-history`.

## Setup

Load `ntm-user:backend`, which says where the theme and `%Message-history` live,
and read both: for a theme in files, its root.

## What you write from

The sender hands over the facts, as its own file says. They hold what the
message must cover, and may hold its tasks and what's known of each, and
anything else its rule asks of the message, such as tone or length.

## The occasions

From the facts, work out which occasions hold for the message: which reminder it
is, when it is one, and what happened to its tasks. They decide what the message
can draw on, and a big win sets the tone.

| Occasion                          | When it holds            |
| --------------------------------- | ------------------------ |
| `morning`, `afternoon`, `evening` | It is that reminder      |
| `weekly`                          | It is the week's message |
| `slipped`                         | A task in it has slipped |
| `done`                            | A task in it got done    |
| `big_win`                         | A big effort, as below   |

A big win is one of these: several tasks closed in one day that had been planned
across several days, a task with a big estimate finally closed, or a task that
slipped many times finally closed. An ordinary day of doing what was planned is
never a big win.

## Writing a message

### 1. Pick

For a theme in files, the picker picks the hook, the speaker and the line.
Otherwise, pick as Picking without the picker says.

The picker is `${CLAUDE_PLUGIN_ROOT}/scripts/picker/pick`; run it with `bash`.
Save the text of the options file's `yaml` block to a file, and the lines of the
Entries part of `%Message-history` to another. Then pick the hook and speaker:

```
pick hook --options <options file> --history <history file> --theme <theme>
    --occasions <occasions> --now "<YYYY-MM-DD HH:MM>"
```

`<theme>` is the root's `theme`, `<occasions>` the occasions that hold, with
commas between them, and `--now` the time now in the user's timezone. It prints
`hook: <kind>/<slug>` and `speaker: <kind>/<slug>`, or `speaker: none`.

Fetch the hook's entry file, the `file` its pool names in the options file, and
save its `yaml` block's text to a file. Then draw the hook's line, with the same
flags and two more:

```
pick line <the same flags> --hook <kind>/<slug> --entries <entry file>
```

It prints `line: <the line>`, then `bend: <how to turn it>` when it has one, or
`line: none`.

When `pick hook` also prints a `fallback:` line, the theme has nothing for these
occasions: add that line after the sender's result. When either prints
`Picker FAILED:` or can't run, pick as Picking without the picker says, and add
`Picked without the picker: <why>` after the sender's result.

The theme material is what the writer gets of the theme:

- the root, whole
- each file the root marks `whole`
- for the hook and the speaker, their file's `about`, their kind's `about`, and
  their entry, with only the line drawn in place of the hook's `lines` and
  `riffs`, and none of the speaker's

For the writer, the hook is the line drawn, with its bend, or the hook's entry
when no line was drawn.

### 2. Set the tone

Read the facts against the theme's guidance and set the tone: how hard each
slipped task is pressed, a nod for what's done, and anything the facts ask of
the tone. Call for a celebration only on a big win, as The occasions says. An
ordinary day of doing what was planned gets a nod. Slips from a while back weigh
less: a task picked up again after a long gap is pressed less than its count of
slips, as you judge it.

### 3. Write

Start the `ntm:writer` agent, and hand it the facts, the tone, the hook, the
speaker, and the theme material, as text or as exactly which parts of the theme
to read. It returns 5 versions, each with a title, a message, and a probability
from 0 to 1 of how likely a reader would be to predict it.

When it returns `Writer FAILED:`, end with that line. When this session can't
start it, end with `Writer FAILED: can't start the writer`.

### 4. Choose

Take the version with the lowest probability whose first five words aren't the
`opening` of a recent entry, or the start of an older entry's `line`. Its title
and message are what gets sent, and step 1's hook, speaker and line go into its
entry with the theme's name.

## Keeping `%Message-history`

Once `ntm-user:notify` has sent the message, or handed it back for the job's
final reply, add its entry at the top of the Entries part. An entry is one JSON
line, written compact, with no spaces or line breaks added, and only the fields
that have a value:

```
{"sent":"2026-11-13 08:45","reminder":"morning","hook":"launch","tasks":[{"id":"ABC-12","planned":"2026-11-13"}]}
```

- `sent`: when it went out, 24-hour, in the user's timezone
- `reminder`: which message it is: the reminder's type, such as `morning`, or
  `weekly`, or `self-test`
- `theme`: the theme's name
- `hook`, `speaker`: what step 1 picked, as the picker printed them,
  `<kind>/<slug>`; `speaker` only when it picked one
- `line_drawn`: the line step 1 drew for the hook, word for word, so the picker
  can rest it; only when it drew one
- `opening`: the message's first five words, as sent
- `tasks`: each task the message is about, with its planned date when it has one
- `feedback`: the user's word on it, `keep` or `stale`
- `verdict`: the nightly rater's

Then drop the entries older than the `Keep:` line, and save.

## Picking without the picker

For a theme not in files yet, or when the picker fails.

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

For a theme in files, pick an entry of its options file this way, and gather the
theme material as step 1 says.

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
