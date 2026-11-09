---
name: style
description: >-
    Writes a message in the user's style, from the Style document on their todo
    list, and keeps Message history. Loaded by the messenger agent for every
    reminder, and run in chat when the user asks for a message in their style.
    Also revises the Style document with the user when they ask: "make it
    meaner", "softer", "shorter", "the reminders aren't landing" or "use my own
    persona".
---

# ntm:style

## Setup

Load `ntm-user:backend` to read the user's conventions: where the Style document
and Message history live, and how to read and write them. Read the Style
document, and `references/persona-contract.md` for what each part of it means
and its default when it's missing. If the Style document can't be read, write
the message plain.

## Usage

```
/ntm:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>
```

`<reminder>` is `morning`, `afternoon`, `evening`, `week` or `completed`, and
implies `--stay-fresh`. The tone is freeform.

## Writing

Rewrite the message in the user's register, from their Style document. For a
persona, its text is the style, and its `## For ntm` section maps this call onto
its own words. Hold to what the contract says `ntm:style` brings.

With `--stay-fresh`, read Message history. Keep lines fresh: avoid what recent
entries used. Let a slipping task climb: a carried-over task's earlier days are
the days before today whose entries name its id, and its level is the one the
Profile's Responding to procrastination section gives for that count (for a
persona, its own levels); any other task is on the first level. Then add one
entry, with today's date, the new line and the task ids it names, pruned to the
`Keep:` line in the database's frontmatter. When Message history is missing,
create it with this first content:

```
---
Keep: 60 entries or 8 weeks
---
```

With `--for`, end with a `Title:` line that says what the message is about in
the same style, never just the reminder's name.

## Revising

When the user asks to change their style, revise the Style document with them in
chat, to the persona contract. Show the part their request touches, propose the
change, and write it once they agree. Parts they don't name stay as they are.

- "Meaner" or "softer": the Register, and the Examples it touches.
- "Shorter": What gets you to read, and the Examples.
- "Not landing": What gets you to read, then Responding to procrastination.
- "Use my own persona": their text replaces the Profile, with a `## For ntm`
  section above it, as the contract's A persona says. Show them that section.

A persona is edited as they say and kept word for word otherwise. How hard it
goes is their call. When a request heads toward plain, offer a livelier register
first: plain is the last resort.

## Result

Only the message, plain text, and that `Title:` line. After a revision, say in a
line what changed.
