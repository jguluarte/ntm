---
name: style-message
description: Rewrites a message the way the user's style profile (ntm-user:style) says it gets read, with the tone given as a freeform description, and returns it. Used by the messenger for every reminder, and in chat when the user asks for a message in their style.
---

# ntm:style-message

The style is `ntm-user:style`, written by `/ntm:configure-communication-style`: a `Profanity:` line, then Register (who is talking), What gets you to read (the attention mechanism), When something keeps slipping (the user's levels), Motifs, Off limits and Examples.

## Usage

```
/ntm:style-message [--stay-fresh] [--for morning|afternoon|evening|week] ["tone"] message
```

- `message` is the text or idea to rephrase. In chat, whatever the user asks to put in their style is the message, and anything they say about how is the tone. Naming the style alone isn't a tone. The skill returns plain text; callers add any links, lists or stats around it.
- `tone` is freeform: how to rephrase the message, and why. For example "Evening reminder; ABC-12 still open, carried over from yesterday" or "always late to brunch". Without one, use the first level.
- `--stay-fresh`: for scheduled runs, which keep lines fresh with a shared history.
- `--for <beat>`: for scheduled runs; one of the four beats below. Implies `--stay-fresh` and adds a `Title:` line. The caller opens the tone with its job name (`Morning reminder; …`).

## The profile

Load `ntm-user:style` by name and read it by heading. With `--stay-fresh`, read the message history too (next section).

If `ntm-user:style` won't load, the style isn't configured. With `--for`, return the message as given plus `Title: <job name>` as the last line, the job name being the first thing in the tone. Without `--for`, return the message as given and, in chat, also say in one line that the style isn't configured and that `/ntm:configure-communication-style` sets it. Nothing else below applies.

A section the profile lacks means: Register, the whole profile as given; What gets you to read, the examples show it; When something keeps slipping, one level and no climb; Motifs, none, with a repeat limit of eight; Off limits, the fixed set below; Examples, the body's own examples, if it has any.

**Register.** The profile's Register is who talks. A plain register has no character: the message speaks as itself, in the manner the section gives, and the mechanism below carries the line.

**What gets you to read** shapes every line. Follow what the profile says, as it combines them:

- brevity: one line, no ornament; the motif is a word, not a bit
- a curiosity hook: open with a question or a fact from the message itself, before the ask
- warmth and encouragement: on their side, never a dig; the ask comes after the regard
- humor: the joke is what gets it read
- a scoreboard: lead with the count the tone gives (what's done this week); never compute or invent one
- a running bit or serial: continue the bit from the newest history entries, one step further each time
- surprise: a form the last few history entries didn't use (a question, a list, a quote, a headline, one word)

**Levels.** The levels under When something keeps slipping, in the profile's order and with its names, are the only levels; this skill names none. The first level is the everyday one: fresh work, work already planned for today, and every line when the profile has one level. For a ticket the tone names as carried over or still open, the level comes from its history count (see With `--for`). The level is the last one whose "after N earlier days" the count has reached; count 0 is always the first level. A profile that lists levels without numbers gets 0, 1, 2… in order (the second level after 1 earlier day, the third after 2, and so on). Without `--for` there is no count: the tone says how hard, and the first level otherwise. Back to the first level once a ticket closes.

The profile's Examples show the register for each level, and for nothing open: how hard it lands, how long it runs, and how a motif ties to the subject. They are not a pool to pick from. Write a new line every time, built from the message and the tone in front of you. Borrow the energy, never the sentence: don't copy an example, and don't reuse one with only the ticket id swapped. If a line you've written sounds like one in the profile, write a different one.

## With `--stay-fresh`

Load `ntm:conventions`; it reads your settings and names the backend guide whose `read note` and `write note` are used below. Scheduled runs pass this flag to draw variety from a history and the profile's motif list. Without it, skip this section.

**History.** The message history note, titled as Notes under Board in your settings says, keeps recent lines in its `jsonl` code block, newest first, one JSON object per line: `{"date": "YYYY-MM-DD", "theme": "…", "line": "…"}`. Its first line is `Keep: <n> entries or <n> weeks`. Read it with the conventions' `read note`. If the note is missing, or the block is empty, there's no history yet. If the board can't be reached, write the line without history and skip saving.

**Motifs.** Pick a motif when the profile lists any; a line that uses none records `"theme": "none"`. From the profile's Motifs section, take the motifs that suit the tone and drop any used within the profile's repeat limit ("not in the last eight messages" when it gives none: the newest eight entries). Among the rest, prefer ones not in the history at all. Go off the list only when nothing on it suits, or every motif that suits was used within the limit. Give an off-list motif a short name. With no Motifs section, every line is off the list. Build the line from that motif and the message's own subject, such as a task's title or whatever someone did.

Don't reuse a joke structure, pun or opening from any history entry. The message's own facts (ids, titles) can repeat, and leading with an id is fine, but the words around them must differ from every history entry. A catchphrase can come back with its motif, in a new structure.

After writing, add a new object at the top of the block. Its `date` is today's date (compute `TODAY` as the conventions' Dates section says). Its `theme` is the motif's name exactly as listed under Motifs (its short name if off the list; `none` when the line uses none), and its `line` the exact output (with `--for`, the message without its `Title:` line). Prune to the note's `Keep:` line: delete every entry older than its weeks (`Keep: 60 entries or 8 weeks` means a `date` 56 or more days before `TODAY`), then keep only its newest entries (60). Change nothing outside the block, and save with the conventions' `write note`. When the note doesn't exist yet, write it as `Keep: 60 entries or 8 weeks`, a blank line, then the block; `write note` creates it.

## With `--for`

The caller passes the beat it's writing for. Each beat sets the register; the caller's tone says what's on the table. `--for` implies `--stay-fresh`.

- **morning**: start-of-day energy. Fresh or already planned tasks get the first level. Anything carried over gets what When something keeps slipping says, by the count below. The tone names each carried-over ticket id with the date it had before and how many days it has carried (`was <date>, carried <n> days`); the message may state that count, and adds nothing else to it.
- **afternoon**: a tap on the shoulder. Playful, a friendly poke; never a dig, whatever the history says. The first level, always.
- **evening**: a friend asking how the day went. Open work gets what When something keeps slipping says, by the same count as the morning; the tone names each open ticket id. Nothing open gets the register of the profile's "nothing open" example: a win for the day, not the year.
- **week**: two halves in one message, a sentence or so each: last week, then the week ahead. The tone describes both. If the tone says there's nothing to look back on, write the week ahead only. The week has no history count: every ticket gets the first level.

**The history count** (morning and evening only). For each ticket id the tone names as carried over or still open, count the earlier days it appears in the history: the distinct dates, before today, of entries whose `line` contains the id. Compute it once, here; Levels says what it does.

**Title line.** With `--for`, the output's last line is `Title: <a few words in the same style>`, on its own line after the message. Callers use the words after `Title:` as the notification title and drop the line from the body.

## Rules

- Include every id in the message, and every id the tone names. Titles are optional. Keep names, titles, dates and counts exactly as given when you use them. Facts given in the tone count as given. Add no other facts about the subject; the style's world is the point.
- Address the user by Name from About you in your settings when the register addresses them by name; otherwise "you".
- Honour Off limits: ticket ids, titles, planned dates, counts and names are carried as given, never rewritten or joked about, and so is anything the profile adds there.
- Short: about one or two sentences. With brevity in the profile, one.
- Follow the tone as described, as hard or as soft as it asks. Profanity is allowed only if the profile's `Profanity:` line says `yes`, in chat and in pushes alike. The levels are the profile's; two tones that aren't levels:
  - **Nothing open:** the day's win, in the register of the profile's "nothing open" example; sincere when the tone asks.
  - **Afternoon:** a friendly poke, never a dig.
- Don't repeat a joke structure or pun from earlier in the conversation.
- Plain text only: emojis only if the message had them, and no Markdown, HTML or quotes around the output.
- Output only the rewritten message (plus the `Title:` line with `--for`).

Write the line they'd open. If they chose humor, make them laugh.

## Result

The rewritten message, plain text, with the `Title:` line last when `--for` was given. With no style configured and `--for`, the message as given, plus that line.
