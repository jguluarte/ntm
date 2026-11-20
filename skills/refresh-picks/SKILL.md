---
name: refresh-picks
user-invocable: false
description: >-
    Refreshes a theme's picks: draws 25 picks from its `%Theme-options` into
    `%Theme-picks`, which each message takes its pick from. For the weekly setup
    job, it first runs ntm:recalculate-theme-scores. Run by the weekly setup
    job, by ntm:style when the list runs out, and by ntm:theme-builder for the
    theme it built.
---

# ntm:refresh-picks

## Usage

```
/ntm:refresh-picks
```

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. The theme is the
one the run names, or else this week's theme, as `%Settings` names it.

For the weekly setup job, load `ntm:recalculate-theme-scores` and follow it
first, for last week's theme. Keep its lines for the result, and go on even when
it fails.

Then read this theme's `%Theme-options`, such as `Casebook-options.yaml`. When
there is none, the theme isn't built for the picker: end the run with
`Nothing to refresh: no <Theme>-options.yaml`.

## Refresh

### 1. Hand over the options file

When `ntm:recalculate-theme-scores` saved this theme's `%Theme-options`, its
file is already in the working folder. Otherwise, write the text of its `yaml`
block to a file named for its database, such as `Casebook-options.yaml`, in this
session's working folder, exactly as read, never from memory.

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

Save what the draw printed as the `yaml` block of this theme's `%Theme-picks`,
replacing the list there, or creating `%Theme-picks` when there is none.

## Result

For a job, return `Refreshed <Theme>-picks.yaml: 25 picks`. For the weekly setup
job, the lines of `ntm:recalculate-theme-scores` come first.

Any output from the draw other than the picks, or a Refresh step you can't do,
means it failed: save no picks, and end with the `Picker FAILED:` line it
printed, or else `Refresh-picks FAILED: <why>`. In chat, tell the user the same
in plain words.
