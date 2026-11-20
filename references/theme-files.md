# Theme files

A theme is what ntm writes every reminder in: a world the user enjoys, with
enough material to keep each message different. A script, the picker, draws what
each message uses from it, so a theme is data in the shapes below.

## A theme's files

A theme named `<Theme>` is a set of files, each named after it, so a theme's
files sort together:

| File                         | What it is                                             |
| ---------------------------- | ------------------------------------------------------ |
| `<Theme>.yaml`               | The root: the writer's guide, and the list of files    |
| `<Theme>-options.yaml`       | What the theme offers the picker, and its numbers      |
| `<Theme>-<descriptor>.yaml`  | An entry file, named for what it holds, such as scenes |
| `<Theme>-terminology.md`     | Words the writer would otherwise get wrong; optional   |
| `<Theme>-message-history.md` | Each message sent in the theme, and how it landed      |
| `<Theme>-picks.yaml`         | The next picks, drawn by `ntm:refresh-picks`           |

Each file is a database, titled with its file name, such as
`Casebook-options.yaml`. A theme's name is its root's title without `.yaml`:
`Casebook`. A YAML file's text sits in one fenced `yaml` block.

The examples below are from `Casebook`, a made-up detective story.

## The root

The root is the theme's guide for the writer, read whole for every message. Its
parts are the same in every theme:

| Part              | What it holds                                                                |
| ----------------- | ---------------------------------------------------------------------------- |
| `theme`           | The theme's name                                                             |
| `world`           | The theme's world, and where the user sits in it                             |
| `escalation`      | How the theme reads a task that slipped, and how it escalates with each slip |
| `finishing_tasks` | How the theme marks a finished task, up to a big win                         |
| `files`           | Every other file of the theme, grouped by how the writer gets data from it   |

`escalation` and `finishing_tasks` each hold levels from the first up, each
keyed by its name in the theme's words and saying how it sounds. One paragraph
may stand in for the levels.

A win is any of these: more tasks finished than planned this week, a task
finished after slipping for days, or a task judged big or hard by the run that
sends the message. A big win is a whole project finished: the project itself
closes as done.

`files` has three groups. Under each, a file's full name maps to a line or two
on what it holds.

| Group            | What the writer gets                                                                            |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| `by_entry`       | All of it, when a picked entry is in it or its line names the message's `finishing_tasks` level |
| `fully_read`     | All of it, for every message: guidance, or the terminology file                                 |
| `for_the_picker` | Each pool's `file`, to find the picked entries: the options file                                |

<!-- prettier-ignore -->
```yaml
theme: Casebook

world: >-
  A detective story set in a foggy city. The user is the client who hired the
  detective; each task is a case on the detective's desk.

escalation:
  fresh_case: >-
    Nothing has slipped. The detective is dry and curious.
  going_cold: >-
    One slip. A raised eyebrow and a remark about cold trails.
  cold_case: >-
    Two slips. A slow lecture on neglect.
  inspector_calls: >-
    It keeps slipping. The inspector starts asking the user questions.

finishing_tasks:
  case_closed: >-
    A finished task, filed with quiet satisfaction.
  breakthrough: >-
    A win. The detective allows a rare smile.
  the_reveal: >-
    A big win. The whole cast gathers in the drawing room for the reveal.

files:
  by_entry:
    Casebook-characters.yaml: >-
      The people of the story, and lines any of them can say.

    Casebook-scenes.yaml: >-
      Recurring scenes a message can be set in.

  fully_read:
    Casebook-terminology.md: >-
      The story's own words.

  for_the_picker:
    Casebook-options.yaml: >-
      What the theme offers the picker.
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
are the theme's own, except `about`, `lines`, `riffs`, `line` and `bend`, which
ntm reads. Prose sits in `>-` folded text.

An entry may carry `lines` it quotes, and `riffs`. A riff is a `line` plus a
`bend`, which says how to turn the line toward a task.

A theme may set entries aside for one of its `finishing_tasks` levels, keyed by
the level's name: a kind of that name, or an entry of that name within a kind.
Each has an `about` saying when it fits. A file that holds them names the level
in its line in the root's `files`.

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
      - File it under closed.
    riffs:
      - line: Every lie leaves a crumb.
        bend: >-
          Treat the slipped task as the crumb that gives away what the user
          did instead.

shared_lines:
  about: >-
    Lines any character can say.
  any_time:
    lines:
      - Somebody in this house is lying.
```

## The options file

The options file holds what the theme offers the picker, and the numbers the
picker draws by. It is the only theme file the picker reads.

It holds one pool per kind of entry. A pool is keyed by its kind, names its
file, and lists the entries that can be picked, each by its slug.

A pool's `roles` say what its entries can be drawn as: a perspective, a
reference, a speaker, or more than one. The perspective is usually a speaker,
who says the message, and sometimes a piece of the world that carries one, such
as a scene. A reference is any piece of the world other than a speaker. A
speaker is only ever drawn as the perspective.

<!-- prettier-ignore -->
```yaml
checksums:
  Casebook-characters.yaml: 9f86d081884c7d65...
  Casebook-scenes.yaml: 2c26b46b68ffc68f...

speaker_rate: 0.4

pools:
  characters:
    file: Casebook-characters.yaml
    roles: [speaker]
    entries:
      detective:
        weight: 0.57
        score: 0.2

  shared_lines:
    file: Casebook-characters.yaml
    roles: [reference]
    entries:
      any_time:
        weight: 0.25
        score: 0.0

  scenes:
    file: Casebook-scenes.yaml
    roles: [perspective, reference]
    entries:
      stakeout:
        weight: 1.0
        score: 0.1
```

The recalculation, a script, computes every number here. An entry without a
`weight` weighs 1, and one without a `score` scores 0.

| Field          | What it is                                                                           |
| -------------- | ------------------------------------------------------------------------------------ |
| `checksums`    | Each entry file's SHA-256, over its text as stored; shortened above                  |
| `speaker_rate` | How often the perspective is a speaker, from 0 to 1; one for the theme               |
| `weight`       | How likely the entry is to be drawn: 1 without lines or riffs, less the fewer it has |
| `score`        | How well messages built on the entry landed, from the message history                |

## The terminology file

An optional markdown file, read whole: only the words a writer would otherwise
not know or would misuse, each with what it means in the theme.

## The message history

An entry for each message sent in the theme, and how it landed. The root's
`files` leaves it out.
