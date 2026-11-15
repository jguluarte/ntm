# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. It runs on Python 3
with PyYAML and jsonschema.

`references/theme-files.md` describes the options file, and
`options.schema.yaml` holds it to that description: the picker checks every
options file against it before picking. The theme builder will check what it
builds against the same file.

## Usage

```
python3 picker.py hook --options <file> [--seed <number>]
```

| Flag        | What it is                            |
| ----------- | ------------------------------------- |
| `--options` | The theme's options file, as YAML     |
| `--seed`    | A whole number, for a repeatable pick |

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
options file that breaks the schema reads as `ValueError`, with where in the
file and what is wrong, and so does a theme where no pool gives a hook.

```
Picker FAILED: ValueError: $.pools.scenes: 'gives' is a required property
Picker FAILED: ValueError: no pool in the options file gives a hook
```

## How it picks

### The hook

The hooks are the entries of every pool that gives a hook, taken as one list.
The picker draws one of them, each as likely as the next.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.
