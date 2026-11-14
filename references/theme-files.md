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

## A theme's files

A theme named `<Theme>` is a set of files, each named after it, so a theme's
files sort together:

| File                  | What it is                                           | Format   |
| --------------------- | ---------------------------------------------------- | -------- |
| `<Theme>`             | The root: the writer's guide, and the list of files  | YAML     |
| `<Theme>-options`     | What the picker picks from, and its numbers          | YAML     |
| `<Theme>-<kind>`      | An entry file: one or more kinds of entry            | YAML     |
| `<Theme>-terminology` | Words the writer would otherwise get wrong; optional | Markdown |

Each file is a database: a page of text in the user's backend, found by its
title, which is the file's name. `ntm-user:backend` says where each one lives,
as it does for every database. For a Linear user, each file is one Linear
document.

The examples below are from `Casebook`, a made-up detective story.

## The root

The root is the theme's guide for the writer, read whole for every message.

| Part        | What it holds                                                          |
| ----------- | ---------------------------------------------------------------------- |
| `theme`     | The theme's name                                                       |
| `world`     | The theme's world, and where the user sits in it                       |
| `slipped`   | How the theme reads a task that slipped, and how much harder each slip |
| `wins`      | How the theme marks a finished task, and a big win                     |
| `reminders` | What each reminder is in the theme's world, by its name                |
| `files`     | Every other file of the theme: what it holds, and how it is read       |

Each file in `files` is read one of three ways:

| `read`   | How                                                                             |
| -------- | ------------------------------------------------------------------------------- |
| `whole`  | The writer gets all of it, for every message: guidance, or the terminology file |
| `entry`  | The writer gets only the entry the picker picked from it                        |
| `picker` | Only the picker reads it: the options file                                      |

<!-- prettier-ignore -->
```yaml
theme: Casebook

world: >-
  A detective story set in a foggy city. The user is the client who hired the
  detective; each task is a case on the detective's desk.

slipped: >-
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
  Casebook-options:
    holds: What the picker picks from for each message.
    read: picker
  Casebook-characters:
    holds: The people of the story, their manner and their lines.
    read: entry
  Casebook-scenes:
    holds: Recurring scenes a message can be set in.
    read: entry
  Casebook-terminology:
    holds: The story's own words.
    read: whole
```

## Entry files

An entry file holds what a message can draw on. What kinds exist is up to the
theme: people who speak, recurring scenes, references, and so on. A file opens
with `about`, which tells the writer how to use an entry from it, then holds
each kind of entry under its own name.

Each entry is keyed by a short slug, which the options file uses to name it.
Within a theme, every entry of a kind has the same keys in the same order. The
key names are the theme's own; prose sits in `>-` folded text.

An entry may carry lines it quotes, and riffs. A riff is a `line` plus either a
`bend`, which says how to turn the line toward a task, or a `when`, for a line
that fits as it is on the occasions it names.

<!-- prettier-ignore -->
```yaml
about: >-
  The people of the story. The picked character speaks the whole message, in
  their own manner: their lines are theirs to quote, and their riffs to bend
  toward the task.

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
        when: closed
```

## `when`

An entry or riff that fits only some occasions says which with `when`: one
occasion, or a list of several, any of which fits. No `when` means any occasion.
The occasions are one fixed set, which the picker understands:

| `when`      | The occasion                       |
| ----------- | ---------------------------------- |
| `morning`   | The morning reminder               |
| `afternoon` | The afternoon reminder             |
| `evening`   | The evening reminder               |
| `weekly`    | The weekly planning message        |
| `slipped`   | A task in the message has slipped  |
| `closed`    | A task in the message got finished |
| `big_win`   | A big effort, as below             |

A big win is one of these: several tasks closed in one day that had been planned
across several days, a task with a big estimate finally closed, or a task that
slipped many times finally closed. An ordinary day of doing what was planned is
never a big win.

## The options file

The options file is the only file the picker reads, so everything it needs is
there. It holds one pool per entry file: the entries that can be picked from
that file, each by its slug, with its `when` copied from the entry.

A pool gives a hook, a speaker, or both. The hook is what a message is built
around: a scene, a reference, a line. The speaker is who says the message.

<!-- prettier-ignore -->
```yaml
checksum: 5d41402abc4b

pools:
  Casebook-characters:
    gives: [hook, speaker]
    rest_days: 3
    speaker_rate: 0.4
    entries:
      detective:
        weight: 1.0
      sidekick:
        weight: 0.8

  Casebook-scenes:
    gives: [hook]
    rest_days: 6
    entries:
      stakeout:
        weight: 1.0
      the_reveal:
        when: big_win
        weight: 1.0
```

The theme builder writes the pools and computes the numbers up front. The
nightly job then recomputes the numbers, only when the checksum shows the entry
files changed:

| Field          | What it is                                                           |
| -------------- | -------------------------------------------------------------------- |
| `checksum`     | A checksum of the entry files the numbers were computed from         |
| `rest_days`    | How long a picked entry from this pool rests, in days                |
| `speaker_rate` | How often a message names a speaker from this pool, from 0 to 1      |
| `weight`       | How likely the entry is to be picked, against the others in its pool |

A resting entry is less likely to be picked. The difference halves every
`rest_days` days, so a rest fades over time.

## The terminology file

An optional markdown file, read whole: only the words a writer would otherwise
not know or would misuse, each with what it means in the theme.

## Several themes

A user can have more than one theme. `%Settings` lists each one by its root
under Themes, and names this week's theme. Everything picked in a week comes
from this week's theme. Each week the weekly job moves to the next theme in the
list, going through every theme before any repeats. With one theme, it is always
that one.
