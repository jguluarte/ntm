# Theme files

A theme is what ntm writes every reminder in: a world the user enjoys, with
enough material to keep each message different. This file describes the files a
theme is made of, for the skills that build, pick from and score a theme, and
for anyone curious.

## Where themes are going

ntm is moving to a script, the picker, that picks what each message draws on,
and a writer that writes the message from the picks. For a script to pick, a
theme has to be data in a known shape, and this file is that shape. Today a
user's theme is still one `%Theme` database, as `ntm:theme-builder` builds it,
and no run reads theme files yet.

A user will be able to have several themes. The Themes part of `%Settings` lists
each one by its root and names this week's theme, the one everything picked in a
week comes from. Each week, the weekly job will move to the next theme in the
list. With one theme, it is always that one.

## A theme's files

A theme named `<Theme>` is a set of files, each named after it, so a theme's
files sort together:

| File                     | What it is                                           |
| ------------------------ | ---------------------------------------------------- |
| `<Theme>.yaml`           | The root: the writer's guide, and the list of files  |
| `<Theme>-options.yaml`   | What the theme offers the picker, and its numbers    |
| `<Theme>-<kinds>.yaml`   | An entry file: one or more kinds of entry            |
| `<Theme>-terminology.md` | Words the writer would otherwise get wrong; optional |

Each file is a database: a page of text in the user's backend, found by its
title, which is the file's name. `ntm-user:backend` says where each one lives,
as it does for every database. For a Linear user, each file is one Linear
document. A YAML file's text sits in one fenced `yaml` block in its document, so
a backend that stores markdown keeps it intact.

The run fetches the text from the backend and hands it to the picker, which
touches no backend.

The examples below are from `Casebook`, a made-up detective story.

## The root

The root is the theme's guide for the writer, read whole for every message. Its
parts are the same in every theme:

| Part         | What it holds                                                                |
| ------------ | ---------------------------------------------------------------------------- |
| `theme`      | The theme's name                                                             |
| `world`      | The theme's world, and where the user sits in it                             |
| `escalation` | How the theme reads a task that slipped, and how it escalates with each slip |
| `wins`       | How the theme marks a finished task, and a big win                           |
| `reminders`  | What each reminder is in the theme's world, by its name                      |
| `files`      | Every other file of the theme: what it holds, and how it is read             |

Each file in `files` is read one of three ways:

| `read`   | How                                                                                                      |
| -------- | -------------------------------------------------------------------------------------------------------- |
| `whole`  | The writer gets all of it, for every message: guidance, or the terminology file                          |
| `entry`  | The writer gets the file's and the kind's `about`, and the picked entry with only its drawn line or riff |
| `picker` | Only the picker reads it: the options file                                                               |

<!-- prettier-ignore -->
```yaml
theme: Casebook

world: >-
  A detective story set in a foggy city. The user is the client who hired the
  detective; each task is a case on the detective's desk.

escalation: >-
  A slipped task is a case going cold. One slip draws a raised eyebrow, three
  draw a lecture on neglect, five and the inspector starts asking questions.

wins: >-
  A finished task is a case closed, filed with quiet satisfaction. A big win
  gets the whole cast in the drawing room for the reveal.

reminders:
  weekly: The new case files land on the desk.
  morning: The detective reads the morning paper for clues to today's case.
  afternoon: The legwork, and whether anyone has left the house.
  evening: The drawing room at dusk, where the day's case is told.

files:
  Casebook-options.yaml:
    holds: What the theme offers the picker.
    read: picker
  Casebook-characters.yaml:
    holds: The people of the story, and lines any of them can say.
    read: entry
  Casebook-scenes.yaml:
    holds: Recurring scenes a message can be set in.
    read: entry
  Casebook-terminology.md:
    holds: The story's own words.
    read: whole
```

## Entry files

An entry file holds what a message can draw on. What kinds exist is up to the
theme: people who speak, recurring scenes, references, and so on. A file opens
with `about`, which tells the writer how to use an entry from it, then holds
each kind of entry under its own name. A kind may open with its own `about`,
which is never an entry.

Each entry is keyed by a slug, a short key such as `detective`, which the
options file uses to name it. Within a theme, the entries of a kind share their
keys, and their optional keys, when present, come in the same order. Key names
are the theme's own, except `about`, `lines`, `riffs` and `when`, which ntm
reads. Prose sits in `>-` folded text.

An entry may carry `lines` it quotes, and `riffs`. A riff is a `line` plus
either a `bend`, which says how to turn the line toward a task, or a `when`, for
a line that fits as it is on the occasions it names.

A group of lines kept for one occasion is an entry with that `when`, such as
`big_win` below.

<!-- prettier-ignore -->
```yaml
about: >-
  The people of the story. A picked character speaks the whole message, in
  their own manner, built on the line drawn from them.

characters:
  detective:
    name: The Detective
    manner: >-
      Calm and precise, faintly bored by the obvious. Names the clue before
      the culprit.
    lines:
      - The answer was on the table the whole time.
      - Nobody leaves this room until I have finished.
    riffs:
      - line: Every lie leaves a crumb.
        bend: >-
          Treat the slipped task as the crumb that gives away what the user
          did instead.
      - line: File it under closed.
        when: done

shared_lines:
  about: >-
    Lines any character can say.
  any_time:
    lines:
      - Somebody in this house is lying.
  big_win:
    when: big_win
    lines:
      - Gather everyone in the drawing room.
```

## `when`

An entry or riff that fits only some occasions says which with `when`: one
occasion, or a list of several, any of which fits. No `when` means any occasion.
The occasions are one fixed set:

| `when`      | The occasion                      |
| ----------- | --------------------------------- |
| `morning`   | The morning reminder              |
| `afternoon` | The afternoon reminder            |
| `evening`   | The evening reminder              |
| `weekly`    | The weekly planning message       |
| `slipped`   | A task in the message has slipped |
| `done`      | A task in the message got done    |
| `big_win`   | A big effort, as below            |

A big win is one of these: several tasks closed in one day that had been planned
across several days, a task with a big estimate finally closed, or a task that
slipped many times finally closed. An ordinary day of doing what was planned is
never a big win.

## The options file

The options file holds what the theme offers the picker, and the numbers the
nightly job computes. It is the only theme file the picker reads.

It holds one pool per kind of entry. A pool is keyed by its kind, names its
file, and lists the entries that can be picked, each by its slug, with its
`when` copied from the entry file.

A pool gives a hook, a speaker, or both. The hook is what a message is built on.
The speaker is who says the message.

<!-- prettier-ignore -->
```yaml
checksums:
  Casebook-characters.yaml: 9f86d081884c7d65...
  Casebook-scenes.yaml: 2c26b46b68ffc68f...

pools:
  characters:
    file: Casebook-characters.yaml
    gives: [hook, speaker]
    half_life_days: 3
    speaker_rate: 0.4
    entries:
      detective:
        weight: 1.0
        line_half_life_days: 9
        score: 0.2

  shared_lines:
    file: Casebook-characters.yaml
    gives: [hook]
    half_life_days: 5
    entries:
      any_time:
        weight: 1.0
        line_half_life_days: 4
        score: 0.0
      big_win:
        when: big_win
        weight: 0.5
        line_half_life_days: 30
        score: 0.0

  scenes:
    file: Casebook-scenes.yaml
    gives: [hook]
    half_life_days: 6
    entries:
      stakeout:
        weight: 1.0
        score: 0.1
```

The theme builder writes the pools and computes the first numbers. The nightly
job updates each `score` every night, and recomputes a file's other numbers when
its checksum differs. The picker's own reference, a later PR, defines how each
number is computed.

| Field                 | What it is                                                              |
| --------------------- | ----------------------------------------------------------------------- |
| `checksums`           | Each entry file's SHA-256, over its text as stored; shortened above     |
| `half_life_days`      | The days for a picked entry's rest to halve; per pool                   |
| `speaker_rate`        | How often a message names a speaker from this pool, from 0 to 1         |
| `weight`              | How likely the entry is to be picked, against every other hook entry    |
| `line_half_life_days` | The days for a used line's rest to halve; per entry with lines or riffs |
| `score`               | How well messages built on the entry landed, from `%Message-history`    |

An entry's line half-life comes from how many lines it has and how often it is
picked.

## The pick

For each message, the run hands the picker the options file's text, the recent
picks and the message's occasions. The recent picks come from
`%Message-history`, which records each message's hook, speaker and when it went
out, and will record the line drawn. The run works out the occasions: which
reminder this is, whether a task in it has slipped, whether one got done, and
whether it's a big win.

The picker keeps the entries whose `when` fits. Each message gets exactly one
hook, drawn from all the entries in hook pools together, each entry counting
once at its weight. An entry's score raises or lowers its chance, and an entry
picked recently is less likely while it rests.

When the picked entry holds lines or riffs, the run hands the picker that entry
from its entry file, and one line or riff is drawn from it, keeping only riffs
whose `when` fits. A recently used line rests the same way an entry does. That
line or riff is what the writer builds on.

Sometimes a speaker is added from a speaker pool, at its `speaker_rate`.

## The terminology file

An optional markdown file, read whole: only the words a writer would otherwise
not know or would misuse, each with what it means in the theme.
