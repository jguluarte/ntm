# The picker

The picker draws the hook for a message: one option from a theme's options file,
at its chance. `references/theme-files.md` describes that file. It needs Python
3 with PyYAML and jsonschema.

```
python3 picker.py hook --options <file> [--seed <number>]
python3 picker.py hook --options <file> --chances
```

The same `--seed` draws the same option. `hook` prints the option it drew;
`--chances` prints each option instead, with its weight, score and chance:

```
hook: characters/detective

hook                   weight  score  chance
characters/detective     0.57    0.2    0.33
shared_lines/any_time    0.25      0    0.13
scenes/stakeout             1    0.1    0.54
```

A failure prints one line on stderr and exits 1, as
`Picker FAILED: MissingWeight: every option weighs 0`.

`python3 recalculate.py start --options <file> <entry file>...` gives a new
theme its first weights and checksums and prints `saved: <file>`, or one
`Recalculation FAILED:` line.
