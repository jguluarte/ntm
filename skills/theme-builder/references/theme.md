# Building the theme

The theme is what ntm writes every reminder in, so the user keeps reading them.
Build it with them one stage at a time, from what they picked. Each section
below is a stage: what to ask them, and what it writes in the theme's files. For
a theme they already have, sort it into these files and build what's missing
with them.

`${CLAUDE_PLUGIN_ROOT}/references/theme-files.md` gives each file's shape.

A theme should be something with enough breadth and material to pull from that
it can create sufficient variation, so it won't become repetitive. A show is a
good option, as you can pull from its entire canon. While you could use a single
character, it will take more effort to ensure an adequate dataset to avoid
repetition. Build every part with several options to draw from, so reminders
keep changing. Tell them when their world is thin.

## The world

Their world, where they sit in it, and who talks to them. Then what makes them
open a reminder: a joke, a jab, a running bit, a story that picks up where
yesterday left off. Several can combine.

Ask how their day maps onto the world, if it does at all: the weekly plan, and
the morning, afternoon and evening reminders. The intro's example is one way.
The user decides what each part of the day is or is not. Ask too whether there
is anything they don't want in it.

Agree the theme's name with them, since it names each of the theme's files, and
write it as the root's `theme`. Write the rest in its `world`: the world and
where they sit in it, what hooks them, how their day maps onto it, what stays
out, and who tells the story when no one in particular speaks.

## The levels

The different ways the theme talks to them: an everyday one, how it snaps back
when a task keeps getting put off, and how it celebrates when it's earned.
Shame, a cheerleader, a demon that stalks them, jabs that sharpen each time:
whatever gets them moving. Talk through with them what they want, then decide
what fits their theme. Ask how hard each level goes: swearing, roasting and
mockery are all welcome when they want them. Push for vivid.

Write the levels in the root's `escalation` and `finishing_tasks`. The user
decides how many each has. Most themes start from these:

| Level | `escalation`                                             | `finishing_tasks`                             |
| ----- | -------------------------------------------------------- | --------------------------------------------- |
| 1st   | Where every message starts                               | Any finished task                             |
| 2nd   | Now and then with no slip, so a good run still gets read | A big day or week, or a big or hard task done |
| 3rd   | A task has slipped                                       | Something truly shocking, and rare            |
| 4th   | A task has kept slipping                                 |                                               |

## The kinds

Derive the theme's kinds from the world's own material, as the user describes it
and as you know it. Propose kinds, each with an `about` saying what an entry is
and how a message uses one, and the keys its entries share. The user keeps,
renames or drops them.

Write each entry file, a pool for each kind in the options file, and the root's
`files`.

## The entries

Ask the user how involved they would like to be with their theme's content. When
they want less of a part in it, offer entries a few at a time, for a yes or no
on each.

Write a few entries of each kind with them; about 20 in all, an estimate and not
a rule, is more than a week of messages. Variety comes from how many entries
there are and how many ways each one can be used: a running scene that moves
forward, or a riff that bends a line to the task, stretches across many
reminders.

Every quote or line comes from the user: they say it, or confirm that one you
offer is true to their world. Keep a few entries for `big_win`, so a big win has
material of its own. Give any other entry a `type` only when it truly belongs to
the reminder types or task outcomes it names; in a theme this small, most
entries have none.

Add each entry to its entry file and to its kind's pool in the options file.
