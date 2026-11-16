# The picker

The picker draws the hook for a message: one option from a theme's options file,
at its chance. `references/theme-files.md` describes that file.

```
python3 picker.py hook --options <file> [--type <list>] [--seed <number>]
python3 picker.py hook --options <file> [--type <list>] --chances
```

`--type` is the message's type, as `evening,slipped`. The same `--seed` draws
the same option. `hook` prints the option it drew; `--chances` prints each
option that fits instead, with its weight, score and chance:

```
hook: characters/detective

hook                   weight  score  chance
characters/detective     0.57    0.2    0.33
shared_lines/any_time    0.25      0    0.13
scenes/stakeout             1    0.1    0.54
```

`python3 recalculate.py start --options <file> <entry file>...` gives a new
theme its first weights and checksums and prints `saved: <file>`.

A failure prints one line on stderr and exits 1, as
`Picker FAILED: UnknownOption: not an option: night`.
