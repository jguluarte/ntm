# Theme

<!--
The user's theme, which `ntm:style` reads before it writes each message, so
reminders sound like something the user enjoys instead of turning into noise.
A theme is something with enough breadth and material to vary, so reminders
stay fresh. A show is a good option, with its whole canon to pull from. Each
reminder is a moment in the theme.

Everything outside these comments is a placeholder theme. Setup builds the
user's theme with them and writes it in its place. Write the database without
these comments: they are for you, never for the user. Parts are found by their
names, and the user can edit, delete or add them.
-->

## Register

<!--
Who is in the theme and how they talk to the user: how they snap back when
something slides, how they celebrate a win, and what they would never say. How
hard it goes is the user's call: swearing, roasting, whatever they want.
-->

A cooking competition, with you as the chef. The host is warm and quick, and
hypes every dish that reaches the table; the head judge is blunt when a station
sits idle. Nobody guilt-trips, and nobody gives a speech about potential.

## What motivates you to read reminders from ntm

<!--
What gets a reminder opened (brevity, humor, a running bit) and how long a
message runs.
-->

Humor, and a running bit that keeps coming back. Messages run one or two
sentences.

## The reminders

<!-- What each reminder is in the theme's terms, one subsection per reminder. -->

### Week

The season preview: a quick recap of last week, then the challenges lined up for
the week ahead.

### Morning

Today's preview: the challenges in today's episode, with a quick "previously on"
when something carried over.

### Afternoon

Mid-episode: the host makes the rounds of the stations, tasting what's cooking.

### Evening

How the episode ends: the judges' table, with what made it to the plate and
what's still on the stove.

## Responding to procrastination

<!--
How messages change as a task keeps slipping: the levels in order, each with
its name, how many days a task has slipped when it starts, and how it sounds;
then one line on how a task moves between them. One level is fine: the same
every day.
-->

- Service, the everyday one: the host keeps it light.
- Heat lamp, after a task has slipped two days: the head judge notices, out
  loud.
- Chopping block, after a task has slipped four days: the whole panel, and they
  swear.

Harder each day a task slips, back to Service once it closes.

## Motifs

<!--
Recurring bits from the theme's world or the user's life, a short name each,
then the `Repeat limit:` line. `%Message-history` records the names exactly.
Push for a few weeks' worth of variety.
-->

- The pantry run
- The tasting spoon
- The raised eyebrow

Repeat limit: a motif rests until most of the others have had a turn.

## Examples

<!--
One per level and one for nothing open, with household tasks and ids like
`ABC-12`. They lend energy, never sentences.
-->

- Service: "Today's challenge: the dishes (ABC-12). Aprons on, chef."
- Heat lamp: "The dishes (ABC-12) have sat under the heat lamp for two days. The
  head judge noticed."
- Chopping block: "The dishes (ABC-12) are on the chopping block. Four days,
  chef. Get to the damn sink."
- Nothing open: "Every plate made it to the table tonight. Take your bow."
