# Rating the past week

The weekly setup job rates last week's messages before the draw: did the user
act on each one? The verdicts move the scores of last week's theme, the one This
week's theme in `%Settings` named before the job moved it on, so the picker
leans toward what got the user moving. Every file below is that theme's.

## Rate

### 1. Rate the messages

Read the theme's `%Message-history`. Rate each entry sent in the last seven days
that has `tasks` and no `verdict`.

The user acted on a message when, since it was sent, they closed one of its
tasks or changed a task's planned date. When the task's `Planned date history`
lists the entry's planned date, ntm moved it, not the user.

Use the tasks the weekly setup job already looked up, and look up only the rest.
Read a task's `Planned date history` only when its date changed.

Write `acted` or `ignored` as each entry's `verdict`, and save
`%Message-history`. Its line is
`Rated <Theme>-message-history.md: <n> acted, <n> ignored`, or
`Rating FAILED: <why>`. With no entry sent in the last seven days, it is
`Nothing to rate`.

### 2. Adjust the scores

Write the text of `%Theme-options`' `yaml` block and of `%Message-history`'s
`jsonl` block each to a file named for its database, such as
`Casebook-options.yaml` and `Casebook-message-history.jsonl`, in this session's
working folder, exactly as read, never from memory. Then run the recalculation
on them, with `--since` the date seven days before today:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/style/scripts/picker/recalculate.py \
    adjust --options <the options file> --history <the history file> \
    --since <date>
```

It updates the options file and prints one line, `saved: <the options file>`;
anything else is `Recalculation FAILED: <why>`. Save that file's text, exactly
as the script wrote it, as the `yaml` block of `%Theme-options`. Its line is
`Adjusted <Theme>-options.yaml`.

Nothing to rate, or a failure, ends the rating there. Keep its lines for the
result, and go on to the draw.
