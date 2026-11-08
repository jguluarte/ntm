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

`ntm-user:style` is the user's own skill; the messenger runs it for every
reminder. It has two halves: the Profile, which holds what the user told you,
and the procedure, which writes each message from the Profile. You write the
Profile; `ntm:settings` builds the skill around it (see Result). Build it with
the user in short rounds: you propose, they react. Never hand them a form.

Read `references/builder.md` first: the Profile's shape, what each section means
and what to ask, how the day's reminders follow an episode, and a plain example.

Ship no persona and name no show, person or brand. The theme, the reminders, the
levels and their names are the user's, in their words.

## Usage

```
/ntm:configure-style [<persona skill text>]
```

Text after the name is a persona skill the user already has, pasted or attached,
or a Profile from an earlier ntm-user. See User-defined persona.

## Before you start

Load `ntm-user:style` by name. If it won't load, this is a new style: go to
Opening.

If it loads, show the Profile section by section and ask what to change. Start
at the section that owns the change:

- "meaner" or "softer": Register, and the Examples for the levels it touches
- "shorter": What gets you to read, and the Examples
- "not landing": What gets you to read, then When something keeps slipping

Leave sections they don't name as they are. Edit a persona as they say, word for
word otherwise.

If `ntm:configure` started this skill, it tells you; return the result to it
(see Result).

## Opening

Offer three choices in one line, none favoured: plain, a theme they describe, or
a persona they already have. "Just remind me", or anything like it, is plain.

## Plain or a theme

Go through the builder's sections in order, with its questions. Each section
says where plain and a theme differ.

For a theme, the user describes who is talking. Take it as they describe it, and
don't propose a named character, show, person or brand. If they want ideas,
offer kinds of character in a line each (a stern coach, a dry narrator, a
game-show host), none of them named.

## User-defined persona

The user's persona skill, or a Profile from an earlier ntm-user, becomes
`ntm-user:style` as it is: the body stays word for word, even the task ids in
its examples. Drop a pasted skill's own frontmatter; everything under it is the
body.

The messenger calls the style the way `ntm:settings` defines:

```
/ntm-user:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>
```

It returns the message; with `--for`, a `Title:` line comes last.

Above the body, write a short `## For ntm` section that maps this call onto the
persona's own words. Read the body for what it calls these things, such as a
`--reminder` flag, a `Subject:` line, or its own note of past messages. One line
each:

- what `--for <reminder>` means to it
- that `Title:` is its last line under `--for`, in place of whatever it calls it
    - If it has no subject line: give it the Title line rule from
      `ntm:settings`, so the title is written with the message, in its theme.
- that `--stay-fresh` is its freshness mechanism
- that its message history note is the one titled under Notes in
  `ntm-user:settings`
    - If the persona names its own note: the title in settings should be that
      one.

Show them the section; they confirm. Add nothing else: the persona's own levels,
profanity and motifs stand.

## Result

For plain or a theme, the Profile, in the shape `builder.md` gives. For a
persona, the `## For ntm` section above the unchanged body. Show it and take one
round of corrections.

Then:

- Run by `ntm:configure`: return it; `configure` packages once at the end.
- Run on its own: load `ntm:settings` and follow its "Regenerating
  `ntm-user.plugin`" section, with the style as the changed part.

The style lives only in `ntm-user`; write it nowhere else.
