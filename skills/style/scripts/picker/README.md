# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. Beside it,
`recalculate.py` writes a theme's numbers into its options file. Both run on
Python 3 with PyYAML and jsonschema.

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
separated by commas. The picker draws from the hooks whose `when` fits that
type, as `references/theme-files.md` says, or, without `--type`, from the hooks
without `when`. On a big win it draws from the hooks kept for `big_win`, or,
when none of those fits, from the hooks that fit `done`.

```
python3 picker.py hook --options Casebook-options.yaml --type big_win
hook: shared_lines/big_win
```

## Writing the numbers

`recalculate.py` writes into a theme's options file the numbers that come from
its entry files, and saves the file in place.

```
python3 recalculate.py start --options <file> <entry file>...
```

`start` gives a new theme its numbers. For each entry file whose checksum
differs from the one in the options file, or that has none yet, it sets the
`weight` of each of the file's entries, then writes the file's checksum: the
SHA-256 of its text exactly as handed over, in full. It leaves the entries of an
unchanged file alone. It prints a line for each file:

```
recounted: Casebook-characters.yaml
unchanged: Casebook-scenes.yaml
```

When it can't, it prints one line on stderr, exits 1 and changes nothing, as the
picker does. An entry file that no pool names as its `file` reads as
`Recalculation FAILED: UnknownEntryFile: no pool in the options file uses Casebook-scenes.yaml`.

### The weight

An entry's `weight` is `lines / (lines + 3)`, counting its `lines` and `riffs`,
rounded to two places, or 1.0 with neither: an entry with 3 lines weighs half.
In `Casebook`, the detective's 2 lines and 2 riffs weigh 0.57, and `any_time`'s
one line weighs 0.25. Other keys, such as a scene's `setting`, aren't lines.

### What it keeps

Everything it doesn't compute stays as it was: `when`, `roles`, `file`, `score`,
the half-lives, `speaker_rate`, and the checksums of files not handed in. An
entry its entry file doesn't hold keeps what it has. Saving keeps the key order
and lists on one line, and loses the file's comments and blank lines.
