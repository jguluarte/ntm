---
name: configure-style
description: >-
    Builds or revises ntm-user:style, the skill that writes every reminder in
    the user's own register, with them in chat: plain, a theme they describe, or
    a persona skill they already have. Run when the user says "set up the
    style", "change how reminders talk to me", "make it meaner", "make it
    softer", "make it shorter", "the reminders aren't landing" or "use my own
    persona"; ntm:configure runs it as one of its parts.
---

# ntm:configure-style

`ntm-user:style` is the user's own skill: the messenger runs it for every
reminder. It has two halves: a Profile (who talks, what gets them to read, the
reminders of the day, the levels when something keeps slipping, motifs, off
limits, examples) and the procedure that writes a line from facts. This skill
writes it with the user in short rounds: you bring proposals, they react. Never
hand them a form.

Read `references/builder.md` once before starting: it holds the Profile's shape,
the questions for each section, the episode arc the reminders follow, and one
plain example. `ntm:settings` builds the skill around it (see Result).

This skill ships no persona and names no show, person or brand. The theme, the
reminders, the levels and their names are the user's, in their words.

## Usage

```
/ntm:configure-style [<persona skill text>]
```

Text after the name is a persona skill the user already has, pasted or attached
(or a Profile in the builder's shape from an earlier ntm-user); see User-defined
persona.

## Before you start

Load `ntm-user:style` by name.

- **Won't load:** a new style. Open with the three choices below.
- **Loads:** a re-run. Show the Profile section by section, ask what to change,
  and go to the section that owns it: "meaner" or "softer" is Register and the
  Examples for the levels it touches; "shorter" is What gets you to read and the
  Examples; "not landing" starts at What gets you to read, then When something
  keeps slipping. Sections they don't name stay as they are. A persona is edited
  as they say, verbatim otherwise.

When `ntm:configure` is running this skill, it says so; the result goes back to
it (see Result).

## Opening

One line, three choices, none favoured: plain; describe a theme; or hand me a
persona you already have. "Just remind me", or anything like it, is plain.

## Plain

Every section answered plainly, no persona:

- **Register:** `Plain.` and one sentence on manner (warm, dry, brisk), in their
  words, and whether swearing is fine (`Profanity: yes` or `no`).
- **What gets you to read:** offer the builder's list; write their answer in
  their words.
- **The reminders:** the defaults; nothing to ask.
- **When something keeps slipping:** offer the builder's list. One level is a
  complete answer ("same every day"). If they want a climb, they name each level
  and say after how many earlier days it starts. Write that number on every
  level after the first.
- **Motifs:** empty, or a few things from their own life, each a short name.
  Repeat limit: the default unless they say otherwise.
- **Off limits:** the fixed sentence; add anything they name.
- **Examples:** one per level and one for nothing open, showing the mechanism
  from What gets you to read at work.

## A theme

The user describes who is talking. Derive each section with them, in order, with
the builder's questions:

- **Register:** who is talking, what they sound like, what they never do; two or
  three sentences, and whether swearing is fine (`Profanity: yes` or `no`).
- **What gets you to read:** the builder's list; more than one can combine; with
  what it needs (what a serial is about).
- **The reminders:** what each of the five is in the theme's terms (the
  builder's The reminders section), using the thing they named as the analogy:
  what the morning is in that world, what the afternoon is, the evening, the
  week, the credits. Propose each as one line; they rename or cut.
- **When something keeps slipping:** their levels, in order, each with the name
  they give it and after how many earlier days it starts; then the climb rule in
  one line.
- **Motifs:** recurring bits from the theme's world, one per line, each a short
  name the message history records exactly, built with them as the builder's
  Motifs section says: ask what they like and use it as the analogy, prefer
  motifs that can be built on, and set the repeat limit from how much variety
  the list gives. They add, cut and replace.
- **Off limits:** the fixed sentence, plus whatever the theme must never joke
  about.
- **Examples:** one per level and one for nothing open. Task ids use Task prefix
  from Todo list in `ntm-user:settings`, or the prefix settled earlier in this
  conversation, or `ABC-12` style when that isn't configured yet. The tasks in
  them are ordinary household ones. Write them, read them back, revise: if they
  chose humor, until they laugh at least once; otherwise until each reads like
  something they'd open.

Take the theme as they describe it. Don't propose a named character, show,
person or brand. If they want directions, offer kinds of character in a line
each (a stern coach, a dry narrator, a game-show host), none of them named.

## User-defined persona

The user has a persona skill already (or a Profile from an earlier ntm-user):
text that says who talks, with rules, maybe recurring bits and example lines. It
becomes `ntm-user:style` as it is: the body stays unchanged, word for word, task
ids included. A pasted skill's own frontmatter is dropped; everything under it
is the body.

What the messenger needs from it is only the call `ntm:settings` names:
`/ntm-user:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>`,
returning the message with `Title: …` as its last line under `--for`. Read the
body for how it names these things (a `--reminder` flag, a `Subject:` line, its
own history) and write a short section, `## For ntm`, that goes above the body
and says, in a line each, how the messenger's call maps onto the persona's own
words: what `--for <reminder>` means to it, that `Title:` is its last line (in
place of whatever it calls it; when the persona has no subject line of its own,
the section gives it the Title line rule from `ntm:settings`, so the title is
written with the message as part of its theme), that `--stay-fresh` is its
freshness mechanism, and that its history is the message history database (see
Databases in `ntm:conventions`; when the persona names a history of its own, the
section says to use that one). Show them the section; they confirm. Nothing else
is added or filled in: the persona's own levels, profanity and motifs stand.

## Result

For plain and a theme: the Profile, in the builder's shape, headings as given.
For a persona: the `## For ntm` section and the unchanged body. Show it and take
one round of corrections: they say what's off, you fix it.

Then:

- Run by `ntm:configure`: return it to `configure`; it packages once at the end.
- Run on its own: load `ntm:settings` and follow its "Regenerating
  `ntm-user.plugin`" section with it as the changed part.

Nothing is written anywhere else; the style lives only in `ntm-user`.
