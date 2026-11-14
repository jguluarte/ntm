# The picker

The picker picks what each message is built on: a hook, drawn at random from a
theme.

It reads a theme's options file and prints the hook it drew. It runs on Python 3
with PyYAML, as `python3 pick`.

`references/theme-files.md` describes the options file.

## Usage

```
pick hook --options <file> [--seed <number>]
```

| Flag        | What it is                                        |
| ----------- | ------------------------------------------------- |
| `--options` | The theme's options file, as YAML                 |
| `--seed`    | A whole number; the same seed draws the same hook |

## What it prints

`pick hook` prints the hook as `<kind>/<slug>`: the pool it came from and the
entry's slug.

```
hook: characters/detective
```

When it can't pick, it prints one line, `Picker FAILED: <why>`, and exits 1:
when a flag or an input is missing or malformed.

## How it picks

### The hook

The picker draws one hook from every pool that gives a hook, together, each
entry as likely as the next.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.
