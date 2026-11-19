# The theme builder

## What it is for

`/ntm:theme-builder` builds a theme with the user: a world they enjoy, with
enough in it to keep their reminders changing for months. A theme is a set of
files named after it, added beside the user's other themes, never replacing one.
Setup runs it during onboarding, and the user runs it for each theme after that.

`references/theme-files.md` gives each file's shape.

## The example theme

`Casebook`, a made-up detective story, is the example in this doc, in
`references/theme-files.md` and in ntm's tests. It shows the shape of a theme's
files, and nothing more. The builder never builds `Casebook` or copies from it:
every theme comes from the user's own world. The skill says so wherever it shows
the example.

## The conversation

It opens with the intro text, then asks one question at a time in chat. A user
who already has a theme can start from it: the builder sorts it into the files
and builds what's missing with them.

| Stage      | What the user is asked                       | What gets written                              |
| ---------- | -------------------------------------------- | ---------------------------------------------- |
| 1. World   | Their world, where they sit, what hooks them | The root's `theme` and `world`                 |
| 2. Levels  | How it sounds when tasks slip, and get done  | `escalation`, `finishing_tasks`                |
| 3. Kinds   | Which kinds of material the world has        | The entry files, the pools, the root's `files` |
| 4. Entries | How involved they want to be, then entries   | Entries in their files and pools               |

Stage 1 also asks how the user's day maps onto their world, if it does at all,
and whether there is anything they don't want in it. The user decides what each
part of the day is or is not. Both answers go in the root's `world`.

Each stage saves its part, so each is a place to stop and come back.

## Kinds

A kind is one sort of material in the world. Each kind has its own pool in the
options file and its own name in an entry file; one entry file can hold several
kinds. No list of kinds is fixed: each theme's kinds come from its world.

The builder proposes kinds from the world, as the user describes it and as the
builder knows it, each with an `about` saying what an entry is and how a message
uses one, and the keys its entries share. The user keeps, renames or drops them.

Every message is built on two entries: a perspective and a reference. The
perspective is who or what tells the message: a speaker, or a piece of the world
that tells it, such as a scene. The reference is another piece of the world it
draws on. A kind's pool says which its entries can be. In `Casebook`, characters
are speakers, shared lines are references, and scenes can be either.

## Entries

The builder writes a few entries of each kind with the user. About 20 in all, an
estimate and not a rule, is more than a week of messages. Variety comes from how
many entries there are and how many ways each can be used: a running scene that
moves forward, or a riff that bends a line to the task, stretches across many
reminders. A world with little to draw on wears out sooner, and the builder says
so.

Every quote or line comes from the user: they say it, or confirm that one the
builder offers is true to their world. A user who wants less to do with it gets
entries offered a few at a time, for a yes or no on each.

## Levels

Two parts of the root have levels. `escalation` is how the theme sounds as a
task keeps slipping; `finishing_tasks` is how it marks finished tasks, up to a
big win. The builder asks how each should sound and how hard it goes, then names
each level in the theme's words and writes how it sounds. The user decides how
many levels each has.

Levels are words, not numbers. For each message, `ntm:style` judges which level
fits from the facts, against the ladder's own words.

## Switching it on

When the last stage is done, the recalculation, a script in `ntm:style`, works
out the options file's numbers from the entry files: each entry's weight, the
theme's speaker rate and each entry file's checksum. `ntm:refresh-picks` draws
the theme's first picks from those numbers. The builder creates the theme's
message history, adds its root to the end of All themes in `%Settings`, and
sends a test message in the new theme. The weekly setup job takes the user's
themes in turn.

No other theme is touched. When another theme already has the name, the user
picks another.

## What it costs

Building costs more, once per theme. Upkeep stays cheap: scripts do the math,
and the writer reads only the root, the files it lists as fully read, and the
files the two picked entries are in.
