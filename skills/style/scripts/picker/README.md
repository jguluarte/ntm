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
`Picker FAILED: <type>: <why>`, and exits 1. `<type>` is the failure's type. An
options file that breaks the schema reads as `InvalidTheme`, with where in the
file and what is wrong. A `--type` that names something other than a reminder
type or task outcome, or more than one reminder type, reads as `ArgumentError`,
naming the flag and the values. A theme with no hook for the message reads as
`MissingHook`: either no pool gives a hook, or no hook fits.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: ArgumentError: argument --type: not an option: night
Picker FAILED: MissingHook: no pool in the options file gives a hook
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
when none of those fits, as for a normal win.

```
python3 picker.py hook --options Casebook-options.yaml --type big_win
hook: shared_lines/big_win
```
