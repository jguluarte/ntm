---
name: refresh-picks
description: >-
    Refreshes a theme's picks: draws 25 picks from its `%Theme-options` into
    `%Theme-picks`, which each message takes its pick from. Run by the weekly
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

When `ntm:theme-builder` runs this skill, it already holds where the databases
go, and the theme is the one it built. Skip the ready-check.

Otherwise, run `/ntm:ready-check`, unless it already ran in this session. It
loads `ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the
run with its result line. The theme is this week's theme, as `%Settings` names
it.

Then read the theme's `%Theme-options`, such as `Casebook-options`. When there
is none, the theme isn't built for the picker: end the run with
`Nothing to refresh: no <Theme>-options`.

## Refresh

### 1. Hand over the options file

The picker reads the options file from a path and touches no backend, so hand it
over this way.

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

For a job, return `Refreshed <Theme>-picks: 25 picks`, such as
`Refreshed Casebook-picks: 25 picks`. When there's no `%Theme-options`,
`Nothing to refresh: no <Theme>-options`.

The picker needs Python 3 with PyYAML and jsonschema, and nothing guarantees
them where this runs: without them, it stops with a Python error. Any output
other than the list of picks, or a step you can't do, means the run failed: save
nothing, and end with the `Picker FAILED:` line it printed, or else
`Refresh-picks FAILED: <why>`, with the last line it printed or what you
couldn't do. In chat, tell the user the same in plain words.
