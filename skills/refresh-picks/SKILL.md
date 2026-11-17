---
name: refresh-picks
description: >-
    Refreshes the week's picks for this week's theme: runs the recalculation on
    its `%Theme-options`, then draws 25 picks into `%Theme-picks`, which each
    message takes its pick from. Run by the weekly setup job.
---

# ntm:refresh-picks

## Usage

```
/ntm:refresh-picks
```

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line. Then read `%Theme-options`: this week's theme's, as
`%Settings` names it, such as `Casebook-options`. When there is none, the theme
isn't built for the picker: end the run with
`Nothing to refresh: no <Theme>-options`.

## Refresh

### 1. Hand over the files

The scripts read files from a path and touch no backend, so hand the theme's
files over this way.

Take the text of `%Theme-options`' `yaml` block. Write that text to a file named
for the theme, such as `Casebook-options.yaml`, in this session's working
folder, exactly as read: never retype it from memory or summarize it.

Each pool in it names an entry file under `file:`, such as
`Casebook-characters.yaml`. Read each of those theme files, and write its `yaml`
block the same way, to a file of the name the pool gives, beside the options
file.

### 2. Recalculate

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/recalculate.py start \
    --options <the options file> <each entry file>
```

It rewrites the options file and prints `saved: <the options file>`.

### 3. Draw the week's picks

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/pick_list.py draw \
    --options <the options file> --count 25
```

It prints the picks as a YAML list, in the order drawn:

```
- perspective: characters/detective
  reference: scenes/stakeout
- perspective: scenes/stakeout
  reference: shared_lines/any_time
```

### 4. Save

Save what the draw printed as the `yaml` block of `%Theme-picks`, replacing the
list there, or creating `%Theme-picks` when there is none.

Read the options file. When its text differs from the `yaml` block of
`%Theme-options`, save it there.

## Result

For a job, return `Refreshed <Theme>-picks: 25 picks`, such as
`Refreshed Casebook-picks: 25 picks`. When there's no `%Theme-options`,
`Nothing to refresh: no <Theme>-options`.

The scripts need Python 3 with PyYAML and jsonschema, and nothing guarantees
them where this runs: without them, a script stops with a Python error. Any
output other than the `saved:` line and the list of picks, or a step you can't
do, means the run failed: save nothing, and end with the `Recalculation FAILED:`
or `Picker FAILED:` line the script printed, or else
`Refresh-picks FAILED: <why>`, with the last line it printed or what you
couldn't do. In chat, tell the user the same in plain words.
