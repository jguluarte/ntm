# The style profile

A user-defined persona skill keeps its own rules for all of this; none of the sections below are asked of it (see User-defined persona in `ntm:configure-style`). This page is for a profile built from scratch.

The Profile half of `ntm-user:style`: what `ntm:configure-style` writes with the user, and what the procedure half of that skill reads. The `Profanity:` line and the headings exactly as shown, in this order; everything else is the user's, in their words. The builder writes every section; a section left empty means its default, as the procedure reads it.

## The shape

```
Profanity: <yes or no>

### Register
<two or three sentences, or "Plain." and one sentence on manner>

### What gets you to read
<the attention mechanism, in the user's words>

### The reminders
<morning, afternoon, evening, week, completed: what each is in the theme's terms, one line each; or empty for the defaults>

### When something keeps slipping
- <level 1 name> (the everyday one): <what it sounds like>
- <level 2 name> (after <n> earlier days): <what it sounds like>
<the climb rule, one line>

### Motifs
- <one recurring bit per line, each a short name>
Repeat limit: <not in the last twenty messages, unless the user says otherwise>

### Off limits
What the style never rewrites or jokes about: ticket ids, titles, planned dates, counts and names are carried as given. <anything the user adds>

### Examples
- <level 1 name>: "<example>"
- <level 2 name>: "<example>"
- Nothing open: "<example>"
```

The quotes only mark where each example starts and ends.

## The sections, and what to ask

### Profanity

Whether swearing is fine: `yes` or `no`. Asked once, with the Register.

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

### The reminders

A day of reminders has the shape of an episode, and a themed style gets to say what each moment is in its own world. Propose the five in the theme's terms, one line each, and let them rename or cut:

- **morning** is the setup: the preview of what's ahead, and a look back only when something slipped into today (a recap that exists only when there's something to recap).
- **afternoon** is the middle: the task in progress, the nudge. Never the judgement.
- **evening** is how it ended: good, bad, or to be continued.
- **week** is the recap and what's coming: last week in a breath, then next week set up.
- **completed** is the credits: what got done, named.

A contest has a challenge, a verdict and an elimination; a serial has a cold open, an act break and a cliffhanger; a shift has a briefing, the floor and the debrief. Ask what they like (a show, a genre, a game) and take the arc from that, in their words; the file itself names nothing. With a plain register, leave the section empty: the defaults are the plain versions above.

### When something keeps slipping

What happens when the same ticket shows up day after day. The user's levels, in order, each with the name they give it and after how many earlier days it starts. The first level is the everyday one, for fresh work and work already planned for today; it carries no number. Write the number on every level after the first: a ticket's level is the last one whose number its count of earlier days has reached, and a count of 0 is always the first level. Offer these, one line each, without favouring any:

- the same every day: one level, no climb
- the same tone, plus a direct question: "what's in the way?"
- break it smaller: the message offers a split or a replan in chat
- harder each day: a level per day, in their names
- step back: go quiet on that ticket and raise it once in the weekly message
- a consequence they name themselves, said plainly when the day comes

Discuss it with them; the offers above are starting points, not the menu. Then the climb rule in one line, such as "harder each day a ticket carries over, back to the first level once it closes". An earlier day is a day before today on which a reminder mentioned the ticket; the procedure counts them from the message history. Levels listed without numbers get 0, 1, 2… in order. The morning and evening reminders follow this section; the afternoon never climbs.

### Motifs

Recurring bits a line can be built from, one per line: from the theme's world, or, with a plain register, from their own life (the pets, the house, the hobby, the commute). Propose a list; they add, cut and replace. Each is a short name the message history records exactly. With brevity, fewer is fine: each is a word the line can carry. Empty is fine too.

Variety comes from two things, so talk about both: how many motifs there are, and how many ways one can be used. A motif that is only a reference wears out in a week; one that can be built on (a running scene that advances, a catchphrase that bends to the subject, a recurring character who reacts to the day) gives many lines. Ask them to name something they like, a show, a genre, a game, a sport, and use it as the analogy for how its recurring bits work: what comes back every episode, how a running gag gets a new turn, what the stock moments are. Tailor the list to that, in the user's words; nothing here names anything.

The repeat limit says how long a motif rests before it comes back. Set it with them, from the list's size and how far each motif stretches: a short list of one-use references needs a long rest; a few rich ones can come back sooner. "Not in the last twenty messages" is the default when they don't say.

### Off limits

What the style never rewrites or jokes about. Ticket ids, titles, planned dates, counts and names are always carried as given; that sentence stays. Add whatever they name: a subject, a person, a kind of joke.

### Examples

One per level, in the level's name, and one for "nothing open" (the evening when everything closed: a win for the day, not the year). Ticket ids use the user's Ticket prefix from Todo list in `ntm-user:settings`, or the prefix settled earlier in this conversation, or `ABC-12` style when neither exists yet. The tasks in them are ordinary household ones. They show how each level lands, how long it runs, and how a motif ties to the subject. The procedure borrows their energy and never their sentences.

## A plain example

The whole Profile, for a plain register with brevity as what gets read and three levels. The ids are the `ABC-12` style; nothing here goes into a user's profile as is.

```
Profanity: no

### Register

Plain. Brisk and friendly; says the thing and stops.

### What gets you to read

Brevity. One line, and the task is the first thing in it.

### The reminders

### When something keeps slipping

- Everyday (the everyday one): the task, nothing else.
- Second ask (after 1 earlier day): the task, how many days it has carried, and one question: what's in the way?
- Offer a split (after 3 earlier days): the task, and an offer to break it smaller in chat.
Back to Everyday once the ticket closes.

### Motifs

- the cat
- the garden
- the long walk
Repeat limit: not in the last twenty messages.

### Off limits

What the style never rewrites or jokes about: ticket ids, titles, planned dates, counts and names are carried as given. Nothing about the neighbours.

### Examples

- Everyday: "Today: ABC-12, replace the porch bulb."
- Second ask: "ABC-12, replace the porch bulb, second day. What's in the way?"
- Offer a split: "ABC-12, replace the porch bulb, fourth day. Want to break it into smaller pieces? Say so and we'll do it now."
- Nothing open: "Nothing open. Good day; the cat agrees."
```
