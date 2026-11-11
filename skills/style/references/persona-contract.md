# Persona contract

The `%Style` document holds the user's persona: what `ntm:style` reads before it
writes a message. Setup's persona step writes it, and `ntm:style` revises it
with the user on request. This page says what the document must hold, what it
may hold, and what `ntm:style` does when a part is missing. `%Message-history`
is a database of its own, not part of the `%Style` document.

Required means setup and every revision write it. A run never stops over a
missing part: `ntm:style` falls back as each part says.

A `%Style` document has one of two shapes:

- **A Profile:** built with the user in setup, plain or from a theme.
- **A persona:** one the user already had, under a `## For ntm` section.

## A Profile

The headings below, exactly as written and in this order. Everything under a
heading is the user's, in their words. Setup writes every heading, even when its
section stays empty.

### Required

`### Register`: who is talking and how they talk to the user, including how they
snap back when something slides, how they celebrate a win, and what they would
never say. Two or three sentences; for plain, `Plain.` and one sentence on
manner. Without it, `ntm:style` writes the message plain.

Plain is the last resort: a plain reminder is easy to swipe away. Push for a
format the user already enjoys, such as a reality competition's judges, a
cooking contest host, a drill sergeant, a coach at halftime or a nature
documentary narrator. How hard it goes is the user's call: swearing, shade,
roasting, whatever they want.

### Optional

An empty or missing part means its default.

- `### What gets you to read`: what gets a reminder opened (brevity, humor, a
  running bit) and how long a message runs. Default: one or two plain sentences.
- `### The reminders`: what the morning, afternoon, evening, week and completed
  are in the theme's terms. Default: morning is the setup, afternoon the nudge,
  evening how the day ended, week the recap and what's coming, completed the
  credits.
- `### Responding to procrastination`: do you want the messages to respond
  differently when you're procrastinating certain tasks? How do you want that?
  Do you want escalating levels of shade? The levels in order, each with its
  name and after how many earlier days it starts, then the climb rule. Default:
  one level, the same every day.
- `### Motifs`: recurring bits from the theme's world or the user's life, a
  short name each, then a `Repeat limit:` line. Push for a few weeks' worth of
  variety. Default: no motifs, and a motif rests until most of the others have
  had a turn.
- `### Examples`: one per level and one for nothing open, with household tasks
  and ids like `ABC-12`. Default: none; the Register alone sets the energy.

## A persona

The user's persona text, word for word, task ids included; a pasted skill's
frontmatter is dropped. Its own rules, levels and motifs stand, and none of the
Profile's parts are asked of it.

Required: above the text, a `## For ntm` section that says, a line each, how
`ntm:style`'s call maps onto the persona's own words: what `--for <type>` means
to it, that `Title:` is its last line, that `--stay-fresh` is its freshness
rule, and that its history is `%Message-history`, each entry naming the task ids
its message names. Without it, the whole text still stands as the persona, its
levels and motifs included. `ntm:style` uses the Profile's defaults only where
the text has no words, such as the `Title:` line and the history entries.

## What `ntm:style` brings

These hold for every `%Style` document, so none states them:

- Facts stay exact: ids, titles, dates and counts as given, nothing added.
- A title is written with its message, in its theme, never the reminder's name.
- No joke shape, pun or opening from a line in `%Message-history`.
- Examples lend energy, never sentences.
