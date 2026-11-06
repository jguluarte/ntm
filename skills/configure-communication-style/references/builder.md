# The style profile

The body of `ntm-user:style`: what `ntm:configure-communication-style` writes and `ntm:style-message` reads. The `Profanity:` line and the headings exactly as shown, in this order; everything else is the user's, in their words. The builder writes every section; a section a handed-in profile lacks means its default, as `ntm:style-message` reads it.

## The shape

```
Profanity: <yes or no>

## Register
<two or three sentences, or "Plain." and one sentence on manner>

## What gets you to read
<the attention mechanism, in the user's words>

## When something keeps slipping
- <level 1 name> (the everyday one): <what it sounds like>
- <level 2 name> (after <n> earlier days): <what it sounds like>
<the climb rule, one line>

## Motifs
- <one recurring bit per line, each a short name>
Repeat limit: <not in the last eight messages, unless the user says otherwise>

## Off limits
What the style never rewrites or jokes about: ticket ids, titles, planned dates, counts and names are carried as given. <anything the user adds>

## Examples
- <level 1 name>: "<example>"
- <level 2 name>: "<example>"
- Nothing open: "<example>"
```

The quotes only mark where each example starts and ends.

## The sections, and what to ask

### Profanity

Is profanity allowed? `yes` or `no`. `ntm:style-message` allows it only on `yes`, in chat and in pushes alike.

### Register

Who is talking, what they sound like, what they never do; two or three sentences. For plain: `Plain.` and one sentence on manner (warm, dry, brisk). A plain register has no character: the message speaks as itself, and What gets you to read carries the line.

### What gets you to read

What makes them open a reminder instead of swatting it. Offer these, one line each, without favouring any; more than one can combine:

- brevity: one line, no ornament
- a curiosity hook: the message opens with a question or a fact
- warmth and encouragement
- humor: the joke is what gets it read
- a scoreboard: what's done this week
- a running bit or serial that continues from one day to the next
- surprise: a different form each day

Write the answer in their words, one or two lines, with anything it needs (what the serial is about).

### When something keeps slipping

What happens when the same ticket shows up day after day. The user's levels, in order, each with the name they give it and after how many earlier days it starts. The first level is the everyday one, for fresh work and work already planned for today; it carries no number. Write the number on every level after the first: a ticket's level is the last one whose number its count of earlier days has reached, and a count of 0 is always the first level. Offer these, one line each, without favouring any:

- the same every day: one level, no climb
- the same tone, plus a direct question: "what's in the way?"
- break it smaller: the message offers a split or a replan in chat
- harder each day: a level per day, in their names
- step back: go quiet on that ticket and raise it once in the weekly message
- a consequence they name themselves, said plainly when the day comes

Then the climb rule in one line, such as "harder each day a ticket carries over, back to the first level once it closes". An earlier day is a day before today on which a reminder mentioned the ticket; `ntm:style-message` counts them from the message history. Levels listed without numbers get 0, 1, 2… in order. The morning and evening reminders follow this section; the afternoon one never climbs.

### Motifs

Recurring bits a line can be built from, one per line: from the theme's world, or, with a plain register, from their own life (the pets, the house, the hobby, the commute). Propose a list; they add, cut and replace. Each is a short name the message history records exactly. With brevity, fewer is fine: each is a word the line can carry. Empty is fine too.

The repeat limit says how long a motif rests before it comes back: "not in the last eight messages" unless they say otherwise.

### Off limits

What the style never rewrites or jokes about. Ticket ids, titles, planned dates, counts and names are always carried as given; that sentence stays. Add whatever they name: a subject, a person, a kind of joke.

### Examples

One per level, in the level's name, and one for "nothing open" (the evening when everything closed: a win for the day, not the year). Ticket ids use the user's Ticket prefix from Board in `ntm-user:settings`, or the prefix settled earlier in this conversation, or `ABC-12` style when neither exists yet. The tasks in them are ordinary household ones. They show how each level lands, how long it runs, and how a motif ties to the subject. `ntm:style-message` borrows their energy and never their sentences.

## A plain example

The whole body, for a plain register with brevity as what gets read and three levels. The ids are the `ABC-12` style; nothing here goes into a user's profile as is.

```
Profanity: no

## Register

Plain. Brisk and friendly; says the thing and stops.

## What gets you to read

Brevity. One line, and the task is the first thing in it.

## When something keeps slipping

- Everyday (the everyday one): the task, nothing else.
- Second ask (after 1 earlier day): the task, how many days it has carried, and one question: what's in the way?
- Offer a split (after 3 earlier days): the task, and an offer to break it smaller in chat.
Back to Everyday once the ticket closes.

## Motifs

- the cat
- the garden
- the long walk
Repeat limit: not in the last eight messages.

## Off limits

What the style never rewrites or jokes about: ticket ids, titles, planned dates, counts and names are carried as given. Nothing about the neighbours.

## Examples

- Everyday: "Today: ABC-12, replace the porch bulb."
- Second ask: "ABC-12, replace the porch bulb, second day. What's in the way?"
- Offer a split: "ABC-12, replace the porch bulb, fourth day. Want to break it into smaller pieces? Say so and we'll do it now."
- Nothing open: "Nothing open. Good day; the cat agrees."
```
