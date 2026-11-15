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
theme's files, and nothing more. Never build `Casebook` or copy from it: every
theme comes from the user's own world.

## Usage

```
/ntm:theme-builder
```

## Setup

When `ntm:setup` runs this skill, it already holds where their databases go. Go
to step 1.

Otherwise, run `/ntm:ready-check`, unless it already ran in this session. It
loads `ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the
run with its result line.

A `<Theme>.yaml` in their backend that All themes, in `%Settings`, doesn't list
is an unfinished theme. Offer to pick it up after its last saved stage, judged
from what its files hold; on a no, start a new one.

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

### 3. Switch it on

Once the last stage is done, create the theme's `%Message-history` from its
template,
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/databases/message-history.md`,
named after the theme, such as `Casebook-message-history`, beside its files.

Then add the theme's root to the end of All themes, in the Themes part of
`%Settings`, or where the user asks for it. When it's their first theme, it is
also This week's theme. The weekly setup job takes their themes in turn.

## Result

Tell the user in a line that their theme is switched on, and where its files
live.
