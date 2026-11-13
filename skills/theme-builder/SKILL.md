---
name: theme-builder
description: >-
    Builds the user's theme, the `%Theme` every reminder is written in, with
    them in chat, one part at a time. Run by setup during onboarding, or by the
    user to build a new theme or rebuild theirs ("build me a new theme", "start
    my theme over", "switch my reminders to a different show").
---

# ntm:theme-builder

The theme is what ntm writes every reminder in, so the user keeps reading them.
This skill builds it with them, one part at a time, and saves it as `%Theme`.

## Usage

```
/ntm:theme-builder
```

## Setup

When `ntm:setup` runs this skill, it already holds where their databases go and
the `%Theme` name they confirmed. Go to step 1.

Otherwise, run `/ntm:ready-check`, unless it already ran in this session. It
loads `ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the
run with its result line.

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

Build the theme with them as
`${CLAUDE_PLUGIN_ROOT}/skills/theme-builder/references/theme.md` says: from the
parts it describes, or from a theme they already have.

### 3. Save `%Theme`

Save their theme in the parts the guide describes: during setup, create the
`%Theme` database; otherwise, replace their `%Theme` where `ntm-user:backend`
says it lives. Each part holds what you built with them, never the guide's own
text: How to connect this theme to ntm's flow holds what their week, morning,
afternoon and evening are in their theme.

## Result

Tell the user in a line that their theme is saved, and where `%Theme` lives.
