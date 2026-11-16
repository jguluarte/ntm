# Picks

A sketch to answer line by line: what the picker gives the writer, and how a
week of picks is drawn ahead.

A pick is the theme's side of one message: two pieces of the theme, one giving
the message its perspective and one adding flavor. The day's side comes from the
reminder when it runs.

## A pick

| Piece         | What it is                                 | What the writer does with it                 |
| ------------- | ------------------------------------------ | -------------------------------------------- |
| `perspective` | A speaker, or a reference that carries one | Tells the message from its point of view     |
| `flavor`      | A reference from another pool              | Works it in: the setting, a callback, a line |

A speaker is someone in the theme's world who talks in a manner of their own. A
reference is any other piece of the world a message draws on: a scene it is set
in, a moment it calls back to, a line anyone can say.

A speaker is always the perspective, so their lines stay in their own mouth. A
reference carries a perspective when it brings its own onlookers: a scene with
people in it, an audience, the morning paper. Any reference can add flavor. A
pool's `roles` in the options file say which of these its entries can be.

A piece whose entry holds lines or riffs brings one of them, drawn with it. A
pick holds no levels, no reminder type and no tasks.

## The groupings

At the theme's `speaker_rate`, the perspective is a speaker; otherwise it is a
reference that carries one. The flavor comes from any other pool, so a message
is never set in two scenes, or calls back two moments. In a theme of speakers,
scenes, moments and lines anyone can say, a speaker comes with any of the three,
and a scene with a moment or a line. Examples from a real theme, `Dragify`:

| Perspective                | Flavor                       | The message                                          |
| -------------------------- | ---------------------------- | ---------------------------------------------------- |
| `actors/michelle_visage`   | `motifs/the_critiques`       | Michelle gives the task the note it has heard before |
| `actors/bianca_del_rio`    | `references/party_city`      | Bianca sends the rushed job back to the costume rack |
| `motifs/reading_challenge` | `references/season_1_filter` | The other tasks read it; the haze hides its age      |
| `motifs/untucked`          | `any_actor_lines/any_time`   | Backstage, the open task asks: "Am I the drama?"     |

## Variety

Each option counts once, at its weight and score, so a pool with more options
comes up more often. A drawn piece then rests: its chance drops, and wins back
half of what it lost over its pool's half-life; a drawn line rests over its
entry's. A week is drawn in order, so each pick rests on those before it as well
as on the history.

## A week of picks

The Sunday job draws the week at about 04:00, after it recalculates the numbers
and moves to this week's theme. A small script of its own builds one picker,
seeded with the date, and calls `pick()` once per message: each reminder type on
each of the seven days, and the weekly message, 22 in all. The slot only says
which message takes the pick; every slot is drawn the same way.

The week is kept in `<Theme>-picks`, replaced each Sunday, by day and reminder:

<!-- prettier-ignore -->
```yaml
weekly:
  perspective: { option: scenes/stakeout }
  flavor: { option: shared_lines/any_time, line: Everyone here is lying. }
2026-11-16:
  morning:
    perspective: { option: characters/detective, line: File it under closed. }
    flavor: { option: scenes/stakeout }
```

A reminder reads its pick under today's date and its type, about 3 KB in all,
and runs no script. It copies the pick into its history entry's `picks`. A
message with no pick drawn for it, such as one written in chat, draws one live.

## What the reminder adds

When a reminder runs, it works out the `escalation` and `finishing_tasks` levels
from the facts it gathered, and adds its type for the writer to draw on. The
writer gets that, the pick, the facts, the root, and the entries for both
pieces, each with only its drawn line. An evening in a theme like `Casebook`,
its level names made up:

<!-- prettier-ignore -->
```yaml
reminder: evening
escalation: lecture
finishing_tasks: case_closed
perspective: { option: characters/detective, line: File it under closed. }
flavor: { option: scenes/stakeout }
tasks:
  - ABC-12 Hang the mirror, slipped 3 times
  - ABC-15 Return the drill, done
```

## The code

| Code            | What changes                                                                        |
| --------------- | ----------------------------------------------------------------------------------- |
| `Picker.pick()` | Returns the perspective and the flavor, each an `Option` with its drawn line        |
| `Theme`         | Reads `roles` as `speaker`, `perspective` and `flavor`; draws a speaker at the rate |
| `Option`        | Its draw weight drops while it rests, from its last use                             |
| The week script | New, beside the picker: one `Picker`, `pick()` per message, prints the week         |
