# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. It runs on Python 3
with PyYAML and jsonschema.

`references/theme-files.md` describes the options file. Its schema,
`options.schema.yaml`, sits beside the picker in the style skill. The picker
checks every options file against it before picking, and the theme builder
checks a theme by running the same code, `theme.py`.

## Usage

```
python3 picker.py hook --options <file> [--type <list>] [--seed <number>]
python3 picker.py hook --options <file> [--type <list>] --chances
```

| Flag        | What it is                                                                                   |
| ----------- | -------------------------------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                                            |
| `--type`    | The message's reminder type and task outcomes, as `evening,slipped`                          |
| `--seed`    | A whole number, for a repeatable pick                                                        |
| `--chances` | Tables of each kind's and fitting hook's weight, score and chance, printed instead of a hook |

A seed makes a pick repeatable: the same seed and options file draw the same
hook, for tests and for looking into why a hook was picked. Without `--seed`,
each run draws afresh, seeded from the operating system's randomness rather than
the clock.

## What it prints

`hook` prints the hook as `<kind>/<slug>`: the pool it came from and the entry's
slug.

```
hook: characters/detective
```

When it can't pick, it prints one line on stderr,
`Picker FAILED: <failure>: <why>`, and exits 1. `<failure>` is the failure's
type. An options file that breaks the schema reads as `InvalidTheme`, with where
in the file and what is wrong. A `--type` that names something other than a
reminder type or task outcome, or more than one reminder type, reads as
`ArgumentError`, naming the flag and the values. A theme where no pool gives a
hook reads as `NoHooks`, one with no hook that fits the message as
`MissingHook`, and one where every hook that fits weighs 0 as `NoHookHasWeight`.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: ArgumentError: argument --type: not an option: night
Picker FAILED: NoHooks: no pool in the options file gives a hook
Picker FAILED: MissingHook: no hook fits morning,slipped
Picker FAILED: NoHookHasWeight: every hook that fits big_win weighs 0
```

## How it picks

### The hook

The picker draws the hook in two steps. First it draws a kind, a pool whose
`roles` include `hook`. Then it draws one of that kind's entries that fit the
message. A kind with no entry that fits, or whose fitting entries all weigh 0,
is never drawn.

The order of pools and entries in a file doesn't change their chances. With a
fixed `--seed`, it does change which one is drawn.

### The message's type

`--type` takes at most one reminder type, `morning`, `afternoon`, `evening` or
`weekly`, and any of the task outcomes `slipped`, `done` and `big_win`,
separated by commas. The picker draws from the hooks whose `type` fits the
message's, as `references/theme-files.md` says, or, without `--type`, from the
hooks without `type`. On a big win it draws from the hooks kept for `big_win`,
or, when none of those fits, from the hooks that fit `done`. That is decided
across the whole theme before a kind is drawn, so when one kind holds a big-win
hook that fits, the kinds without one are never drawn.

```
python3 picker.py hook --options Casebook-options.yaml --type big_win
hook: shared_lines/big_win
```

### How likely each kind and hook is

A pool and an entry each carry a `weight` and a `score`. A pool's numbers set
how likely its kind is against the other kinds, and an entry's how likely it is
against the other entries of its kind.

| Number                    | What it is                                                           |
| ------------------------- | -------------------------------------------------------------------- |
| Draw weight               | `weight * 2 ** score`                                                |
| Kind's chance             | The kind's draw weight over the total of the kinds that can be drawn |
| Hook's chance in its kind | The hook's draw weight over the total of its kind's fitting hooks    |
| Hook's chance overall     | The kind's chance times the hook's chance in its kind                |

Each point of score doubles the draw weight, and each point below 0 halves it. A
kind keeps its full weight however few of its hooks fit. A hook that weighs 0 is
never drawn.

`--chances` prints the kinds that can be drawn, then the fitting hooks of each
of those kinds, both in file order, each with its `weight`, its `score` and its
chance.

### An example

`Weighted-options.yaml`, one of the picker's test fixtures, without `--type`.

First, the kind. `scenes` weighs 3.5 and scores 1, a draw weight of 3.5 × 2 = 7.
`characters` weighs 2 and scores -1, a draw weight of 2 × 0.5 = 1. `extras`
can't be drawn: its one hook weighs 0. The kinds total 7 + 1 = 8, so `scenes`
has a chance of 7 / 8 = 0.875 and `characters` 1 / 8 = 0.125.

Then, a hook in `scenes`. `dawn` weighs 0.5 with no score, a draw weight of 0.5.
`noon` has no weight and scores 1, a draw weight of 1 × 2 = 2. `dusk` weighs 0,
and `big_win` doesn't fit. The hooks total 0.5 + 2 + 0 = 2.5, so `noon` has a
chance in `scenes` of 2 / 2.5 = 0.8. `host` is the only hook in `characters`, so
its chance there is 1.

Overall, `noon` is drawn 0.875 × 0.8 = 0.7 of the time.

```
python3 picker.py hook --options Weighted-options.yaml --chances
kind        weight  score  chance
scenes         3.5      1    0.88
characters       2     -1    0.12

hook             weight  score  chance in kind
scenes/dawn         0.5      0            0.20
scenes/noon           1      1            0.80
scenes/dusk           0      0            0.00
characters/host       3     -1            1.00
```
