# The style profile

The Profile is what the user told you about how their reminders should talk,
written down in a fixed shape. It is one half of `ntm-user:style`; the other
half, the procedure, reads it each time it writes a message.
`ntm:configure-style` builds it with the user from this page, for plain or a
theme. A persona skill keeps its own rules, and none of this is asked of it.

Write the `Profanity:` line and the headings exactly as shown, in this order,
even when a section stays empty: an empty section means its default. Everything
else is the user's, in their words.

## The shape

```
Profanity: <yes or no>

### Register
<two or three sentences, or "Plain." and one sentence on manner>

### What gets you to read
<the attention mechanism, in the user's words>

### The reminders
<morning, afternoon, evening, week, completed: what each is in the theme's
terms, one line each; or empty for the defaults>

### When something keeps slipping
- <level 1 name> (the everyday one): <what it sounds like>
- <level 2 name> (after <n> earlier days): <what it sounds like>
<the climb rule, one line>

### Motifs
- <one recurring bit per line, each a short name>
Repeat limit: <not in the last twenty messages, unless the user says otherwise>

### Examples
- <level 1 name>: "<example>"
- <level 2 name>: "<example>"
- Nothing open: "<example>"
```

The quotes only mark where each example starts and ends.

## The sections

What each section means and what to ask for it. Plain and a theme go through the
same sections; where they differ, the section says.

### Profanity

Whether swearing is fine: `yes` or `no`. Ask once, with the Register.

### Register

For a theme: who is talking, what they sound like, what they never do; two or
three sentences. For plain: `Plain.` and one sentence on manner (warm, dry,
brisk), in their words. A plain register has no character: the message speaks as
itself, and What gets you to read carries the line.

### What gets you to read

What makes them open a reminder instead of swatting it away. Offer these, one
line each, none favoured; more than one can combine:

- brevity: one line, no ornament
- a curiosity hook: the message opens with a question or a fact
- warmth and encouragement
- humor: the joke is what gets it read
- a scoreboard: what's done this week
- a running bit or serial that continues from one day to the next
- surprise: a different form each day

Write their answer in one or two lines, with anything it needs (what the serial
is about).

### The reminders

A day of reminders has the shape of an episode:

- **morning** is the setup: the preview of what's ahead, and a look back only
  when something slipped into today.
- **afternoon** is the middle: the task in progress, the nudge. Never the
  judgement.
- **evening** is how it ended: good, bad, or to be continued.
- **week** is the recap and what's coming: last week in a breath, then next week
  set up.
- **completed** is the credits: what got done, named.

For plain, leave the section empty: these are the defaults.

For a theme, propose what each of the five is in the theme's world, one line
each; they rename or cut. Ask what they like (a show, a genre, a game) and take
the arc from that, in their words. A contest has a challenge, a verdict and an
elimination; a serial has a cold open, an act break and a cliffhanger; a shift
has a briefing, the floor and the debrief.

### When something keeps slipping

What happens when the same task shows up day after day. An earlier day is a day
before today on which a reminder mentioned the task; the procedure counts them
from the message history.

Offer these, one line each, none favoured. They're starting points, not the
menu: talk it through.

- the same every day: one level, no climb
- the same tone, plus a direct question: "what's in the way?"
- break it smaller: the message offers a split or a replan in chat
- harder each day: a level per day, in their names
- step back: go quiet on that task and raise it once in the weekly message
- a consequence they name themselves, said plainly when the day comes

One level is a complete answer. For more, write their levels in order, each with
its name and after how many earlier days it starts. The first level is the
everyday one, for fresh work and work already planned for today; it carries no
number. Write the number on every level after it. Levels written without numbers
count as 0, 1, 2… in order.

A task's level is the last one whose number its count of earlier days has
reached; a count of 0 is always the first level.

Then write the climb rule in one line, such as "harder each day a task carries
over, back to the first level once it closes". The morning and evening reminders
follow this section; the afternoon never climbs.

### Motifs

Recurring bits a line can be built from, one per line, each a short name the
message history records exactly. For a theme they come from the theme's world;
for plain, from the user's own life (the pets, the house, the hobby, the
commute). Propose a list; they add, cut and replace. Empty is fine. With
brevity, fewer is fine: each is a word the line can carry.

For a theme, talk about variety: how many motifs there are, and how many ways
each can be used. A motif that's only a reference wears out in a week; one that
can be built on (a running scene that advances, a catchphrase that bends to the
subject, a recurring character who reacts to the day) gives many lines. Ask them
to name something they like (a show, a genre, a game, a sport) and use how its
recurring bits work as the model: what comes back every episode, how a running
gag gets a new turn, what the stock moments are. Fit the list to that, in their
words.

The repeat limit is how long a motif rests before it comes back. The default is
"not in the last twenty messages"; plain keeps it unless they say otherwise. For
a theme, set it with them from the list's size and how far each motif stretches:
a short list of one-use references needs a long rest; a few rich ones can come
back sooner.

### Examples

One per level, under the level's name, and one for "nothing open": the evening
when everything closed, a win for the day, not the year. Use generic task ids,
like `ABC-12`, and ordinary household tasks.

Each example shows how its level lands and how long it runs. Together they show
how a motif ties to the subject, and what gets the user to read at work. The
procedure borrows their energy, never their sentences.

For a theme, write them, read them back and revise: with humor, until they laugh
at least once; otherwise until each reads like something they'd open.

## A plain example

A whole Profile: plain register, brevity, three levels. Nothing here goes into a
user's profile as is.

```
Profanity: no

### Register

Plain. Brisk and friendly; says the thing and stops.

### What gets you to read

Brevity. One line, and the task is the first thing in it.

### The reminders

### When something keeps slipping

- Everyday (the everyday one): the task, nothing else.
- Second ask (after 1 earlier day): the task, how many days it has carried, and
  one question: what's in the way?
- Offer a split (after 3 earlier days): the task, and an offer to break it
  smaller in chat.
Back to Everyday once the task closes.

### Motifs

- the cat
- the garden
- the long walk
Repeat limit: not in the last twenty messages.

### Examples

- Everyday: "Today: replace the porch bulb (ABC-12)."
- Second ask: "Replace the porch bulb (ABC-12), second day. What's in the way?"
- Offer a split: "Replace the porch bulb (ABC-12), fourth day. Want to break it
  into smaller pieces? Say so and we'll do it now."
- Nothing open: "Nothing open. Good day; the cat agrees."
```
