# Picks

A sketch to answer line by line: what the picker gives the writer, and how a
week of picks is drawn ahead.

A pick is the theme's side of one message: two pieces of the theme, a
perspective the message is told from and a reference it works in. The day's side
comes from the reminder when it runs.

## A pick

| Piece         | What it is                                 | What the writer does with it                 |
| ------------- | ------------------------------------------ | -------------------------------------------- |
| `perspective` | A speaker, or a reference that carries one | Tells the message from its point of view     |
| `reference`   | A second piece, from another pool          | Works it in: the setting, a callback, a line |

A speaker is someone in the theme's world who talks in a manner of their own. A
reference is any other piece of the world a message draws on: a scene it is set
in, a moment it calls back to, a line anyone can say.

The perspective is usually a speaker, and sometimes a reference that carries one
because it brings its own onlookers: a challenge, an audience, the morning
paper. The pick's reference is a second piece, from another pool. A speaker is
only ever drawn as the perspective, so their lines stay in their own mouth. A
pool's `roles` in the options file say whether its entries can be the
perspective, the pick's reference or both; a pool of speakers adds `speaker`.

A piece whose entry holds lines or riffs brings one of them, drawn with it. A
pick holds no levels, no reminder type and no tasks.

## The groupings

At the theme's `speaker_rate`, the perspective is a speaker; otherwise it is a
reference that carries one. The two pieces come from different pools, so a
message is never set in two scenes, or calls back two moments. In a theme of
speakers, scenes, moments and lines anyone can say, a speaker comes with any of
the three, and a scene with a moment or a line. Examples from a real theme,
`Dragify`:

| Perspective                | Reference                    | The message                                          |
| -------------------------- | ---------------------------- | ---------------------------------------------------- |
| `actors/michelle_visage`   | `motifs/the_critiques`       | Michelle gives the task the note it has heard before |
| `actors/bianca_del_rio`    | `references/party_city`      | Bianca sends the rushed job back to the costume rack |
| `motifs/reading_challenge` | `references/season_1_filter` | The other tasks read it; the haze hides its age      |
| `motifs/untucked`          | `any_actor_lines/any_time`   | Backstage, the open task asks: "Am I the drama?"     |

## Variety

Each option counts once, at its weight and score, so a pool with more options
comes up more often. A drawn piece then rests: its chance drops, and regains
half of what it lost over its pool's half-life; a drawn line rests over its
entry's half-life. A week is drawn in order, so each pick rests on those before
it as well as on the history.

## A week of picks

The Sunday job draws the week at about 04:00, after it recalculates the numbers
and moves to this week's theme. A small script of its own builds one picker,
seeded with the date, and calls `pick()` 25 times: the week's 22 messages, three
reminders a day and the weekly one, and 3 spare for messages written in chat.

`<Theme>-picks` keeps them as one list, in order, beside the theme's other files
in the user's backend, replaced each Sunday:

<!-- prettier-ignore -->
```yaml
- perspective: { option: characters/detective, line: File it under closed. }
  reference: { option: scenes/stakeout }
- perspective: { option: scenes/stakeout }
  reference: { option: shared_lines/any_time, line: Everyone here is lying. }
```

Every message, a reminder, the weekly one or one written in chat, takes the
first pick and saves the list without it: one small read and one small write, no
script, and the list shows what is left. It copies the pick into its history
entry's `picks`. If the list runs out before Sunday, a message runs the picker
for its own.

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
reference: { option: scenes/stakeout }
tasks:
  - ABC-12 Hang the mirror, slipped 3 times
  - ABC-15 Return the drill, done
```

## The code

| Code            | What changes                                                                           |
| --------------- | -------------------------------------------------------------------------------------- |
| `Picker.pick()` | Returns the perspective and the reference, each an `Option` with its drawn line        |
| `Theme`         | Reads `roles` as `perspective`, `reference` and `speaker`; draws a speaker at the rate |
| `Option`        | Its draw weight drops while it rests, from its last use                                |
| The week script | New, beside the picker: one `Picker`, `pick()` per message, prints the week            |
