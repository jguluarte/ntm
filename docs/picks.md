# Picks

A sketch to answer line by line: what the picker gives the writer, and how a
week of picks is drawn ahead.

A pick is the theme's side of one message: two pieces of the theme that give the
writer a point of view. The day's side comes from the reminder when it runs.

## A pick

| Piece     | Drawn from                         | What the writer does with it          |
| --------- | ---------------------------------- | ------------------------------------- |
| `hook`    | Every pool with the `hook` role    | Builds the message on it              |
| `speaker` | Every pool with the `speaker` role | Says the message, in their own manner |

Every pick has both. A hook that can speak is its own speaker, so its lines stay
in its own mouth; any other hook gets a speaker drawn for it.

In a theme like `Casebook`, the pick `hook: scenes/stakeout` with
`speaker: characters/detective` has the detective tell the message from a cold
car across from the suspect's door. A pick holds no levels, no reminder type and
no tasks.

## Variety

Each option counts once, at its weight and score. A pool with more options comes
up more often, because it has more to offer; a theme that wants more of a kind
adds options to it.

In a week, a drawn hook sits out until every other hook has had its turn, and a
drawn speaker until every other speaker has; then each starts over. So no hook
comes back within a week unless the theme has fewer hooks than the week has
picks, and speakers take turns. Weights and scores decide the order, and which
options make a week when there are more than it needs. Each week starts fresh,
from the numbers just updated.

## A week of picks

The Sunday job draws the week at about 04:00, after it recalculates the numbers
and moves to this week's theme. A small script of its own builds one picker,
seeded with the date, and calls `pick()` once per message: each reminder type on
each of the seven days, and the weekly message, 22 in all. The slot only says
which message takes the pick; every slot is drawn the same way.

The week is kept in `<Theme>-picks`, replaced each Sunday, by day and reminder:

<!-- prettier-ignore -->
```yaml
weekly: { hook: characters/detective, speaker: characters/detective }
2026-11-16:
  morning: { hook: scenes/stakeout, speaker: characters/assistant }
  afternoon: { hook: shared_lines/any_time, speaker: characters/detective }
```

A reminder reads its pick under today's date and its type, about 2 KB in all,
and runs no script. It copies the pick into its history entry's `picks`. A
message with no pick drawn for it, such as one written in chat, draws one live.

## What the reminder adds

When a reminder runs, it works out the `escalation` and `finishing_tasks` levels
from the facts it gathered, and adds its type for the writer to draw on. The
writer gets that, the pick, the facts, the root, and the entries for the hook
and the speaker. An evening in a theme like `Casebook`, its level names made up:

<!-- prettier-ignore -->
```yaml
reminder: evening
escalation: lecture
finishing_tasks: case_closed
hook: scenes/stakeout
speaker: characters/detective
tasks:
  - ABC-12 Hang the mirror, slipped 3 times
  - ABC-15 Return the drill, done
```

## The code

| Code             | What changes                                                                |
| ---------------- | --------------------------------------------------------------------------- |
| `Picker.pick()`  | Returns a `Pick`: a hook and a speaker, each an `Option`; next one per call |
| `Theme`          | Seeds one generator, for a lottery over the hooks and one over the speakers |
| `Lottery.draw()` | Sets its winner aside, and starts over once every candidate is drawn        |
| The week script  | New, beside the picker: one `Picker`, `pick()` per message, prints the week |

## Not decided here

- Whether a pick also names one line of its hook, drawn on Sunday.
- Whether the options file keeps its half-lives and its speaker rate.
- The names of the Sunday job's script and of `<Theme>-picks`.
