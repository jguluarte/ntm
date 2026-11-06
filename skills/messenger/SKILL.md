---
name: messenger
description: Sets up or revises the messenger profile that nudge:voice writes every reminder from, with the user in chat, and saves it to the board as the messenger note; with --import, builds it from a persona skill they already have. Run when the user says "set up the messenger", "change the messenger", "make it meaner", "make it softer", "make it shorter", "the reminders aren't landing" or "import my persona"; nudge:setup runs it during onboarding.
---

# nudge:messenger

The messenger is whoever reaches the user: every reminder is written from its profile. The profile lives on the board, in the note named by the config's `messenger note`, in the format of `references/template.md`, five sections: Voice, What gets you to read, When something keeps slipping, Motifs, Examples. This skill writes that note with the user, in short rounds: you bring proposals, they react. Never hand them a form.

## Usage

```
/nudge:messenger [--import <skill text or description>]
```

- Without a flag: set up a new profile through the rounds below, or revise the one on the board.
- `--import`: build the profile from a persona skill the user already has, without the interview. The argument is the skill's text, pasted or read from a file, or a description of it when the text isn't to hand; the job prompts from an earlier, skills-based version of this system (account skills plus scheduled tasks) can come with it, and the escalation policy is read from them. See With `--import`.

Read `references/template.md` once before starting.

## Before you start

Load `nudge:board` and read the note with the adapter's `read note` on the config's `messenger note`. When `nudge:setup` runs this skill, don't load `nudge:board`: setup says which board, ticket prefix and note name to use and which adapter file to read; read and write through that file.

- **Missing:** a new profile. Take the rounds in order.
- **Present:** a revision. Say what's there in a line or two, ask what they want different, and go to the round that owns it. "Meaner" or "softer" is the Voice round and the Examples round for the tones it touches. "Shorter" is What gets you to read and the Examples. "The reminders aren't landing" starts at What gets you to read, then When something keeps slipping: one of those two is what's failing. Motifs stay unless they ask.

## With `--import`

The user has a persona skill: a skill that rewrites messages in a character's voice, with its own rules, a theme list and example lines. The profile comes from it, section by section, instead of from the rounds. Fill each section from the skill, and say in a line what it came from; ask only where the skill has nothing:

- **Voice:** who is talking, what they sound like, what they never do, from the skill's persona and its rules. `Profanity:` from its wording: `yes` when it welcomes or allows profanity, `no` when it forbids it; ask when it says nothing.
- **What gets you to read:** humor, when the skill is a comedic voice. The skill never says so in those words, so say that's what you read into it and let them correct. Otherwise offer round 2's list.
- **When something keeps slipping:** from the old job prompts when they're given (they say what the day count does: after how many days, and what happens then); otherwise harder each day, when the skill has an escalation ladder (tones that get pointier the longer something sits). Otherwise offer round 3's list.
- **Motifs:** the skill's theme list, each name exactly as listed, so an existing voice history still counts against them.
- **Examples:** the skill's example sections, grouped by tone: its lightest tone under Light, the next under Escalated, its hardest under Harsh (only when the policy is harder each day), its affirmation under Affirmation, and anything about things that aren't tasks under Beyond tasks. The lines stay as they are, ticket ids included.
- **Name:** asked once, as in The name below.

Then write the note (Saving), show the profile, and take one round of corrections: they say what's off, you fix it and save again. From then on, changes go through the rounds as a revision.

## The rounds

Each round is a proposal they edit, a few lines long.

### 1. Voice

Who is talking. Offer a few directions, in one line each, without favoring any: a drill sergeant, a disappointed butler, a sports commentator, a nature-documentary narrator, a passive-aggressive roommate, a noir detective, a game-show host, or plain: no character, the messenger speaks as itself. Or none at all: reminders arrive as the jobs write them. During setup that's `voice on` = `no`, and this skill ends; afterwards, the config's `voice on` is the switch.

Then two or three sentences: who is talking, what they sound like, what they never do. For plain, one sentence on manner is enough (warm, dry, brisk). Ask whether profanity is allowed (`Profanity: yes` or `no`).

### 2. What gets you to read

What makes them open a reminder instead of swatting it. Offer these, one line each, without favoring any; more than one can combine:

- brevity: one line, no ornament
- a curiosity hook: the message opens with a question or a fact
- warmth and encouragement
- humor: the joke is what gets it read
- a scoreboard: what's done this week
- a running bit or serial that continues from one day to the next
- surprise: a different form each day

Write their answer in their words, one or two lines, with anything it needs: what the serial is about.

### 3. When something keeps slipping

What the messenger does when the same ticket shows up day after day. Offer these, one line each, without favoring any:

- the same tone, plus a direct question: "what's in the way?"
- break it smaller: the message offers a split or a replan in chat
- harder each day
- step back: go quiet on that ticket and raise it once in the weekly recap
- a consequence they name themselves, said plainly when the day comes

One policy, in their words, with whatever it needs: after how many days it starts, what the question is, what the consequence is. This section decides what the morning and evening reminders do with a ticket's history; `nudge:voice` reads it.

### 4. Motifs

15–25 recurring bits, one line each, that lines can be built from: from the voice's world, or, when the voice is plain, from their own life (the pets, the house, the hobby, the commute). Propose a list; they add, cut and replace. Each is a short name the voice history can record exactly. With brevity, fewer is fine: each is a word the line can carry.

### 5. Examples

Three or four per tone, from the profile: light, escalated, affirmation, a few beyond tasks, and harsh only when the policy in round 3 is harder each day. Ticket ids use the config's `ticket prefix` (`HOME-12` style) and the tasks are ordinary household ones. With a plain voice the examples show the attention mechanism at work instead of a character. Write them, read them back, revise: if they chose humor, until they laugh at least once; otherwise, until each reads like something they'd open. The template's illustrations show how each tone lands, in a stand-in voice; borrow the register, never a line.

## The name

For a new profile, ask what they'll call the messenger, since that's how they'll invoke it in chat ("run that through the Butler"). During setup, record it for the config's `messenger name`. The note's `Name:` line holds it; a revision keeps the name unless they ask to change it.

## Saving

Write the note with the adapter's `write note` to the config's `messenger note`, in the template's format, headings as given. `write note` creates it on the first save. The next reminder uses it.

## Result

One line: `Messenger saved: <name>`, or `Messenger FAILED: <why>` when the note can't be written.
