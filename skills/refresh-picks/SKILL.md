---
name: refresh-picks
description: >-
    Refreshes a theme's picks: draws 25 picks from its `%Theme-options` into
    `%Theme-picks`, which each message takes its pick from. For the weekly setup
    job, it first rates how the past week's messages landed. Run by the weekly
    setup job and by ntm:style when the list runs out, for this week's theme,
    and by ntm:theme-builder for the theme it built.
---

# ntm:refresh-picks

Run by the weekly setup job, by `ntm:style` when `%Theme-picks` runs out, and by
`ntm:theme-builder` for the theme it built.

## Usage

```
/ntm:refresh-picks
```

## Setup

Run `/ntm:ready-check` if needed (if it isn't already loaded in the context).
The theme is the one `ntm:theme-builder` built, when it runs this skill, or else
this week's theme, as `%Settings` names it.

Then read the theme's `%Theme-options`, such as `Casebook-options.yaml`. When
there is none, the theme isn't built for the picker: end the run with
`Nothing to refresh: no <Theme>-options.yaml`.

For the weekly setup job, rate the past week before the draw, as
`references/rating.md` says.

## Refresh

### 1. Hand over the options file

When the rating saved this theme's `%Theme-options`, its file is already in the
working folder: go on to the draw.

Otherwise, the picker reads the options file from a path and touches no backend,
so hand it over this way.

Take the text of `%Theme-options`' `yaml` block. Write that text to a file named
for the theme, such as `Casebook-options.yaml`, in this session's working
folder, exactly as read: never retype it from memory or summarize it.

### 2. Draw the week's picks

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/pick_list.py draw \
    --options <the file> --count 25
```

It prints the picks as a YAML list, in the order drawn:

```
- perspective: characters/detective
  reference: scenes/stakeout
- perspective: scenes/stakeout
  reference: shared_lines/any_time
```

### 3. Save

Save what the draw printed as the `yaml` block of `%Theme-picks`, replacing the
list there, or creating `%Theme-picks` when there is none.

## Result

For a job, return `Refreshed <Theme>-picks.yaml: 25 picks`, such as
`Refreshed Casebook-picks.yaml: 25 picks`. When there's no `%Theme-options`,
`Nothing to refresh: no <Theme>-options.yaml`.

For the weekly setup job, the rating's lines come first.

The picker needs Python 3 with PyYAML and jsonschema, and nothing guarantees
them where this runs: without them, it stops with a Python error. Any output
from the draw other than the list of picks, or a step of Refresh you can't do,
means the refresh failed: save no picks, and end with the `Picker FAILED:` line
it printed, or else `Refresh-picks FAILED: <why>`, with the last line it printed
or what you couldn't do. In chat, tell the user the same in plain words.
