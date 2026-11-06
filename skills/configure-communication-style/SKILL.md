---
name: configure-communication-style
description: Builds or revises the user's style profile (ntm-user:style), which ntm:style-message writes every reminder from, with them in chat: plain, a theme they describe, or a profile they already have. Run when the user says "set up the style", "change how reminders talk to me", "make it meaner", "make it softer", "make it shorter", "the reminders aren't landing" or "use my own profile"; ntm:configure runs it as one of its parts.
---

# ntm:configure-communication-style

The profile is `ntm-user:style`: a `Profanity:` line, then Register, What gets you to read, When something keeps slipping, Motifs, Off limits and Examples. `ntm:style-message` reads it for every reminder. This skill writes it with the user in short rounds: you bring proposals, they react. Never hand them a form.

Read `references/builder.md` once before starting: it holds the shape, the questions for each section, and one plain example.

This skill ships no persona and names no show, person or brand. The theme, the levels and their names are the user's, in their words.

## Usage

```
/ntm:configure-communication-style [<profile or skill text>]
```

Text after the name is a profile or a persona skill the user already has, pasted or attached; see Handed in.

## Before you start

Load `ntm-user:style` by name.

- **Won't load:** a new profile. Open with the three choices below.
- **Loads:** a re-run. Show it section by section, ask what to change, and go to the section that owns it: "meaner" or "softer" is Register and the Examples for the levels it touches; "shorter" is What gets you to read and the Examples; "not landing" starts at What gets you to read, then When something keeps slipping. Sections they don't name stay as they are.

When `ntm:configure` is running this skill, it says so; the body goes back to it (see Result).

## Opening

One line, three choices, none favoured: plain; describe a theme; or hand me a profile you already have. "Just remind me", or anything like it, is plain.

## Plain

Every section answered plainly, no persona:

- **Register:** `Plain.` and one sentence on manner (warm, dry, brisk), in their words. Ask about profanity: `yes` or `no`.
- **What gets you to read:** offer the builder's list; write their answer in their words.
- **When something keeps slipping:** offer the builder's list. One level is a complete answer ("same every day"). If they want a climb, they name each level and say after how many earlier days it starts. Write that number on every level after the first: a ticket's level is the last one whose number its count has reached, and count 0 is always the first level.
- **Motifs:** empty, or a few things from their own life, each a short name. Repeat limit: the default unless they say otherwise.
- **Off limits:** the fixed set; add anything they name.
- **Examples:** one per level and one for nothing open, showing the mechanism from What gets you to read at work.

## A theme

The user describes who is talking. Derive each section with them, in order, with the builder's questions:

- **Register:** who is talking, what they sound like, what they never do; two or three sentences. Profanity: `yes` or `no`.
- **What gets you to read:** the builder's list; more than one can combine; with what it needs (what a serial is about).
- **When something keeps slipping:** their levels, in order, each with the name they give it and after how many earlier days it starts. The first level is the everyday one (count 0); every level after it carries its number. Then the climb rule in one line, such as "harder each day a ticket carries over, back to the first level once it closes".
- **Motifs:** recurring bits from the theme's world, one per line, each a short name the message history records exactly. Propose a list; they add, cut and replace. The repeat limit, or the default.
- **Off limits:** the fixed set, plus whatever the theme must never joke about.
- **Examples:** one per level and one for nothing open. Ticket ids use Ticket prefix from Board in your settings (`ntm-user:settings`), or the prefix settled earlier in this conversation, or `ABC-12` style when that isn't configured yet. The tasks in them are ordinary household ones. Write them, read them back, revise: if they chose humor, until they laugh at least once; otherwise until each reads like something they'd open.

Take the theme as they describe it. Don't propose a named character, show, person or brand. If they want directions, offer kinds of character in a line each (a stern coach, a dry narrator, a game-show host), none of them named.

## Handed in

The user has a profile or a persona skill already: text that says who talks, with rules, maybe a list of recurring bits and example lines. Its body stays unchanged, word for word, ticket ids included. A pasted skill's own frontmatter is dropped; everything under it is the body. It gets the frontmatter and opening line the template gives every style; `ntm:settings` applies those. Fill nothing in from it: `ntm:style-message` reads what's there, and a section it lacks means its default. The defaults: Register, the whole profile as given; What gets you to read, the examples show it; Motifs, none; Off limits, the fixed set; Examples, the body's own.

Ask two things, in one round, and a third when it applies. Profanity: propose `yes` when the body's own lines swear, `no` otherwise; they confirm. Then: what should happen when something keeps slipping? And when the body keeps its own list of recurring bits (themes, references, running jokes) under a heading of its own, `ntm:style-message` won't find it there, since it reads Motifs by heading; so propose that list as the Motifs. Write `Profanity: <answer>` as the first line, then the `## When something keeps slipping` section, then, if they took the motifs, a `## Motifs` section with the list copied line for line, then the unchanged body (the builder's order). The levels section is in the builder's shape: named levels in order, the number (after how many earlier days it starts) on every level after the first, and the climb rule.

When the body groups its examples under headings (light, escalated, harsh, say), propose those groups as the levels, in that order: the first as the everyday one, the second after 1 earlier day, each further one a day later. Propose "harder each day a ticket carries over, back to the first level once it closes" as the climb rule. The user confirms or edits. Those groups are then the levels `ntm:style-message` uses.

## Result

The `ntm-user:style` body, in the builder's shape, headings as given (a handed-in body as Handed in says). Show it and take one round of corrections: they say what's off, you fix it.

Then:

- Run by `ntm:configure`: return the body to it; it packages once at the end.
- Run on its own: load `ntm:settings` and follow its "Regenerating `ntm-user.plugin`" section with the body as the changed part.

Nothing is written anywhere else; the profile lives only in `ntm-user`.
