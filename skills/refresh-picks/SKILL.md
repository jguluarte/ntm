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

## Rate the past week

Only when the weekly setup job runs this skill. The past week's messages went
out in last week's theme, the one This week's theme named before the job moved
it on: rate and adjust that theme, and draw for this week's. With one theme,
they're the same.

When the theme has no `%Message-history`, or no entry in it was sent in the last
seven days, there's nothing to rate: go on to Refresh.

A failure in step 1 or 2 ends this part: keep its failure line for the result,
and go on to Refresh.

### 1. Rate the week's messages

Read the theme's `%Message-history`. Rate each entry sent in the last seven days
that has `tasks` and no `verdict`.

The user acted on it when, since it was sent, they closed one of its tasks, or
moved or cleared its planned date. ntm carries and clears planned dates too, and
the task's `Planned date history` lists each date it slipped from: when that
lists the entry's `planned` date, ntm moved it, not the user.

The weekly setup job already looked up last week's closed tasks and the open
tasks planned in the past: use those. Look up only the tasks they don't cover,
and a task's `Planned date history` only when its date changed.

Write `acted` or `ignored` as the entry's `verdict`, and save
`%Message-history`. When you can't, the failure line is `Rating FAILED: <why>`.

### 2. Adjust the scores

The recalculation, a script in `ntm:style`, reads files from paths and touches
no backend, so hand them over this way.

Take the text of `%Theme-options`' `yaml` block and of `%Message-history`'s
`jsonl` block. Write each to a file named for its database, such as
`Casebook-options.yaml` and `Casebook-message-history.jsonl`, in this session's
working folder, exactly as read: never retype it from memory or summarize it.
Then run the recalculation on them, with `--since` the date seven days before
today:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/recalculate.py \
    adjust --options <the options file> --history <the history file> \
    --since <date>
```

It updates the options file and prints one line, `saved: <the options file>`.
Save that file's text, exactly as the script wrote it, as the `yaml` block of
`%Theme-options`.

Any other output, or a part of this you can't do, means it failed. Its failure
line is the `Recalculation FAILED: <failure>: <why>` line it printed, or else
`Recalculation FAILED: <why>`.

## Refresh

### 3. Hand over the options file

When step 2 saved this theme's `%Theme-options`, its file is already in the
working folder: go on to the draw.

Otherwise, the picker reads the options file from a path and touches no backend,
so hand it over this way.

Take the text of `%Theme-options`' `yaml` block. Write that text to a file named
for the theme, such as `Casebook-options.yaml`, in this session's working
folder, exactly as read: never retype it from memory or summarize it.

### 4. Draw the week's picks

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

### 5. Save

Save what the draw printed as the `yaml` block of `%Theme-picks`, replacing the
list there, or creating `%Theme-picks` when there is none.

## Result

For a job, return `Refreshed <Theme>-picks.yaml: 25 picks`, such as
`Refreshed Casebook-picks.yaml: 25 picks`. When there's no `%Theme-options`,
`Nothing to refresh: no <Theme>-options.yaml`.

For the weekly setup job, two lines come first, or the failure line in their
place: `Rated <Theme>-message-history.md: <n> acted, <n> ignored`, then
`Adjusted <Theme>-options.yaml`. With nothing to rate, they're one line,
`Nothing to rate`.

The picker needs Python 3 with PyYAML and jsonschema, and nothing guarantees
them where this runs: without them, it stops with a Python error. Any output
from the draw other than the list of picks, or a step of Refresh you can't do,
means the refresh failed: save no picks, and end with the `Picker FAILED:` line
it printed, or else `Refresh-picks FAILED: <why>`, with the last line it printed
or what you couldn't do. In chat, tell the user the same in plain words.
