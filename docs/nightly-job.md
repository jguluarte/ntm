# The nightly job

A sketch of the nightly job and its skill. A line that waits on a decision says
"to decide"; the open questions are at the end.

## What it is for

It keeps each theme's numbers current, so the picker can stay a small, fast
script that only reads them. It is the one part of ntm that learns from how the
user reacted: which hooks land, which kinds work, and whether a raised level
gets more done.

## Who does what

The model only judges. For each history entry not yet judged, it reads the tasks
the entry names on the task list and decides whether the user acted on them:
closing one, moving its date or clearing the day, setting aside ntm's own
changes, which each task's `Planned date history` lists. The verdict is `landed`
when they did, `missed` when they didn't, and `none` when every task was done
before the message went out.

It hands the script one line per entry, its `sent` time and verdict: on a normal
night, the day's three or so messages, each judged once. When two messages name
the same task, acting on it credits both. To decide: credit only the latest
message before the action.

| Who        | Owns                                                           |
| ---------- | -------------------------------------------------------------- |
| The model  | Reading the task list, each verdict, fetching and saving files |
| The script | Every number, and the text of every file it changes            |

## What the script reads and writes

| File                      | Read or written        | What for                                    |
| ------------------------- | ---------------------- | ------------------------------------------- |
| `%Settings`               | Read, by the model     | This week's theme, the one a night works on |
| `<Theme>-message-history` | Read and written       | Entries to judge, verdicts, pruning         |
| `<Theme>-options.yaml`    | Read and written       | Every number the picker reads               |
| Entry files               | Read, only when edited | To checksum and count lines                 |

The job never changes what a person or the theme builder wrote in the options
file: the levels and thresholds under `escalation` and `finishing_tasks`, a
pool's `roles` and `file`, an entry's `when`.

The files are documents in the user's backend, and the script touches no
backend. As for the picker, the run fetches each file, hands its text over, and
saves back what the script wrote. To decide: whether a document can reach the
script and come back without the model writing it out in full; the picker shares
the question.

## The numbers

Plain words, then the formula. "The first formulas" were written for the
picker's first draft; where they give a number, it is kept.

| Number                | Where        | Changes               | Default             | Bounds     |
| --------------------- | ------------ | --------------------- | ------------------- | ---------- |
| `weight`              | Entry        | When its file changes | 1                   | 0 to 1     |
| `score`               | Entry, pool  | Each night            | 0                   | -1 to 1    |
| `half_life_days`      | Pool         | When its file changes | None: no rest       | Above 0    |
| `line_half_life_days` | Entry        | When its file changes | None: no rest       | Above 0    |
| `speaker_rate`        | Pool         | When a file changes   | 0.5                 | 0 to 1     |
| `weight`              | Pool         | When its file changes | Square root of size | Above 0    |
| `bump_rate`           | `escalation` | Each night, with data | 1.0                 | 0.1 to 0.9 |
| `checksums`           | Top level    | When a file changes   | None                | None       |

### An entry's `weight`

What an entry has to offer: few lines weigh less until there are enough to vary.
`lines / (lines + 3)`, counting riffs, or 1 with none; from the first formulas.
One line weighs 0.25, nine weigh 0.75.

### `score`

How well the messages built on an entry landed. Each judged message moves the
score of its `picks.hook` and `picks.speaker` a step toward 1 if it landed, -1
if it missed: `score + 0.1 * (target - score)`, so about the last ten decide it.
A `keep` or `stale` steps by 0.3. The first formulas counted every message, and
pruning drops old ones, so the score moves a step at a time instead. To decide:
the 0.1 and the 0.3.

### `half_life_days` and `line_half_life_days`

The days until a picked entry, or a drawn line, wins back half the chance it
lost: half the time it takes to work through the pool, or the entry's lines.
`entries / (daily * share) / 2` and `lines / (daily * share) / 2`, from the
first formulas: `daily` is messages a day, `share` the pool's or entry's part of
the history's hooks. With no history, `daily` is the user's reminders a day, or
3, and shares come from the weights.

### A pool's `speaker_rate`

How often a message names a speaker from the pool, aiming for half of all
messages: `(0.5 - people) / (1 - people)`, never below 0, where `people` is the
part of hooks from pools whose `roles` hold speaker; from the first formulas.

### A kind's `weight`

A pool's weight when the picker draws a kind: the square root of its size,
counting lines for line groups, so 9 entries start at 3 and 75 at about 8.7. It
moves with reactions through a `score` on the pool, moved like an entry's by
each message whose hook came from it. To decide: that score.

### `bump_rate`

How readily the picker raises a calm day's level by one. Each night the script
compares how often messages at a raised `picks.escalation` got a reaction with
those at the first level. More often by over 5 in 100: up 0.05. Less often by as
much: down 0.05. It waits for 10 judged messages on each side. To decide: those
numbers, the bounds, and whether a theme starts at the picker's 1.0, above the
bounds, or at 0.9.

### `checksums`

Each entry file's SHA-256. Linear's document list gives each file's last-edited
time without its text, so the run fetches an entry file only when it was edited
since the options file was saved. When its checksum differs, the script
recomputes what comes from that file: weights, half-lives, the kind's starting
weight and the speaker rates. To decide: an entry the file gained or lost is
only reported, for the theme builder.

## Pruning the history

The rule, in the owner's words: "Once all of the things from an old entry have
been reselected later....we don't need the past references to it. then it can
just maintain a rolling forward and causes an upper limit on that theme's
message history file."

Each entry holds a `picks` object, exactly what the picker printed: `hook`,
`speaker`, `line`, `escalation`, `finishing_tasks`, later `role` and `bump`.
Those keys hold for every theme; only their values are the theme's. A judged
entry goes once every value in its `picks` appears under the same key in a later
entry.

Nothing is lost. Its verdict and feedback reached the scores and `weeks` the
night it was judged, and the picker needs only each value's latest use, which
stays. So a history never holds more entries than its theme has values.
`ntm:style`, the history template and `references/theme-files.md` take the
`picks` shape in the picker's history slice.

## When it runs

Nightly as its own light job, after the day's last reminder, and in the weekly
job just before `ntm:clean`, so the week is judged before planning.

Before the rotation, the weekly job's chat, never its push, says how last week's
theme did: messages sent, how many got a reaction, keeps and stales. From about
four weeks of scored messages, one tunable number, it also says whether the
theme does well or poorly for the user. With one theme, no report. The counts
come from `weeks`, a line per week of use in the options file. To decide: well
or poorly means a reaction rate 10 in 100 above or below the user's other
themes'.

## What it costs

On a normal night the model reads the history, fetched whole (about 250 bytes an
entry, so 25 KB at 100 entries); the options file, 7 KB in and 7 KB back out;
the day's three or so tasks with their comments, 1 to 2 KB each; and a few lines
of `%Settings` and the document list. Sized from a theme in daily use, that is
about 15,000 tokens a night, mostly reading. The script handles every number,
line count, checksum and the pruning without the model reading them.

Two things would make it expensive, and the design keeps both out. The entry
files, about 185 KB or 45,000 tokens for that theme, are fetched only when one
was edited. The history is fetched whole, as each reminder already does, but the
model judges only the day's entries and does no arithmetic. One cost is still
open: if a document must be written out to reach the script, the options file
and the history cost their size again.

## The script's shape

The script is one Python module on the picker's stack. It computes a theme's
numbers for both the nightly job and the theme builder
(`docs/theme-builder.md`), with a class per file it works on:

| Class       | Owns                                                             |
| ----------- | ---------------------------------------------------------------- |
| `Options`   | The options file: loads, checks against the schema, pools, saves |
| `History`   | A message history: entries, verdicts written in, pruning, saving |
| `EntryFile` | An entry file: its checksum and each entry's line count          |
| The command | A method per thing it does; named with the skill                 |

`start`, for the theme builder, gives a new theme its first numbers with no
history: weights from lines, square-root kind weights, half-lives and speaker
rates from starting shares, every score 0, the checksums and an empty `weeks`.
`update`, nightly, takes in the verdicts, recounts changed files, moves the bump
rate and prunes. `report` writes the weekly theme report.

`Options` and `History` are shared with the picker, one class each, from a
module beside the schema that both scripts import; `History` comes with the
picker's history slice. To decide: where that module lives, since it reaches
across skill folders as the schema does.

## The build order

PRs near 400 lines that each run, tested in the picker's style. The first is
also what the theme builder needs, so it comes first; the rest follow the
picker's history slice.

1. Weights and checksums from the entry files, written into the options file.
2. Half-lives and speaker rates.
3. Scores from verdicts, and `weeks`.
4. The bump rate.
5. Pruning.
6. The skill and the job: judging, the hand-off, setup, the weekly step, the
   README.
7. The weekly theme report.

## Open questions

1. The skill's name, and the command's with it.
2. Whether setup shows the nightly job in its jobs round for the user's yes.
3. The hand-off of a file's text between the backend and the script.
4. Each line marked "to decide" above.
5. Whether the history's `Keep:` line goes, now that pruning bounds it.
