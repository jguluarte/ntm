# Building the theme

The theme is what ntm writes every reminder in, so the user keeps reading them.
Build it with them one stage at a time, from what they picked. Each section
below is a stage: what to ask them, and what it writes in the theme's files. For
a theme they already have, sort it into these files and build what's missing
with them.

`${CLAUDE_PLUGIN_ROOT}/references/theme-files.md` gives each file's shape, with
`Casebook`, a made-up detective story, as its example. `Casebook` shows the
shape and nothing more: build from the user's own world, and never build
`Casebook` or copy from it.

A theme should be something with enough breadth and material to pull from that
it can create sufficient variation, so it won't become repetitive. A show is a
good option, as you can pull from its entire canon. While you could use a single
character, it will take more effort to ensure an adequate dataset to avoid
repetition. Build every part with several options to draw from, so reminders
keep changing. A world with little to draw on may not work well for them; a
better defined one holds up longer, so tell them when theirs is thin.

## The world

Their world, where they sit in it, and who talks to them. Then what makes them
open a reminder: a joke, a jab, a running bit, a story that picks up where
yesterday left off. Several can combine. A world they invent has nothing to look
up: write all of it with them.

Ask how their day maps onto the world, if it does at all: the weekly plan, and
the morning, afternoon and evening reminders. The intro's detective story is one
way. The user decides what each part of the day is or is not. Ask too whether
there is anything they don't want in it.

Write the theme's name as the root's `theme`. Write the rest in its `world`: the
world and where they sit in it, what hooks them, how their day maps onto it,
what stays out, and who tells the story when no one in particular speaks.

## The levels

The different ways the theme talks to them: an everyday one, how it snaps back
when a task keeps getting put off, and how it celebrates when it's earned.
Shame, a cheerleader, a demon that stalks them, jabs that sharpen each time:
whatever gets them moving. Talk through with them what they want, then decide
what fits their theme. Ask how hard each level goes: swearing, roasting and
mockery are all welcome when they want them. Push for vivid.

The root's `escalation` has four levels, and its `wins` three, in this order.
Name each level in the theme's words, as its key, and write how it sounds.

| Level | `escalation`                                             | `wins`                                        |
| ----- | -------------------------------------------------------- | --------------------------------------------- |
| 1st   | Where every message starts                               | Any finished task                             |
| 2nd   | Now and then with no slip, so a good run still gets read | A big day or week, or a big or hard task done |
| 3rd   | A task has slipped                                       | Something truly shocking, and rare            |
| 4th   | A task has kept slipping                                 |                                               |

## The kinds

A kind is one sort of material in their world. Each kind has its own pool in the
options file and its own name in an entry file; one entry file can hold several
kinds. No list of kinds is fixed: derive them from the world's own material, as
the user describes it and as you know it. Most worlds have actors: people who
talk in a manner of their own. Two more kinds turn up in many worlds: recurring
scenes a message can be set in, and single moments to call back to.

Propose kinds, each with an `about` saying what an entry is and how a message
uses one, and the keys its entries share. The user keeps, renames or drops them.

An entry that talks in a manner of its own can be a `speaker`; one with
something to build on, such as lines, a scene or a moment, can be a `hook`.
Actors are usually both.

Write each entry file, `<Theme>-<descriptor>.yaml`, with its `about` and each
kind's `about`. In the options file, `<Theme>-options.yaml`, give each kind a
pool with its `file` and `roles`. List the entry files under the root's `files`,
in `by_entry`, and the options file in `for_the_picker`.

## The entries

Ask how involved they would like to be with their theme's content. It is likely
fine to make changes over time if they don't want to dedicate time today.

Write a few entries of each kind with them; about 20 in all, an estimate and not
a rule, is more than a week of messages. Variety comes from how many entries
there are and how many ways each one can be used: a running scene that moves
forward, or a riff that bends a line to the task, stretches across many
reminders.

Each entry follows its kind's keys. Every quote or line comes from the user:
they say it, or confirm that one you offer is true to their world. An entry that
fits only some messages gets a `when`, from how their day maps onto the world.
Keep a few entries for `big_win`, so a big win has material of its own.

Add each entry to its entry file, under its kind, and to the kind's pool in the
options file, by its slug, with its `when` copied.

## Sample messages

A few sample messages for each escalation level, and a few for each level of
wins, with tasks like theirs, each built on one of their entries. Read them back
and revise how each level sounds until they smile.
