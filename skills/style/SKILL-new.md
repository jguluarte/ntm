---
name: style
description: >-
    Writes a message in the user's style, from their Style database, and keeps
    their Message history. Loaded by the messenger agent for every message it
    sends.
---

# ntm:style

The user's style is the persona in their `Style` database: who talks to them and
how, so they actually read what ntm sends. This skill rewrites a plain message
in it. It keeps `Message history`, what the messages have said, so the next ones
stay fresh and a task that keeps slipping climbs the style's levels.

## Setup

Load `ntm-user:backend` to read the user's conventions, then read the user's
`Style` and `Message history` databases. The comments in their templates,
`style.md` and `message-history.md` under `references/databases/` in the newest
installed `ntm`, say what each part is for and how it's kept. Follow them
whenever you save Message history.

When the Style is a persona, the user's own text in place of a Profile, that
text is the style, its levels and motifs included. Its `## For ntm` section maps
this skill's call onto its words.

## Usage

```
Usage:
    /ntm:style --for <type> ["<tone>"] <message>

Inputs:
    --for <type>  the messenger's type: freeform, or a path into the user's
                  Message rules, such as reminders.morning
    <tone>        how the message should feel today, in a few words
    <message>     the core message, in plain words
```

## Writing a message

### 1. Find each task's level

A task the message names climbs as it keeps slipping. Its earlier days are the
days before today with a Message history entry that names its id, and its level
is the one the Responding to procrastination part gives for that count.

### 2. Write it

Rewrite the message the way the Style says, in the tone given. When the type has
a part in The reminders, that part says what this message is in the theme's
terms: `reminders.morning` is Morning.

Keep every fact as given: task ids, dates, counts and names, nothing added. Keep
it fresh: no opening, joke shape or pun from a line in Message history, and a
motif rests as the Motifs part's repeat limit says.

### 3. Title it

End with a `Title:` line that says what the message is about, in the same style,
never just the type's name.

### 4. Record it

Add one entry to Message history for this message: today's date, the task ids it
names, and the message as written.

## Result

The message in plain text, then the `Title:` line.
