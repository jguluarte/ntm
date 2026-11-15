# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file, and its message history when given one, and
prints the hook it drew. It runs on Python 3 with PyYAML and jsonschema.

`references/theme-files.md` describes the options file. Its schema,
`options.schema.yaml`, sits beside the picker in the style skill. The picker
checks every options file against it before picking, and the theme builder
checks a theme by running the same code, `theme.py`.

## Usage

```
python3 picker.py hook --options <file> [--type <list>]
    [--history <file> --today <date>] [--seed <number>]
python3 picker.py hook --options <file> [--type <list>]
    [--history <file> --today <date>] --chances
```

| Flag        | What it is                                                          |
| ----------- | ------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                   |
| `--type`    | The message's reminder type and task outcomes, as `evening,slipped` |
| `--history` | The theme's message history, as JSON lines                          |
| `--today`   | Today's date, as `2026-11-15`; needed with `--history`              |
| `--seed`    | A whole number, for a repeatable pick                               |
| `--chances` | Shows each kind's and each hook's chance instead of drawing one     |

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

With `--chances`, it prints the chance of each kind and of each hook in its kind
instead, as "How likely each kind and hook is" and "Rest" show.

When it can't pick, it prints one line on stderr,
`Picker FAILED: <failure>: <why>`, and exits 1. `<failure>` is the failure's
type. An options file that breaks the schema reads as `InvalidTheme`, with where
in the file and what is wrong. A history line that isn't a JSON entry with a
`sent` date and time reads as `InvalidHistory`, with its line number and the
line, shown below on two lines to fit. A `--type` that names something other
than a reminder type or task outcome, or more than one reminder type, reads as
`ArgumentError`, naming the flag and the values, and so do `--history` without
`--today` and a `--today` that isn't a date. A theme where no pool gives a hook
reads as `NoHooks`, one with no hook that fits the message as `MissingHook`, and
one where every hook that fits weighs 0 as `NoHookHasWeight`.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: InvalidHistory: line 2: not an entry with a sent date and time:
    {"sent":"13 Nov"}
Picker FAILED: ArgumentError: argument --type: not an option: night
Picker FAILED: ArgumentError: --history needs --today
Picker FAILED: ArgumentError: argument --today: not a date as YYYY-MM-DD: 15 Nov
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
against the other entries of its kind. Without a `weight`, a pool or entry
weighs 1; without a `score`, it scores 0.

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
of those kinds, both in file order. Each chance is rounded to two places with a
half rounding up: 0.125 shows as 0.13.

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
kind        chance
scenes        0.88
characters    0.13

hook             chance in kind
scenes/dawn                0.20
scenes/noon                0.80
scenes/dusk                0.00
characters/host            1.00
```

0.875 and 0.125 show as 0.88 and 0.13, so rounded chances can add up to just
over 1.

### Rest

A pool's `half_life_days` sets how fast its hooks come back after a message is
built on one. Right after its use, a hook can't be drawn. After `half_life_days`
days it draws at half its draw weight, and after twice that at three quarters:
each `half_life_days`, it wins back half of what it still lacks. A pool without
`half_life_days` never rests, and without `--history` nothing does.

Rest counts whole days, from the day the latest message built on the hook went
out to `--today`, as each history entry's `sent` and `picks` say. A hook used
today can't be drawn again until tomorrow. When every fitting hook of the drawn
kind was used today, none of them rests for that draw: each draws at its draw
weight, so a kind that can be drawn always gives a hook.

| Number             | What it is                                                                                    |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Days since used    | Whole days from the latest message built on the hook to `--today`                             |
| Share won back     | `1 - 2 ** (-days since used / half_life_days)`; 1 when never used or without `half_life_days` |
| Rested draw weight | Draw weight × share won back                                                                  |

With a history, a hook's chance in its kind is its rested draw weight over the
total rested draw weight of its kind's fitting hooks.

### An example of rest

`Even-options.yaml` with `Even-message-history.jsonl`, both test fixtures, on
2026-11-15.

`scenes` has a `half_life_days` of 2. The latest message built on `scenes/dawn`
went out on 2026-11-13, so its days since used are 2: one `half_life_days`, so
it has won back half, a share won back of 0.5. Its rested draw weight is its
draw weight of 1 × 0.5 = 0.5. No message used `noon` or `dusk`, so each keeps
its draw weight of 1. The fitting hooks total 0.5 + 1 + 1 = 2.5, so `dawn` has a
chance in `scenes` of 0.5 / 2.5 = 0.2, and `noon` and `dusk` each 1 / 2.5 = 0.4.

The history's message on `dawn` from 2026-11-10 is older, so it doesn't count.
The one from 2026-11-14 has no `picks`, so it used nothing. `host` was used on
2026-11-13 too, but it's the only hook in `characters`, so its chance there is
still 1.

```
python3 picker.py hook --options Even-options.yaml \
    --history Even-message-history.jsonl --today 2026-11-15 --chances
kind        chance
scenes        0.50
characters    0.50

hook             chance in kind
scenes/dawn                0.20
scenes/noon                0.40
scenes/dusk                0.40
characters/host            1.00
```

With `--seed 32` in place of `--chances`, it draws `scenes/noon`; without the
history, `scenes/dawn`.
