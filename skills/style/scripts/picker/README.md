# The picker

The picker draws the pick for a message: a perspective and a reference, two
options from different pools of a theme's options file, each at its chance.
`references/theme-files.md` describes that file. It needs Python 3 with PyYAML
and jsonschema.

```
python3 picker.py pick --options <file> [--seed <number>]
python3 picker.py pick --options <file> --chances
```

The same `--seed` draws the same picks. `pick` prints the two options it drew;
`--chances` prints each perspective instead, with its weight, score and chance:

```
perspective: characters/detective
reference: scenes/stakeout

perspective           weight  score  chance
characters/detective    0.57    0.2    0.40
scenes/stakeout            1    0.1    0.60
```

A failure prints one line on stderr and exits 1, as
`Picker FAILED: MissingWeight: every option weighs 0`.

`python3 recalculate.py start --options <file> <entry file>...` gives a new
theme its first weights, line counts and checksums and prints `saved: <file>`,
or one `Recalculation FAILED:` line.
