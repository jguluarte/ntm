# Rating the past week

Only when the weekly setup job runs `ntm:refresh-picks`. The past week's
messages went out in last week's theme, the one This week's theme named before
the job moved it on: rate and adjust that theme, and draw for this week's. With
one theme, they're the same.

When the theme has no `%Message-history`, or no entry in it was sent in the last
seven days, there's nothing to rate: go on to the draw.

A failure in step 1 or 2 ends the rating: keep its failure line for the result,
and go on to the draw.

## Rate

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

## Result

Two lines, or the failure line in their place:
`Rated <Theme>-message-history.md: <n> acted, <n> ignored`, then
`Adjusted <Theme>-options.yaml`. With nothing to rate, they're one line,
`Nothing to rate`.
