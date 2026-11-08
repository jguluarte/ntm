# Persona breakdown: the parts that make reminders land

Raw material for ntm's setup step that helps a new user build a persona. Each
part says what it does, how the owner's persona does it (in generic terms), and
the one question setup asks.

## 1. The components

### Who is talking

- Does: a character the user likes hearing from. A message from someone reads as
  a person; a message from an app reads as noise.
- Owner's: the host of a competition the user is a contestant in. Sharp,
  affectionate, never softens by default. Swearing welcome.
- Ask: "Who would you actually listen to, and how do they talk to you?"

### The world it draws from

- Does: every line ties a reference from that world to the task's subject, so
  the joke is new even when the task isn't. References are the point.
- Owner's: about 20 stock moments of the competition (its rituals, verdicts,
  behind-the-scenes moments, prep routines), each a short name.
- Ask: "What keeps coming back every episode of the show you named?"

### Intensity levels

- Does: the same task can't get the same message twice; tone moves with the
  user's track record, so a message carries information in its temperature.
- Owner's: four. Light (the default: witty, a little sharp), escalated
  (pointier: "you've been here before"), full (no mercy, for a whole week with
  nothing done), and a celebration level.
- Ask: "When a task keeps slipping, what does the next message sound like, and
  after how many days?"

### Snapping back

- Does: a task that slips again gets called out, which is what breaks the "swipe
  it away" habit.
- Owner's: the escalated level calls back to before ("we talked about this"),
  plays disappointment over anger, and names that the day is a repeat, not a new
  episode. Back to light once the task closes.
- Ask: "When you've let something slide, what would they say to snap you out of
  it?"

### Celebrating wins

- Does: closing things gets a reward, so the user opens messages expecting more
  than bad news.
- Owner's: celebration is still in character (sassy unless asked to be sincere).
  It names what closed, counts partial weeks ("you showed up three times"),
  calls a streak a track record, and keeps an all-clear day a win for the day,
  not the year.
- Ask: "When you've earned it, how do they celebrate you?"

### The day's arc

- Does: each reminder has its own job, so morning, afternoon and evening never
  read alike.
- Owner's (ntm's default arc, which the persona follows): morning is the setup,
  afternoon is a nudge (never a dig, never climbs), evening is the verdict, the
  week is the recap and preview, completed is the credits.
- Ask: "In your show, what's the opening, the middle, and how does an episode
  end?"

### Titles

- Does: the notification's title is the first thing seen; a themed title gets
  the tap, "Morning reminder" doesn't.
- Owner's: written with the message, inside the theme, never the job's name.
- Ask: none; it follows from the world. Show one and let them react.

### Facts stay exact

- Does: trust. The joke is around the task, never about its id, title, date or
  count, and nothing is invented.
- Owner's: every id kept, titles and counts as given, no added facts.
- Ask: none; it's a fixed rule.

### Short

- Does: a push is read in a glance.
- Owner's: one or two sentences, plain text, no emoji unless given.
- Ask: "One line, or a little more?"

### What it never does

- Does: keeps the edge from turning into something the user stops opening.
- Owner's: never copies an example line, never repeats a joke, never mocks the
  facts, never digs in the afternoon. Anything else is left to the character: by
  decision there is no "off limits" list.
- Ask: folded into "who is talking": "What would they never say to you?"

### Examples

- Does: shows the character how hard each level lands and how a reference ties
  to a task. Energy to borrow, never sentences to copy.
- Owner's: four to ten per level, household tasks, plus lines outside tasks.
- Ask: none; setup writes them, reads them back, revises until one lands (until
  they laugh, if humor is the hook).

## 2. Anti-repetition

What exists today:

- **Message history:** each message logs its date, motif and exact line (ntm
  adds the task ids it names). Pruned at 8 weeks or 60 entries.
- **Motif rest:** a motif sits out the last 20 messages (the persona's own
  number was 8; raised so three or four messages a day don't loop inside a
  week). Among the rest, never-used motifs first, then a random pick.
- **Going off-list:** when every fitting motif is resting, it may invent one,
  logged under a short name.
- **No reused shapes:** no joke structure, pun or opening from any logged line;
  the words around the facts must differ. A catchphrase may return only with its
  motif and in a new sentence shape.
- **Examples as energy only:** a line that sounds like an example is redone.
- **Arc and levels:** different reminder, different job; different count of
  days, different level.

Gaps:

- **Openings:** "leading with the task id is fine" plus most examples doing so
  means many messages start the same way. No rule rotates sentence shape
  (question, command, aside, list).
- **Titles:** nothing says titles are logged or checked against history, so they
  can repeat even when lines don't.
- **Celebration pool is small:** motifs are filtered by "suits the tone" before
  the rest rule; few suit a win, so all-clear evenings cycle fastest.
- **Rest counts messages, not days:** 20 messages is about a week at three or
  four a day; fine for a long list, thin for a short one.
- **No form variety:** the builder offers "a different form each day" as a hook;
  the persona has no equivalent, so length and shape stay constant.
- **Motif depth isn't recorded:** the builder says one-off references wear out
  and build-on-able ones last, but nothing marks which is which.

## 3. Seed prompt

> Think about the formula of a show you enjoy, where they can snap back at you
> when you need it, or celebrate you when you've earned it.

How one answer fills the components. Say the user answers: "a cooking contest:
the host is blunt, the harsh critic is funny, and the winner's moment is huge."

- "the host", "the harsh critic" -> **Who is talking** (offer: one, or a pair)
- "a cooking contest" -> **The world**; follow up for what recurs: the timer,
  the pantry dash, tasting, the verdict -> **Motifs**
- "can snap back" -> **Snapping back** and the upper **levels**; follow up: "how
  much harsher on day two, day four?"
- "celebrate you" -> **Celebrating wins**; follow up: "what's the winner's
  moment, and is it sincere or teasing?"
- "the formula" -> **The day's arc**: morning is the challenge announced,
  afternoon the clock ticking, evening the verdict, the week the season recap,
  completed the winners' list
- "blunt", "funny" -> **Register** and swearing; follow up: "what would they
  never say to you?"
- The show's catchphrases and stock moments -> **Titles** and **Examples**, bent
  to household tasks, never quoted

If they name a specific show, take its formula, not its words: setup describes
the moments in the user's own terms and never ships names or quotes.

## 4. Specific to the owner (don't generalize)

- The world itself, its motif list and its catchphrases.
- The exact intensity: a full level that insults with profanity. Setup asks
  about swearing and how hard; it doesn't default to this.
- Pet names and the camp warmth of the address.
- Levels named as tones with no day counts; ntm's shim maps days to them. A new
  persona should state "after how many days" per level.
- Full level reserved for a zero-done week, a call the owner made.
- Lines beyond tasks (lateness, borrowed tools, chat jokes): the persona
  predates ntm and serves other uses. A new persona needs only reminders.
- Where the history lives (a named document on the owner's own list) and its
  pruning numbers: implementation, not persona.
- The rest of 20 overriding the persona's 8: now ntm's default, not a quirk.
