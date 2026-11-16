# The picker

The picker picks what each message is built on, its hook: an option drawn at
random from a theme.

It reads a theme's options file and prints the option it drew. Beside it,
`recalculate.py` writes a new theme's weights and checksums into its options
file. Both run on Python 3 with PyYAML and jsonschema.

`references/theme-files.md` describes the options file. Its schema,
`options.schema.yaml`, sits beside the picker in the style skill. The picker
checks every options file against it before picking, and the theme builder
checks a theme by running the same code, `theme.py`.

## Usage

```
python3 picker.py hook --options <file> [--type <list>] [--seed <number>]
python3 picker.py hook --options <file> [--type <list>] --chances
```

| Flag        | What it is                                                                         |
| ----------- | ---------------------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                                  |
| `--type`    | The message's reminder type and task outcomes, as `evening,slipped`                |
| `--seed`    | A whole number, for a repeatable pick                                              |
| `--chances` | A table of each fitting option's weight, score and chance, shown instead of a hook |

A seed makes a pick repeatable: the same seed and options file draw the same
option, for tests and for looking into why an option was picked. Without
`--seed`, each run draws afresh, seeded from the operating system's randomness
rather than the clock.

## What it prints

`hook` prints the option it drew as `<kind>/<slug>`: the pool it came from and
the entry's slug.

```
hook: characters/detective
```

When it can't pick, it prints one line on stderr,
`Picker FAILED: <failure>: <why>`, and exits 1. `<failure>` is the failure's
type.

An options file that breaks the schema, or where no pool gives a hook, reads as
`InvalidTheme`, with where in the file and what is wrong. A `--type` that names
something other than a reminder type or task outcome reads as `UnknownOption`,
and one that names more than one reminder type as `MoreThanOneReminderType`.

When the file and the type are fine but there is nothing to draw, a message no
option fits reads as `MissingOptions`, and one where every option that fits
weighs 0 as `MissingWeight`.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: InvalidTheme: $.pools: no pool gives a hook
Picker FAILED: UnknownOption: not an option: night
Picker FAILED: MissingOptions: no option fits morning,slipped
Picker FAILED: MissingWeight: every option that fits big_win weighs 0
```

## How it picks

### The options

The options are the entries of every pool whose `roles` include `hook`, taken as
one list. The picker draws one of those that fit, each at its chance.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.

### The message's type

`--type` takes at most one reminder type, `morning`, `afternoon`, `evening` or
`weekly`, and any of the task outcomes `slipped`, `done`, `win` and `big_win`,
separated by commas. The picker draws from the options whose `type` fits the
message's, as `references/theme-files.md` says, or, without `--type`, from the
options without `type`. On a big win it draws from the options kept for
`big_win`, or, when none of those fits, from the options that fit `done`.

```
python3 picker.py hook --options Casebook-options.yaml --type big_win
hook: shared_lines/big_win
```

### How likely each option is

An option's draw weight is its `weight` times 2 to the power of its `score`,
`weight * 2 ** score`, so each point of score doubles it and each point below 0
halves it. An option's chance is its draw weight over the total draw weight of
every option that fits. An option that weighs 0 is never drawn.

`--chances` prints each option that fits, in file order, with its `weight`, its
`score` and its chance.

In `Casebook-options.yaml`, the detective's draw weight, about 0.65, is 0.33 of
the total draw weight, 1.98, of the three options that fit without `--type`.

```
python3 picker.py hook --options Casebook-options.yaml --chances
hook                   weight  score  chance
characters/detective     0.57    0.2    0.33
shared_lines/any_time    0.25      0    0.13
scenes/stakeout             1    0.1    0.54
```

## Writing the numbers

```
python3 recalculate.py start --options <file> <entry file>...
```

`start` gives a new theme its first weights and checksums, in its options file.
It sets the `weight` of each entry in the entry files it is handed, records each
entry file's checksum, the SHA-256 of its text exactly as handed over, in full,
then saves the options file in place and prints one line naming it:

```
saved: Casebook-options.yaml
```

When it can't, it prints one line on stderr and exits 1, as the picker does, and
leaves the options file as it was. An entry file that no pool names as its
`file` fails with `UnknownEntryFile`, as when `Casebook`'s entry files are
handed in with another theme's options file:

```
Recalculation FAILED: UnknownEntryFile: no pool uses Casebook-characters.yaml
```

### The weight

An entry with only a few lines would repeat itself if it were drawn as often as
one with many, so it is drawn less until it has enough lines to vary. An entry
with 3 lines is drawn half as readily as it could be, one with 9 lines three
quarters as readily, and one with 1 line a quarter.

```
weight = lines / (lines + LINES_AT_HALF_WEIGHT)
```

`lines` counts the entry's `lines` and `riffs`; other keys, such as a scene's
`setting`, aren't lines. `LINES_AT_HALF_WEIGHT` is 3, the number of lines at
which an entry weighs half. The weight is rounded to two places, and is 1.0 for
an entry with no lines.

| lines | weight |
| ----- | ------ |
| 1     | 0.25   |
| 3     | 0.5    |
| 9     | 0.75   |

In `Casebook`, the detective's 2 lines and 2 riffs weigh 0.57, and `any_time`'s
one line weighs 0.25.

### What it keeps

Everything it doesn't compute stays as it was: `type`, `roles`, `file`, `score`,
the half-lives and `speaker_rate`. Saving keeps the key order and lists on one
line, and loses the file's comments and blank lines: the options file is written
by ntm, not annotated by hand.
