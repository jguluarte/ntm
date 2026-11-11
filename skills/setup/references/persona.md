# Building a persona

The persona is the character behind the user's reminders. It lives in their
`%Style` database, built from ntm's template, `references/databases/style.md`,
and `ntm:style` reads it before every message.

Push for a character they enjoy: a plain reminder is easy to swipe away. You
propose each part in the character's terms, they react, and you rewrite until it
sounds like the character.

## A new persona

Build each part under the template's heading, in its order, with the headings
exactly as written. Everything under a heading is the user's, in their words.

### Register

Who is talking, and how they talk to the user. Take the character they picked
and ask how it reacts when something slides, how it celebrates a win, and what
it would never say. Ask how hard it goes: swearing, shade, roasting, whatever
they want. Write it in two or three sentences.

### What motivates you to read reminders from ntm

What gets them to open a reminder instead of swiping it away, and how long a
message runs. Offer a few; more than one can combine:

- humor: the joke is what gets it read
- brevity: one line, the task first
- a running bit that continues from one day to the next
- a scoreboard of what's done this week
- surprise: a different form each day

### The reminders

A day of reminders follows an episode, and a week follows a season. Propose what
each reminder is in the character's world, one line under each subsection, and
let them rename or cut:

- Morning: the preview of what's ahead, with a quick recap when something
  carried over from yesterday.
- Afternoon: the first half of the episode, the nudge.
- Evening: how the episode ends.
- Week: the season preview, with last week in a breath.
- Completed: the credits, what got done.

Take the arc from what they picked: a contest has a challenge and a verdict, a
serial has a cold open and a cliffhanger.

### Responding to procrastination

How the messages change when a task keeps carrying over. Start from what they
said they need when they're slacking off: shame, a cheerleader, a demon to stalk
them. Build the levels from it in the character's words, each with its name and
after how many earlier days it starts, then the climb rule in a line. One level,
the same every day, is a complete answer.

### Motifs

Recurring bits a line can be built from: from the character's world, or from the
user's life (the pets, the house, the commute). Each gets a short name, which
`%Message-history` records exactly.

Push for a few weeks' worth of variety. A motif that is only a reference wears
out in a week; one that can be built on lasts: a running scene that advances, a
catchphrase that bends to the subject, a recurring character who reacts to the
day. Ask what comes back every episode in what they picked, and propose a list
from it; they add, cut and replace. Set the `Repeat limit:` line from how far
the list stretches.

### Examples

One per level and one for nothing open, with ordinary household tasks and ids
like `ABC-12`. Write them, read them back, and revise until each is one they'd
open; with humor, until they laugh.

## Their own persona

A user who already has a persona (a skill, a prompt, a page of notes) keeps it
word for word, task ids included, in place of the template's Profile. A pasted
skill's frontmatter is dropped.

Above it, write a `## For ntm` section from how the persona names things, as the
A persona section of `ntm:style`'s `references/persona-contract.md` says. Show
them the section; they confirm. Nothing else is added: the persona's own levels
and motifs stand.

## Before saving

Show them the whole persona and take one round of corrections.
