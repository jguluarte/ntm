# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. It runs on Python 3
with PyYAML and jsonschema.

`references/theme-files.md` describes the options file. The theme builder owns
its schema, `skills/theme-builder/references/options.schema.yaml`, and will
check what it builds against it; the picker checks every options file against
the same schema before picking.

## Usage

```
python3 picker.py hook --options <file> [--for <list>] [--seed <number>]
```

| Flag        | What it is                                                          |
| ----------- | ------------------------------------------------------------------- |
| `--options` | The theme's options file, as YAML                                   |
| `--for`     | The message's reminder type and task outcomes, as `evening,slipped` |
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
file and what is wrong. A `--for` that names something other than a reminder
type or task outcome, or more than one reminder type, reads as
`InvalidThemeOptions`, naming the values. A theme with no hook for the message
reads as `MissingHook`: either no pool gives a hook, or no hook fits.

```
Picker FAILED: InvalidTheme: $.pools.scenes: 'roles' is a required property
Picker FAILED: InvalidThemeOptions: not an option: night
Picker FAILED: MissingHook: no pool in the options file gives a hook
Picker FAILED: MissingHook: no hook fits morning,slipped
```

## How it picks

### What fits the message

`--for` names the message's reminder type and task outcomes, separated by
commas, from the values `references/theme-files.md` lists under `when`: at most
one reminder type, and any number of task outcomes. The picker draws only from
hooks whose `when` fits, as that file says. A hook without `when` fits any
message except a big win. With `big_win`, only hooks kept for `big_win` fit.
When none of those fits, the picker draws as for a normal win, with `done` in
place of `big_win`. Without `--for`, only hooks without `when` fit.

```
python3 picker.py hook --options Casebook-options.yaml --for big_win
hook: shared_lines/big_win
```

### The hook

The hooks are the entries of every pool whose `roles` include `hook`, taken as
one list. The picker draws one of those that fit, each as likely as the next.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.
