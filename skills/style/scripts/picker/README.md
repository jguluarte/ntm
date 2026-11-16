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

| Flag        | What it is                                                          |
| ----------- | ------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                   |
| `--type`    | The message's reminder type and task outcomes, as `evening,slipped` |
| `--seed`    | A whole number, for a repeatable pick                               |
| `--chances` | Shows each hook's weight, score and chance instead of drawing one   |

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

With `--chances`, it prints each hook that fits with its weight, score and
chance instead, as "How likely each hook is" shows.

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

The hooks are the entries of every pool whose `roles` include `hook`, taken as
one list. The picker draws one of those that fit, each at its chance.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.

### The message's type

`--type` takes at most one reminder type, `morning`, `afternoon`, `evening` or
`weekly`, and any of the task outcomes `slipped`, `done` and `big_win`,
separated by commas. The picker draws from the hooks whose `type` fits the
message's, as `references/theme-files.md` says, or, without `--type`, from the
hooks without `type`. On a big win it draws from the hooks kept for `big_win`,
or, when none of those fits, from the hooks that fit `done`.

```
python3 picker.py hook --options Casebook-options.yaml --type big_win
hook: shared_lines/big_win
```

### How likely each hook is

A hook's draw weight is its `weight` times 2 to the power of its `score`,
`weight * 2 ** score`, so each point of score doubles it and each point below 0
halves it. An entry without a `weight` weighs 1, and one without a `score`
scores 0. A hook's chance is its draw weight over the total draw weight of every
hook that fits. A hook that weighs 0 is never drawn.

`--chances` prints each hook that fits, in file order, with its `weight`, its
`score` and its chance.

In `Casebook-options.yaml`, the detective weighs 0.57 and scores 0.2. 2 to the
power of 0.2 is about 1.149, so its draw weight is 0.57 × 1.149, about 0.65.
Without `--type`, three hooks fit, with draw weights 0.65, 0.25 and 1.07, 1.98
in all. The detective's chance is 0.65 / 1.98, which shows as 0.33.

```
python3 picker.py hook --options Casebook-options.yaml --chances
hook                   weight  score  chance
characters/detective     0.57    0.2    0.33
shared_lines/any_time    0.25      0    0.13
scenes/stakeout             1    0.1    0.54
```
