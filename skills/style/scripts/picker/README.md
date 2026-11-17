# The picker

The picker draws the pick for a message: a perspective and a reference, two
options from different pools of a theme's options file, each at its chance.
`references/theme-files.md` describes that file. It needs Python 3 with PyYAML
and jsonschema.

```
python3 picker.py pick --options <file> [--seed <number>]
python3 picker.py pick --options <file> --chances
```

An option picked recently rests: its pick takes 2 off its score, and that rest
halves with each `half_life_days` of its pool. `--history <file>` gives the
recent picks, the theme's message history as JSON lines, and `--now <time>` says
when the pick is for, written like the history's `sent`, such as
`2026-11-14 08:45`. `--now` defaults to this machine's clock.

The same `--seed` draws the same picks. `pick` prints the two options it drew;
`--chances` prints each perspective instead, with its weight, score, rest and
chance. Here with a history:

```
perspective: characters/detective
reference: scenes/stakeout

perspective           weight  score  rest  chance
characters/detective    0.57    0.2  1.78    0.40
scenes/stakeout            1    0.1  1.89    0.60
```

A failure prints one line on stderr and exits 1, as
`Picker FAILED: MissingWeight: every option weighs 0`.

`python3 recalculate.py start --options <file> <entry file>...` gives a new
theme its first weights and checksums and prints `saved: <file>`, or one
`Recalculation FAILED:` line.
