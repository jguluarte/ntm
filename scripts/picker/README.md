# The picker

The picker picks what each message is built on: a hook, sometimes a speaker, and
a line from the hook. It draws at random, weighted, and rests whatever was used
lately, so a theme's whole range gets used.

`ntm:style` runs it in its Pick step. The run fetches the theme's files and the
history from the backend and hands them over as files; the picker reads them and
prints a few lines. It needs `yq`, the Python one, and `jq`.

`references/theme-files.md` describes the files it reads.

## Usage

```
pick hook --options <file> --history <file> --theme <name> --now <time>
    [--occasions <list>] [--seed <number>] [--chances]

pick line --options <file> --history <file> --theme <name> --now <time>
    --hook <kind>/<slug> --entries <file>
    [--occasions <list>] [--seed <number>] [--chances]
```

| Flag          | What it is                                                              |
| ------------- | ----------------------------------------------------------------------- |
| `--options`   | The theme's options file, as YAML                                       |
| `--history`   | The Entries part of `%Message-history`, one JSON line per message       |
| `--theme`     | The theme's name; only its entries in the history count                 |
| `--now`       | The time now, `YYYY-MM-DD HH:MM`, in the user's timezone                |
| `--occasions` | The occasions that hold, with commas between, such as `morning,slipped` |
| `--seed`      | A whole number; the same seed draws the same                            |
| `--chances`   | Print each candidate's numbers and chance in place of drawing           |
| `--hook`      | The hook `pick hook` printed                                            |
| `--entries`   | The hook's entry file, the file its pool names, as YAML                 |

## What it prints

`pick hook` prints the hook and the speaker, each as `<kind>/<slug>`: the pool
it came from and the entry's slug.

```
hook: characters/detective
speaker: none
```

When no hook fits the occasions, it draws from the entries without `when`, and
says so in a third line:

```
fallback: no hook fits evening,big_win; drew from the entries without when
```

`pick line` prints the line drawn from the hook's entry, with its `bend` when it
is a riff that has one, or `line: none` when the entry has no line that fits.

```
line: Every lie leaves a crumb.
bend: Treat the slipped task as the crumb that gives away what the user did.
```

When it can't pick, it prints one line, `Picker FAILED: <why>`, and exits 1:
when no hook fits and every entry has a `when`, when an input is missing or
malformed, or when `yq` or `jq` isn't installed.

## How it picks

### What fits

The occasions are of two kinds: which reminder a message is, `morning`,
`afternoon`, `evening` or `weekly`, and what happened to its tasks, `slipped`,
`done` or `big_win`. A message is one reminder at most, and any of what happened
that holds.

An entry or riff fits a message when its `when` names no reminder or this
message's reminder, and names nothing that happened or something that happened
in this message.

| `when`               | Fits                                |
| -------------------- | ----------------------------------- |
| none                 | Every message                       |
| `evening`            | Any evening                         |
| `slipped`            | Any message with a slipped task     |
| `[evening, slipped]` | Only an evening with a slipped task |
| `[morning, weekly]`  | Either reminder                     |

### The hook

On a big win, only the entries that name `big_win` can be the hook. Otherwise
the hook comes from the entries that fit. Either way, the picker draws one from
every pool that gives a hook, together, each entry at its effective weight.

When no entry fits, it draws from the entries without `when`, and says so.

### The speaker

When the hook's pool gives a speaker, the hook is a person's, and that person is
the speaker. Otherwise it draws a speaker the same way from the pools that give
one, and keeps them at their pool's `speaker_rate`.

### The line

From the hook's entry, it keeps every line, and each riff whose `when` fits, and
draws one. Each counts the same, and a line drawn lately rests over the entry's
`line_half_life_days`.

### Use and rest

An entry was used when a message's hook or speaker named it, and a line when a
message's `line_drawn` holds its text. Only the history entries of `--theme`
count. The order of entries in a file means nothing.

## The numbers

The options file holds these numbers. The theme builder and the nightly job
compute them as below; the picker only reads them.

| Number                | What it is                              | How it is computed                   | Tunable |
| --------------------- | --------------------------------------- | ------------------------------------ | ------- |
| `weight`              | What an entry has to offer              | `lines / (lines + 3)`, or 1          | 3       |
| `half_life_days`      | Days a used entry's rest takes to halve | `entries / (daily * share) / 2`      | 2       |
| `line_half_life_days` | Days a drawn line's rest takes to halve | `lines / (daily * share) / 2`        | 2       |
| `score`               | How well its messages landed            | `(landed - missed) / (messages + 3)` | 3       |
| `speaker_rate`        | Chance a non-person hook gets a speaker | `(0.5 - people) / (1 - people)`      | 0.5     |

| Term       | What it is                                                                  |
| ---------- | --------------------------------------------------------------------------- |
| `lines`    | The entry's lines and riffs                                                 |
| `daily`    | Messages a day: those in `%Message-history`, over the days it covers        |
| `share`    | How often the pool or entry gives the hook: its part of the history's hooks |
| `landed`   | Messages built on the entry that the user acted on or kept                  |
| `missed`   | Messages built on the entry that the user didn't act on, or called stale    |
| `messages` | Every message built on the entry; the 3 keeps a few from swinging the score |
| `people`   | The share of hooks from pools that give a speaker                           |

Before a theme has any history, an entry's `share` is its part of all hook
weights. A score stays between -1 and 1. `speaker_rate` is at least 0, and aims
for half of all messages to have a speaker, counting the hooks that are a
person's.

The picker works these out for each draw:

| Number           | What it is                                  | How it is computed                     | Tunable |
| ---------------- | ------------------------------------------- | -------------------------------------- | ------- |
| rest             | How rested an entry or line is, from 0 to 1 | `1 - 2^(-days since used / half-life)` |         |
| effective weight | What an entry counts for in the draw        | `weight * 2^score * rest`              | 2       |
| chance           | How likely a candidate is to be drawn       | its effective weight / all of theirs   |         |

Rest is 0 right after use, 0.5 one half-life later, 0.75 two half-lives later. A
score of 1 doubles an entry's weight, and -1 halves it. A speaker's chance also
counts its pool's `speaker_rate`.

A number the options file doesn't hold takes its default:

| Number                | Default       |
| --------------------- | ------------- |
| `weight`              | 1             |
| `score`               | 0             |
| `half_life_days`      | none: no rest |
| `line_half_life_days` | none: no rest |
| `speaker_rate`        | 0.5           |
