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
python3 picker.py hook --options <file> [--occasions <list>] [--seed <number>]
```

| Flag          | What it is                                         |
| ------------- | -------------------------------------------------- |
| `--options`   | The theme's options file, as YAML                  |
| `--occasions` | The message's occasions, such as `morning,slipped` |
| `--seed`      | A whole number, for a repeatable pick              |

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
options file that breaks the schema reads as `InvalidOptions`, with where in the
file and what is wrong; a theme where no pool gives a hook reads as `NoHooks`,
and one where no hook fits the message's occasions as `NoHookFits`. An
`--occasions` with an unknown occasion, or more than one reminder, reads as
`ArgumentError`, naming the flag.

```
Picker FAILED: InvalidOptions: $.pools.scenes: 'roles' is a required property
Picker FAILED: NoHooks: no pool in the options file gives a hook
Picker FAILED: NoHookFits: no hook fits the occasions big_win, evening
Picker FAILED: ArgumentError: argument --occasions: not an occasion: night
```

## How it picks

### What fits the message

`--occasions` names the message's occasions, separated by commas, from the ones
`references/theme-files.md` lists under `when`: at most one reminder, and any
number of things that happened. The picker draws only from hooks whose `when`
fits, as that file says. A hook without `when` fits any message except a big
win. With `big_win`, only hooks kept for `big_win` fit. When none of those fits,
the picker draws as for a normal win, with `done` in place of `big_win`. Without
`--occasions`, only hooks without `when` fit.

```
python3 picker.py hook --options Casebook-options.yaml --occasions big_win
hook: shared_lines/big_win
```

### The hook

The hooks are the entries of every pool whose `roles` include `hook`, taken as
one list. The picker draws one of those that fit, each as likely as the next.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.
