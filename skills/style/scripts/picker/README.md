# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. Beside it,
`recalculate.py` writes a new theme's weights and checksums into its options
file. Both run on Python 3 with PyYAML and jsonschema.

`references/theme-files.md` describes the options file. Its schema,
`options.schema.yaml`, sits beside the picker in the style skill. The picker
checks every options file against it before picking, and the theme builder
checks a theme by running the same code, `theme.py`.

## Usage

```
python3 picker.py hook --options <file> [--type <list>] [--seed <number>]
```

| Flag        | What it is                                                          |
| ----------- | ------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                   |
| `--type`    | The message's reminder type and task outcomes, as `evening,slipped` |
| `--seed`    | A whole number, for a repeatable pick                               |

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
hook reads as `NoHooks`, and one with no hook that fits the message as
`MissingHook`.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: ArgumentError: argument --type: not an option: night
Picker FAILED: NoHooks: no pool in the options file gives a hook
Picker FAILED: MissingHook: no hook fits morning,slipped
```

## How it picks

### The hook

The hooks are the entries of every pool whose `roles` include `hook`, taken as
one list. The picker draws one of those that fit, each as likely as the next.

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

## Writing the numbers

```
python3 recalculate.py start --options <file> <entry file>...
```

`start` writes a new theme's weights and checksums. For each entry file, it sets
the `weight` of each of the file's entries, then writes the file's checksum, the
SHA-256 of its text exactly as handed over, in full. It saves the options file
in place, and prints a line for each entry file:

```
recounted: Casebook-characters.yaml
recounted: Casebook-scenes.yaml
```

When it can't, it prints one line on stderr, exits 1 and changes nothing, as the
picker does. An entry file that no pool names as its `file` reads as
`UnknownEntryFile`, as when `Casebook`'s entry files are handed in with another
theme's options file:

```
Recalculation FAILED: UnknownEntryFile: no pool uses Casebook-characters.yaml
```

### The weight

An entry with only a few lines would repeat itself if it were drawn as often as
one with many, so it is drawn less until it has enough lines to vary. An entry
with 3 lines is drawn half as readily as it could be, one with 9 lines three
quarters as readily, and one with 1 line a quarter. An entry with no lines of
its own counts in full. The 3 is one number that can be tuned later.

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
