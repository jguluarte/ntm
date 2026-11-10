---
name: style
description: >-
    Writes a message in the user's style, from their Style database, and keeps
    their Message history. Loaded by the messenger agent for every message it
    sends. Changes the style with the user in chat when they say "change how
    reminders talk to me" or "make it meaner".
---

# ntm:style

The user's style is the persona in their `Style` database: who talks to them and
how, so they actually read what ntm sends. This skill rewrites a plain message
in it, and changes it with the user. It keeps `Message history`, what the
messages have said, so the next ones stay fresh and a task that keeps slipping
climbs the style's levels.

## Setup

Load `ntm-user:backend` to read the user's conventions, then read the user's
`Style` and `Message history` databases. The comments in their templates,
`style.md` and `message-history.md` under `references/databases/` in the newest
installed `ntm`, say what each part is for and how it's kept. Follow them
whenever you save either one.

When the Style is a persona, the user's own text in place of a Profile, that
text is the style, its levels and motifs included. Its `## For ntm` section maps
this skill's call onto its words. This skill's `references/persona-contract.md`
says what a Profile and a persona each hold.

## Usage

```
Usage:
    type: <type>
    [tone: <tone>]
    message: <message>

    /ntm:style [<what to change>]

Inputs:
    type:             the messenger's type: freeform, or a path into the user's
                      Message rules, such as reminders.morning
    tone:             how the message should feel today, in a few words
    message:          the core message, in plain words
    <what to change>  in the user's words, such as "make it meaner"
```

With nothing after it, show the user their Style and ask what they'd like to
change.

## Writing a message

### 1. Find each task's level

A task the message names climbs as it keeps slipping. Count the earlier days
Message history names the task; the Style's Responding to procrastination part
gives the level for that count.

### 2. Write it

Rewrite the message the way the Style says, in the tone given. The Style's The
reminders part says what each reminder is in the theme's terms; when the type
has a part there, write the message as that part says: `reminders.morning` is
Morning.

Keep every fact as given: task ids, dates, counts and names, nothing added. Keep
it fresh: no opening, joke shape or pun from a line in Message history, and a
motif rests as the Motifs part's repeat limit says.

### 3. Title it

End with a `Title:` line that says what the message is about, in the same style,
never just the type's name.

### 4. Record it

Add one entry to Message history for this message: today's date, the task ids it
names, and the message as written.

### Result

The message in plain text, then the `Title:` line.

## Changing the style

Change the Style with the user in chat, the way their words say. Its template's
comments and `references/persona-contract.md` say what each part is for and how
it's written. Save without asking them to approve: they said what they want.
Then show the parts that changed as they now read.
