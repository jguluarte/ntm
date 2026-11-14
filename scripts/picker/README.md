# The picker

The picker picks what each message is built on: a hook, sometimes a speaker, and
a line from the hook. It draws at random, weighted, and rests whatever was used
lately, so a theme's whole range gets used. It also moves the user on to the
next theme each week.

`ntm:style` runs it: in its Pick step for each message, and in This week's theme
for the weekly job. The run fetches the theme's files and the history from the
backend and hands them over as files; the picker reads them and prints a few
lines. It needs `jq` 1.6 or later, and `yq`, the Python one; `pick theme` needs
only `jq`.

`references/theme-files.md` describes the files it reads.

## Usage

```
pick hook --options <file> --history <file> --theme <name> --now <time>
    [--occasions <list>] [--seed <number>] [--chances]

pick line --options <file> --history <file> --theme <name> --now <time>
    --hook <kind>/<slug> --entries <file>
    [--occasions <list>] [--seed <number>] [--chances]

pick theme --this-week <theme> <theme>...
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
| `--this-week` | This week's theme                                                       |
| `<theme>...`  | Every theme, in the order the Themes part of `%Settings` lists them     |

The lines of the history's code fence are skipped, so its lines can be saved
with or without the fence.

## What it prints

`pick hook` prints the hook and the speaker, each as `<kind>/<slug>`: the pool
it came from and the entry's slug.

```
hook: characters/detective
speaker: none
```

`pick line` prints the line drawn from the hook's entry, with its `bend` when it
is a riff that has one, or `line: none` when the entry has no line that fits.

```
line: Every lie leaves a crumb.
bend: Treat the slipped task as the crumb that gives away what the user did.
```

`pick theme` prints the theme after this week's, in the list's order, and the
first after the last: `theme: Harbor`. With one theme, it prints that one. When
this week's theme isn't in the list, it prints the first.

When it can't pick, it prints one line, `Picker FAILED: <why>`, and exits 1:
when no hook fits, when every hook that fits weighs 0, when a flag or an input
is missing or malformed, or when a tool it needs isn't there.

## How it picks

### What fits

The occasions are of two kinds: which reminder a message is, `morning`,
`afternoon`, `evening` or `weekly`, and what happened to its tasks, `slipped`,
`done` or `big_win`. A message is one reminder at most, and any of what happened
that holds.

An entry or riff fits a message when its `when` names no reminder or this
message's reminder, and names nothing that happened or something that happened
in this message. An entry without `when` fits every message.

| `when`               | Fits                                |
| -------------------- | ----------------------------------- |
| none                 | Every message                       |
| `evening`            | Any evening                         |
| `slipped`            | Any message with a slipped task     |
| `[evening, slipped]` | Only an evening with a slipped task |
| `[morning, weekly]`  | Either reminder                     |

### The hook

The picker draws one hook from every pool that gives a hook, together, each
entry at its effective weight, from the entries that fit. On a big win, it draws
only from the entries that fit and name `big_win`; when the theme keeps none for
a big win, it draws from the entries without `when`.

### The speaker

When the hook's pool gives a speaker, the hook is a person's, and that person is
the speaker. Otherwise it draws a speaker the same way from the pools that give
one, and keeps them at their pool's `speaker_rate`.

### The line

From the hook's entry, it keeps every line, and each riff whose `when` fits, and
draws one. Each counts the same, and a line drawn lately rests over the entry's
`line_half_life_days`.

### Use and rest

An entry was used when a message's hook or speaker named it, and a line was
drawn when a message's `line_drawn` holds its text. Only the history entries of
`--theme` count, and only the latest use. A history entry whose `sent` can't be
read counts as no use. When everything in a draw rests at 0, rest is set aside
for that draw.

The order of entries in a file doesn't change their chances. With a fixed
`--seed`, it does change which one is drawn.

## The numbers

The options file holds these numbers. The theme builder computes them when it
builds a theme, and the nightly job recomputes them; the picker only reads them.
Tunable is the constant in each formula that can be changed to tune it.

| Number                | What it is                               | How it is computed                   | Tunable |
| --------------------- | ---------------------------------------- | ------------------------------------ | ------- |
| `weight`              | What an entry has to offer, up to 1      | `lines / (lines + 3)`, or 1          | 3       |
| `half_life_days`      | Days for the chance a use took to halve  | `entries / (daily * share) / 2`      | 2       |
| `line_half_life_days` | Days for the chance a draw took to halve | `lines / (daily * share) / 2`        | 2       |
| `score`               | How well its messages landed, -1 to 1    | `(landed - missed) / (messages + 3)` | 3       |
| `speaker_rate`        | Chance a non-person hook gets a speaker  | `(0.5 - people) / (1 - people)`      | 0.5     |

| Term       | What it is                                                                           |
| ---------- | ------------------------------------------------------------------------------------ |
| `lines`    | How many lines and riffs the entry has                                               |
| `entries`  | How many entries the pool has                                                        |
| `daily`    | Messages a day: those in `%Message-history`, over the days it covers                 |
| `share`    | Its part of the theme's hooks in the history: the pool's, or for a line, the entry's |
| `messages` | The messages built on the entry: those whose `hook` is the entry                     |
| `landed`   | Of those, the ones whose `verdict` says they landed, or whose `feedback` is `keep`   |
| `missed`   | Of those, the ones whose `verdict` says they missed, or whose `feedback` is `stale`  |
| `people`   | The part of the theme's hooks in the history from pools that give a speaker          |

`weight` is `lines / (lines + 3)` for an entry with lines or riffs, and 1 for an
entry without, such as a scene: an entry with lines weighs less until it has
enough of them to vary. `half_life_days` is per pool, and `line_half_life_days`
per entry with lines or riffs. A message's `verdict` is the nightly job's
verdict on the entry it was built on, and its `feedback` the user's word on it.
`speaker_rate` aims for half of all messages to have a speaker, counting the
hooks that are a person's. It is never below 0, and when every hook is a
person's, `people` is 1 and `speaker_rate` is 0.

### Before any history

The theme builder computes the numbers before the theme has a history:

- `daily` is how many reminders the user's jobs send a day, or 3 when that isn't
  known.
- An entry's `share` is its `weight` over the weights of every entry in a pool
  that gives a hook; a pool's is the sum of its entries'.
- `people` is the starting `share` of the pools that give a speaker, added up.
- `score` is 0.

The nightly job uses the same starting `share` for a pool or entry the history
holds no hook from yet, so no `share` is ever 0.

### What the picker works out

| Number           | What it is                                  | How it is computed                     |
| ---------------- | ------------------------------------------- | -------------------------------------- |
| rest             | How rested an entry or line is, from 0 to 1 | `1 - 2^(-days since used / half-life)` |
| effective weight | What an entry counts for in the draw        | `weight * 2^score * rest`              |
| chance           | How likely a candidate is to be drawn       | its effective weight / all of theirs   |

The days since used run from the latest use to `--now`. The half-life is the
pool's `half_life_days` for an entry, and the entry's `line_half_life_days` for
a line. Right after use an entry has lost all its chance, and rests at 0; one
half-life later it has half of it back, and rests at 0.5; two half-lives later,
0.75. A score of 1 doubles an entry's weight, and -1 halves it. A speaker's
chance also counts its pool's `speaker_rate`.

### An example

One made-up entry, `characters/detective`, carried through every number. The
user gets 3 messages a day. The detective has 2 lines and 2 riffs. The
`characters` pool has 2 entries and gives a third of the hooks; the detective
gives a sixth. 9 messages were built on it: 5 landed and 2 missed. It was last
used one day ago.

| Number                | Worked out                                     | Value |
| --------------------- | ---------------------------------------------- | ----- |
| `weight`              | `4 / (4 + 3)`                                  | 0.57  |
| `half_life_days`      | `2 / (3 * 1/3) / 2`                            | 1     |
| `line_half_life_days` | `4 / (3 * 1/6) / 2`                            | 4     |
| `score`               | `(5 - 2) / (9 + 3)`                            | 0.25  |
| rest                  | `1 - 2^(-1 / 1)`                               | 0.5   |
| effective weight      | `0.57 * 2^0.25 * 0.5`                          | 0.34  |
| chance                | `0.34 / 2`, when all the candidates add to `2` | 0.17  |

### Defaults

A number the options file doesn't hold takes its default. A line has no numbers
of its own, so each line takes weight 1 and score 0.

| Number                | Default       |
| --------------------- | ------------- |
| `weight`              | 1             |
| `score`               | 0             |
| `half_life_days`      | none: no rest |
| `line_half_life_days` | none: no rest |
| `speaker_rate`        | 0.5           |
