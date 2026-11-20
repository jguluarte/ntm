---
name: theme-builder
description: >-
    Builds a theme with the user in chat, one stage at a time: a world they
    enjoy, saved as a set of files every reminder can be written in, and added
    to their themes. Run by setup during onboarding, or by the user to build
    another theme ("build me a new theme", "add a theme from another show").
---

# ntm:theme-builder

The theme is what ntm writes every reminder in, so the user keeps reading them.
This skill builds one with them, one stage at a time, as a set of files named
after it, and adds it beside their other themes.

`Casebook`, a made-up detective story, is the example in this skill and in
`${CLAUDE_PLUGIN_ROOT}/references/theme-files.md`. It shows the shape of a
theme's files, and nothing more. Never build `Casebook` or copy from it.

## Usage

```
/ntm:theme-builder
```

## Setup

When `ntm:setup` runs this skill, it already holds where their databases go:
skip the ready-check, here and in `ntm:refresh-picks`. Otherwise, run
`/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

A theme's root is a YAML database with a `theme` part. One that All themes, in
`%Settings`, doesn't list is unfinished: offer to pick it up where its files
leave off.

## Building the theme

### 1. Introduce the theme

Send this text as written, in one message. Then add anything else you think is
important for them to know before they pick one, based on what you know about
your user from your memories about them.

> The theme is what your reminders are created with, that way messages are
> always unique and ultimately bring you joy. This is how reminders are never
> exactly the same, so it doesn't become noise you ignore.
>
> Consider something you enjoy, like a book or maybe a show. Reality competition
> shows in particular typically follow a kind of formula that allows ntm to
> introduce a wider variety of reminders. If you decide to schedule things a
> week at a time, then the weekly plan is sort of like the season preview. Each
> day has a preview of what is to come (sometimes a quick synopsis of
> yesterday), the afternoon is whatever would normally happen in the first half
> of the episode, and the evening is how an episode ends. This pattern is
> something an LLM is particularly good at following.
>
> It's now up to you to get creative, pick something that brings you happiness
> and will make you smile. When you're slacking off, imagine how they could
> motivate you? Do you need to be shamed? Do you need a cheerleader? Do you need
> a demon to stalk you? The world is your oyster - make it so!

### 2. Build it with them

Build the theme with them one stage at a time, as the theme guide,
`${CLAUDE_PLUGIN_ROOT}/skills/theme-builder/references/theme.md`, says: the
world, the levels, the kinds and the entries.

Save each stage's part in the theme's files, beside their other databases, as it
finishes, so a later chat picks it up. When another theme has the name they
pick, ask for another.

### 3. Work out its numbers

When this run wrote or changed the theme's files, run the recalculation, which
works out the numbers in `%Theme-options`: each entry's weight, the theme's
speaker rate and each entry file's checksum.

Write the text of the `yaml` block of `%Theme-options`, and of each entry file
its pools name, to a file named for its database, such as
`Casebook-options.yaml` and `Casebook-scenes.yaml`, in this session's working
folder, exactly as read, never from memory. Then run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/recalculate.py start \
    --options <the options file> <each entry file>
```

It writes the numbers into the options file and prints one line,
`saved: <the options file>`. Save that file's text, exactly as the script wrote
it, as the `yaml` block of `%Theme-options`.

Any other output, or a part of this you can't do, means it failed: tell the user
in a line that the theme's numbers weren't worked out, with what it printed or
why, and go on.

### 4. Draw its first picks

When step 3 passed, load `ntm:refresh-picks` and follow it for this theme. When
it ends with a failure line, tell the user in a line that the theme's picks
weren't drawn, with that line, and go on.

### 5. Switch it on

Create the theme's `%Message-history` from its template,
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/databases/message-history.md`,
named after the theme, such as `Casebook-message-history.md`, beside its files.

Then add the theme's root to the end of All themes, in the Themes part of
`%Settings`, or where the user asks for it. When it's their first theme, it is
also This week's theme.

### 6. Send a test message

When `ntm:setup` runs this skill, skip this step: its self-test sends the first
message. Otherwise, send one message as the core rules' Sending a message in the
user's style says, written in this theme in place of This week's theme. Its one
fact is that the theme, by its name, is built and switched on. Show the user any
`NOTIFY VIA FINAL REPLY` block it returns. When it isn't sent, tell the user in
a line, with what it returned, and go on: the theme stays on.

## Result

Tell the user in a line that their theme is switched on, and where its files
live.
