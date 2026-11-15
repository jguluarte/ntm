# Recalculating the picker's weights

A sketch of how the picker's weights get recalculated, and of the skill that
does it. A line that waits on a decision says "to decide"; the open questions
are at the end.

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

A run takes in the seven days before it, last Sunday through yesterday; anything
done on the Sunday of the run is picked up by the next run. An action credits
the last message before it that names the task, so a message's window runs until
the next message naming the task.

It hands the script one line per entry, its `sent` time and verdict: in a normal
week, about 16 messages, three reminders each weekday and the weekly message.
The script writes each verdict into its entry's `verdict` field, which marks the
entry as calculated: a run judges only entries without one, so nothing is
counted twice.

| Who        | Owns                                                           |
| ---------- | -------------------------------------------------------------- |
| The model  | Reading the task list, each verdict, fetching and saving files |
| The script | Every number, and the text of every file it changes            |

## What the script reads and writes

| File                      | Read or written        | What for                                                  |
| ------------------------- | ---------------------- | --------------------------------------------------------- |
| `%Settings`               | Read, by the model     | The judged week's theme, set until the evening's rotation |
| `<Theme>-message-history` | Read and written       | Entries to judge, verdicts, pruning                       |
| `<Theme>-options.yaml`    | Read and written       | Every number the picker reads                             |
| Entry files               | Read, only when edited | To checksum and count lines                               |

The run never changes what a person or the theme builder wrote in the options
file: the levels and thresholds under `escalation` and `finishing_tasks`, a
pool's `roles` and `file`, an entry's `type`.

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
| `score`               | Entry, pool  | Each week             | 0                   | -1 to 1    |
| `half_life_days`      | Pool         | Each week             | None: no rest       | Above 0    |
| `line_half_life_days` | Entry        | Each week             | None: no rest       | Above 0    |
| `speaker_rate`        | Pool         | Each week             | 0.5                 | 0 to 1     |
| `weight`              | Pool         | Each week             | Square root of size | Above 0    |
| `bump_rate`           | `escalation` | Each week, with data  | 1.0                 | 0.1 to 0.9 |
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

How readily the picker raises a calm day's level by one. Each week the script
compares how often messages at a raised `picks.escalation` got a reaction with
those at the first level. More often by over 5 in 100: up a step. Less often by
as much: down a step. It waits for 10 judged messages on each side. A step comes
once a week, so 0.05 takes 16 weeks to go from one bound to the other. To
decide: the step; recommended 0.1, about two months from one bound to the other.
Also the 5 in 100, the 10 messages, the bounds, and whether a theme starts at
the picker's 1.0, above the bounds, or at 0.9.

### `checksums`

Each entry file's SHA-256. Linear's document list gives each file's last-edited
time without its text, so the run fetches an entry file only when it was edited
since the options file was saved. When its checksum differs, the script
recomputes what comes from that file: weights, half-lives, the kind's starting
weight and the speaker rates. An edit reaches the numbers at the next weekly
run; until then the picker draws on the old ones. To decide: an entry the file
gained or lost is only reported, for the theme builder.

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

Nothing is lost. Its verdict and feedback reached the scores and `weeks` in the
run that judged it, and the picker needs only each value's latest use, which
stays. So a history never holds more entries than its theme has values, plus the
week's entries waiting to be judged. The picker reads `picks.hook` from an
entry, as `references/theme-files.md` says; `ntm:style` and the history template
take the `picks` shape with the skill's own change.

## When it runs

Once a week, as a job of its own, early on Sunday morning, at about 04:00.

The session limit is then fully open, the run stays clear of the user's Sunday
evening, and it takes in the whole previous calendar week. The weekly job that
evening plans and rotates with fresh numbers, and the weekly report is ready
before the weekly job's chat. It runs whether or not the user's device is awake.
Between runs, the picker draws on the numbers the last run left.

Before the rotation, the weekly job's chat, never its push, says how last week's
theme did: messages sent, how many got a reaction, keeps and stales. From about
four weeks of scored messages, one tunable number, it also says whether the
theme does well or poorly for the user. With one theme, no report. The counts
come from `weeks`, a line per week of use in the options file. To decide: well
or poorly means a reaction rate 10 in 100 above or below the user's other
themes'.

## What it costs

An estimate, sized from a theme in daily use. In a normal week's run the model
reads:

| What                              | Size                                        |
| --------------------------------- | ------------------------------------------- |
| The history, fetched whole        | 30 KB: 250 bytes an entry, 100 kept, 16 new |
| The options file                  | 7 KB in, 7 KB back out                      |
| The week's tasks, with comments   | Up to 30 KB: 16 tasks at 1 to 2 KB          |
| `%Settings` and the document list | About 1 KB                                  |
| All of it                         | About 75 KB                                 |

At about 3 bytes a token, that is about 25,000 tokens a week, mostly reading,
spent in its own job on Sunday morning. It is less when a day's reminders name
the same tasks, as they mostly do. The script handles every number, line count,
checksum and the pruning without the model reading them.

Two things would make it expensive, and the design keeps both out. The entry
files, about 185 KB or 60,000 tokens for that theme, are fetched only when one
was edited. The history is fetched whole, as each reminder already does, but the
model judges only the week's entries and does no arithmetic. One cost is still
open: if a document must be written out to reach the script, the options file
and the history cost their size again.

## The script's shape

The script is one Python module on the picker's stack. It computes a theme's
numbers for both the recalculation and the theme builder
(`docs/theme-builder.md`), with a class per file it works on:

| Class       | Owns                                                             |
| ----------- | ---------------------------------------------------------------- |
| `Theme`     | The options file: loads, checks against the schema, pools, saves |
| `History`   | A message history: entries, verdicts written in, pruning, saving |
| `EntryFile` | An entry file: its checksum and each entry's line count          |
| The command | A method per thing it does; named with the skill                 |

`start`, for the theme builder, gives a new theme its first numbers with no
history: weights from lines, square-root kind weights, half-lives and speaker
rates from starting shares, every score 0, the checksums and an empty `weeks`.
`update`, in the Sunday morning job, takes in the verdicts, recounts changed
files, moves the bump rate and prunes. `report` writes the weekly theme report.

`Theme` and `History` are shared with the picker, one class each, from a module
beside the schema that both scripts import; `History` comes with the picker's
history slice. To decide: where that module lives, since it reaches across skill
folders as the schema does.

## The build order

PRs near 400 lines that each run, tested in the picker's style. The first is
also what the theme builder needs, so it comes first; the rest follow the
picker's history slice.

1. Weights and checksums from the entry files, written into the options file.
2. Half-lives and speaker rates.
3. Scores from verdicts, and `weeks`.
4. The bump rate.
5. Pruning.
6. The skill and its job: judging, the hand-off, the Sunday morning job, which
   setup creates and shows with the user's other jobs, the README.
7. The weekly theme report.

## Open questions

1. The skill's name, and the command's with it. Suggested, following the owner's
   comment that the name says what it does: `ntm:recalculate-weights`, and
   `recalculate-weights` for the command. Waits on the owner's yes.
2. The hand-off of a file's text between the backend and the script.
3. Each line marked "to decide" above.
4. Whether the history's `Keep:` line goes, now that pruning bounds it.
