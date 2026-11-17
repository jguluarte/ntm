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

When `ntm:setup` runs this skill, it already holds where their databases go.
Skip the ready-check, and look for an unfinished theme.

Otherwise, run `/ntm:ready-check`, unless it already ran in this session. It
loads `ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the
run with its result line.

A theme's root in their backend, a YAML database whose text has a `theme` part,
is an unfinished theme when All themes, in `%Settings`, doesn't list it. Offer
to pick it up after its last saved stage, judged from what its files hold; on a
no, start a new one.

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

Build the theme with them as the theme guide,
`${CLAUDE_PLUGIN_ROOT}/skills/theme-builder/references/theme.md`, says: stage by
stage, or from a theme they already have.

Save each stage's part as it finishes, so a later chat picks it up instead of
starting over. Each file holds what you built with them, never the guide's own
text.

Each of the theme's files is a database in their backend, beside their other
databases, titled with its file name, such as `Casebook.yaml`. A YAML file's
text sits in one fenced `yaml` block. No other theme is touched: when another
theme already has the name they pick, ask them for another.

### 3. Work out its numbers

When this run wrote or changed the theme's files, run the recalculation, a
script in `ntm:style` that works out the numbers in the theme's options file:
each entry's weight, the theme's speaker rate, and each entry file's checksum.
It reads files from paths and touches no backend, and the theme's files live in
the user's backend, so hand them over this way.

Read `%Theme-options` and each entry file its pools name, and take the text of
each one's `yaml` block. Write each text to a file named for its database, such
as `Casebook-options.yaml` and `Casebook-scenes.yaml`, in this session's working
folder, exactly as read: never retype it from memory or summarize it. Then run
the recalculation on those files:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/recalculate.py start \
    --options <the options file> <each entry file>
```

It writes the numbers into the options file and prints one line,
`saved: <the options file>`. Save that file's text, exactly as the script wrote
it, as the `yaml` block of `%Theme-options`.

It needs Python 3 with PyYAML and jsonschema, and nothing guarantees them where
this runs: without them, the script stops with a Python error. Any other output,
or a part of this you can't do, means the recalculation failed. Its failure line
is the `Recalculation FAILED: <failure>: <why>` line it printed, or else
`Recalculation FAILED: <why>`, with the last line it printed or what you
couldn't do. When it fails, tell the user in a line that the theme's numbers
weren't worked out, with its failure line, and go on.

### 4. Draw its first picks

When step 3 passed, load `ntm:refresh-picks` and follow it for this theme, so
its `%Theme-picks` is drawn on the new numbers. When `ntm:setup` runs this
skill, skip `ntm:refresh-picks`'s ready-check too, as Setup says. When it ends
with a failure line, tell the user in a line that the theme's picks weren't
drawn, with that line, and go on.

### 5. Switch it on

Create the theme's `%Message-history` from its template,
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/databases/message-history.md`,
named after the theme, such as `Casebook-message-history.md`, beside its files.

Then add the theme's root to the end of All themes, in the Themes part of
`%Settings`, or where the user asks for it. When it's their first theme, it is
also This week's theme. The weekly setup job takes their themes in turn.

### 6. Send a test message

When `ntm:setup` runs this skill, skip this step: its self-test sends the first
message. Otherwise, send one message as the core rules' Sending a message in the
user's style says, written in this theme in place of This week's theme. Its one
fact is that the theme, by its name, is built and switched on. It's sent when
`ntm-user:notify` returns `Sent:`, or its `NOTIFY VIA FINAL REPLY` block, which
you show the user. On any other return, tell the user in a line that the test
message didn't go out, with what it returned, and go on: the theme stays on.

## Result

Tell the user in a line that their theme is switched on, and where its files
live.
