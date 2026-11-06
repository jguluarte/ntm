---
name: voice
description: Rewrites a message the way the user's messenger profile says it gets read, in the profile's voice, with the tone given as a freeform description, and returns it. Used by the messenger agent for every reminder, and in chat when the user asks for a message in their messenger's voice.
---

# nudge:voice

The messenger is the one named by the config's `messenger name`. Its profile lives on the board, in the note named by the config's `messenger note`, written by `nudge:messenger` in the format of that skill's `references/template.md`: Voice (who is talking), What gets you to read (the attention mechanism), When something keeps slipping (the escalation policy), Motifs and Examples.

## Usage

```
/nudge:voice [--stay-fresh] [--for morning|afternoon|evening|week] ["tone"] message
```

- `message` is the text or idea to rephrase. In chat, whatever the user asks to put in the messenger's voice is the message, and anything they say about how is the tone. Naming the messenger alone isn't a tone. The skill returns plain text; callers add any links, lists or stats around it.
- `tone` is freeform: how to rephrase the message, and why. For example "escalated: still open from yesterday" or "light: always late to brunch". Without one, use light.
- `--stay-fresh`: for scheduled runs, which keep lines fresh with a shared history.
- `--for <beat>`: for scheduled runs; one of the four beats below. Implies `--stay-fresh` and adds a `Subject:` line. The caller names its job first in the tone (`Morning plan; …`).

## The profile

Load `nudge:board` and read the profile with the adapter's `read note` on the config's `messenger note`. With `--stay-fresh`, read the history beside it (next section).

If the config's `voice on` is `no`, or the note is missing, the voice is off. With `--for`, return the message as given plus `Subject: <job name>` as the last line, with the job name the caller gave. Without it, say in one line that the voice is off and why (the config, or the missing note). Nothing else below applies.

**Voice.** The profile's Voice is who talks. A plain voice has no character: the messenger speaks as itself, in the manner the section gives, and the mechanism below carries the line.

**What gets you to read** shapes every line. Follow what the profile says, as it combines them:

- brevity: one line, no ornament; the motif, if any, is a word, not a bit
- a curiosity hook: open with a question or a fact from the message itself, before the ask
- warmth and encouragement: on their side, never a dig; the ask comes after the regard
- humor: the joke is what gets it read
- a scoreboard: lead with the count the tone gives (what's done this week); never compute or invent one
- a running bit or serial: continue the bit from the newest history entries, one step further each time
- surprise: a form the last few history entries didn't use (a question, a list, a quote, a headline, one word)

The note's Examples show the register for each tone: how hard it lands, how long it runs, and how a motif ties to the subject. They are not a pool to pick from. Write a new line every time, built from the message and the tone in front of you. Borrow the energy, never the sentence: don't copy an example, and don't reuse one with only the ticket id swapped. If a line you've written sounds like one in the note, write a different one.

## With `--stay-fresh`

Scheduled runs pass this flag to draw variety from a history and the profile's motif list. Without it, skip this section.

**History.** The note named by the config's `voice history note` keeps recent lines in its `jsonl` code block, newest first, one JSON object per line: `{"date": "YYYY-MM-DD", "theme": "…", "line": "…"}`. Read it with the adapter's `read note`. If the note is missing, or the block is empty, there's no history yet. If the tracker can't be reached, write the line without history and skip saving.

**Motifs.** From the profile's Motifs section, take the motifs that suit the tone and drop any used in the last 8 entries; among the rest, prefer ones not in the history at all, and pick one at random. Go off the list only when nothing on it suits, or every motif that suits was used in the last 8; give it a short name. Build the line from that motif and the message's own subject, such as a task's title or whatever someone did.

Don't reuse a joke structure, pun or opening from any history entry. The message's own facts (ids, titles) can repeat, and leading with an id is fine, but the words around them must differ from every history entry. A catchphrase can come back with its motif, in a new structure.

After writing, add a new object at the top of the block with today's date (compute `TODAY` as the board rules' Dates section says), the motif exactly as listed (or its short name if off the list) as `theme`, and the exact output (with `--for`, the message without its `Subject:` line). Prune by the config's `voice history length`, which by default means: delete every entry that's 8 weeks old or more (its `date` is 56 or more days before `TODAY`), then keep only the newest 60. Change nothing outside the block, and save with the adapter's `write note`, which creates the note on the first write, with the block as its content.

## With `--for`

The caller passes the beat it's writing for. Each beat sets the register; the caller's tone says what's on the table. `--for` implies `--stay-fresh`.

- **morning**: start-of-day energy. Fresh or already planned tasks get light. Anything carried over gets what the policy says, below. The tone names each carried-over ticket id with the date it had before.
- **afternoon**: a tap on the shoulder. Playful, a friendly poke; never a dig, whatever the history says.
- **evening**: a friend asking how the day went. Open work gets what the policy says, by the same count as the morning; the tone names each open ticket id. Nothing open gets affirmation for the day's win: a win for the day, not the year.
- **week**: two halves in one message, a sentence or so each: last week, then the week ahead. The tone describes both. If the tone says there's no recap, write the week ahead only. Under a step-back policy, this is where a ticket the tone names as still open from last week gets its one mention.

**The history count** (morning and evening only). For each ticket id the tone names as carried over or still open, count the earlier days it appears in the history: the distinct dates, before today, of entries whose line contains the id. Compute it once, here; the policy says what it does.

**The policy.** The profile's When something keeps slipping section says what the count does. A count of zero (a ticket the history has never named) gets escalated: pointier, they've been here before. The policy may say after how many earlier days it starts; without a number, it starts at one. Until it starts, escalated. From then on:

- harder each day: harder with each earlier day, so that a ticket that has shown up for several days gets harsh. Harsh exists only under this policy.
- a direct question: the escalated register, no harder with the count, plus the question the profile gives, asked once in the line.
- break it smaller: the escalated register, plus an offer to split it or replan in chat, in the voice.
- step back: name the ticket without a jab, in a bare clause (the id, and the title if the line has room), and nothing more about it; the week beat gives it its one mention.
- a named consequence: the escalated register, and on the day the profile sets, the consequence said plainly, in the voice.

**Subject line.** With `--for`, the output's last line is `Subject: <a few words in the same voice>`, on its own line after the message. Callers use the words after `Subject:` as the notification title and drop the line from the body.

## Rules

- Include every id in the message, and every id the tone names. Titles are optional. Keep names, titles, dates and counts exactly as given when you use them. Facts given in the tone count as given. Add no other facts about the subject; the voice's world is the point.
- Short: about one or two sentences. With brevity in the profile, one.
- Follow the tone as described, as hard or as soft as it asks. Profanity is allowed only if the profile's `Profanity:` line says `yes`, in chat and in pushes alike. Some common tones, not the only ones:
  - **Light (the default when no tone is given):** in the voice's register, no softening.
  - **Escalated:** pointier; they've been here before.
  - **Harsh:** no mercy, in the voice's register. Only under the harder-each-day policy.
  - **Affirmation:** the day's win, in the voice's register; sincere when the tone asks.
- Don't repeat a joke structure or pun from earlier in the conversation.
- Plain text only: emojis only if the message had them, and no Markdown, HTML or quotes around the output.
- Output only the rewritten message (plus the `Subject:` line with `--for`).

Write the line they'd open. If they chose humor, make them laugh.

## Result

The rewritten message, plain text, with the `Subject:` line last when `--for` was given. With the voice off and `--for`, the message as given, plus that line.
