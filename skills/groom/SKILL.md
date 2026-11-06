---
name: groom
description: Grooms the user's nudge board with them in chat: closes obsolete or duplicate tickets, then sizes and splits ungroomed ones with their approval. Run only when the user asks to groom ("let's groom", "groom the kitchen project"), never by a job.
---

# nudge:groom

## Why this exists

Daily reminders only help when they point at something the user could pick up. Grooming gets tickets there, and it has to stay cheap enough that the user keeps doing it: if it turns into a process, they'll stop. When in doubt, take the lighter option:

- **A short session is a good session.** One project, or three tickets, is fine. Stop the moment the user wants to, and never push for more.
- **You bring proposals; the user reacts.** Never make them fill in fields, and never hit them with a list of questions.
- **Good enough beats complete.** A ticket can be rough, or just a checklist, as long as the user says it's adequate.
- **The user drives the wording.** Your unvetted wording tends toward filler, so propose enough, keep it short, and never expand their descriptions unless they ask.

## Setup

1. Load `nudge:board`, and compute `TODAY` as its Dates section says.
2. Read the Grooming log (see below).
3. Fetch every open ticket and list the projects, both as the board rules' Fetching says, adding each project's summary to the project fields, as the adapter says.

A ticket is **ungroomed** when it's open, has no estimate (or, on a tracker without estimates, no entry in the log's Estimates block, as the adapter says), and isn't a container (a parent with open sub-tickets).

## The slice

The user names what to groom however they like: a project, part of one, a few tickets, or something already groomed that they want to look at again. Take what they say.

If they don't name one, use what Setup fetched to propose one project, with a one-line reason such as how much is left ungroomed. Go once they agree.

Tickets with no project get grouped by likeness and groomed a group at a time. A group can also be a reason to propose a project to file it under, even a new one.

## 1. Overview

Clear out what doesn't belong before looking at details. Look over every open ticket in the slice by title, reading a description only where the title isn't enough. Also skim the titles in projects whose names or topics overlap with the slice, for tickets logged twice or filed in the wrong place.

Propose, as one numbered list, one short line each, only for tickets you'd change:

- **Close as obsolete:** canceled, or done if it looks like it already happened, with the adapter's `set status`.
- **Duplicates:** identify all of the tickets that are ultimately duplicated, and quote anything that appears only on a specific one. You can propose what to do, but the user has the final say. On approval, do what they say and close the other(s) with the adapter's `mark duplicate of`.
- **Move:** to the project it belongs in, or to none, with the adapter's `update ticket`.

A plain "ok" approves the whole list; the user can strike items by number. If nothing stands out, say so in one line and move on. Write what they approve as soon as they approve it.

## 2. Order of operations

Read the slice's ungroomed tickets, plus any groomed ones the user named, and their parent chains, with the adapter's `read ticket`. For a blocked ticket with no blocked-by link, check its comments (`read comments`) for what it waits on.

Propose an order to groom them in, as a short list of IDs and titles. Blockers come before what they block. When a ticket waits on something outside the slice:

- If the blocker has an obvious end state ("the desk is clear"), groom the ticket anyway, assuming that end state, and mention that when you present it.
- Otherwise ask the user about it when you reach it.

If much of the slice waits on another project, say so and offer to start there instead. The user adjusts the order however they like, then you start.

## 3. Ticket by ticket

One ticket per message, in the agreed order:

1. The ID linked to its URL, and the title.
2. Your proposed **estimate**, with a few words on why, guided by how past guesses in the Grooming log compared with what the user settled on. If it already has one (on a tracker without estimates, its latest log entry's `final`), say what it is.
3. If it's a 3 or more, one line on whether it looks like it splits. Some things can't, and that's fine. Pieces come up in the talk that follows (see Splits).
4. Usually no edits. Suggest one or two at most, only where the ticket would otherwise be hard to start: a title that doesn't say what it is, or a blocker that isn't linked. Show the exact new text, and write only what the user saw.
5. The description, exactly as written.

Make it one proposal: a plain "ok" approves all of it, and the user changes any part in their own words. They'll very likely want to talk most tickets through, so do that. If it splits, the estimate is for what's left of the original; if the split came after your guess, re-propose for what's left and log that as `guess`. "Skip" leaves the ticket ungroomed for another day.

Once a ticket is settled, write it with the adapter's `update ticket` (estimate, and any approved title, description or blocked-by link) and update the log in the same turn that presents the next ticket (or ends the session), so writes never make the user wait.

### Splits

- The user usually brings their own split ideas. Propose pieces only when they don't; otherwise just check whether they missed something obvious.
- Split pieces off as new tickets, and leave the original with its reduced scope. Show the exact text for the original's reduced scope and each new title, and write only that, the original's with the adapter's `update ticket`. New tickets get the original's project and parent. When the order matters, the later ticket is blocked by the earlier one. Don't default to sub-tickets.
- Write new tickets with the adapter's `create ticket`, the way the board rules' "Creating tickets when the user asks" section says. They join the end of the grooming order un-estimated, unless the user asks to do them next.

## The Grooming log

The note named by the config's `grooming log note`. It's yours: it's how you learn to work better with the user over time. Read it with the adapter's `read note`. When it's missing, `write note` creates it with the two sections below, with `<your name>` in the first heading taken from the config's `your name`.

### `## How <your name> works`

Short bullets about the user, in the third person (they can read this note too), on whatever would help you do better with them next time: how they like tickets written and split, how they like sessions to go, and what they keep correcting. Learn from what they change, push back on or say. When something would apply again, fold it in: rewrite and merge bullets rather than appending, and keep the section to about 20 bullets.

### `## Estimates`

A `jsonl` code block, newest first, one object per approved estimate:

```jsonl
{"date": "YYYY-MM-DD", "id": "ABC-12", "guess": 2, "final": 3, "why": "wiring took longer than it looked"}
```

`guess` is what you proposed and `final` what the user approved. Keep `why` to a few words: what made them change it, or what made the guess right. Keep the newest 150 entries.

Save it with `write note` whenever you change it, leaving the rest as it was.

## Ending

When the user stops, or the slice is done, fold anything you learned into `## How <your name> works` and save the log, then sum up in a line or two: how many tickets were groomed, closed and split, and what's still ungroomed in the slice.
