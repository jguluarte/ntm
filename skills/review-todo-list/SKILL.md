---
name: review-todo-list
description: Reviews the user's todo list with them in chat: closes obsolete or duplicate tickets, then sizes and splits unreviewed ones with their approval. Run by the user in chat, never by a job ("let's review my list", "review the kitchen project", "size the garage work").
---

# ntm:review-todo-list

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

What to review is a project, part of one, or a few tickets; see The slice.
Without it, propose one.

## Why this exists

Daily reminders only help when they point at something the user could pick up.
Reviewing gets tickets there, and it has to stay cheap enough that the user
keeps doing it: if it turns into a process, they'll stop. When in doubt, take
the lighter option:

- **A short session is a good session.** One project, or three items, is fine.
  Stop the moment the user wants to, and never push for more.
- **You bring proposals; the user reacts.** Never make them fill in fields, and
  never hit them with a list of questions.
- **Good enough reminders complete.** A ticket can be rough, or just a
  checklist, as long as the user says it's adequate.
- **The user drives the wording.** Your unvetted wording tends toward filler, so
  propose enough, keep it short, and never expand their descriptions unless they
  ask.

## Setup

1. Load `ntm:conventions`, and compute `TODAY` as its Dates section says.
2. Read the grooming log (see below).
3. Fetch every open ticket and list the projects, both as the conventions'
   Fetching says. Add each project's summary to the project fields, as the guide
   says.

A ticket is **unreviewed** when it's open, has no estimate, and isn't a parent
with open sub-tickets. On a backend without an estimate field (its guide or Todo
list in your settings says), "no estimate" means no entry in the log's Estimates
block.

## The slice

The user names what to review however they like: a project, part of one, a few
tickets, or something already reviewed that they want to look at again. Take
what they say.

If they don't name one, use what Setup fetched to propose one project, with a
one-line reason such as how much is left unreviewed. Go once they agree.

Tickets with no project get grouped by likeness and reviewed a group at a time.
A group can also be a reason to propose a project to file it under, even a new
one.

## 1. Overview

Clear out what doesn't belong before looking at details. Look over every open
ticket in the slice by title, reading a description only where the title isn't
enough. Also skim the titles in projects whose names or topics overlap with the
slice, for tickets logged twice or filed in the wrong place.

Propose, as one numbered list, one short line each, only for tickets you'd
change:

- **Close as obsolete:** canceled, or done if it looks like it already happened,
  with the guide's `set status`.
- **Duplicates:** identify all of the tickets that are ultimately duplicated,
  and quote anything that appears only on a specific one. You can propose what
  to do, but the user has the final say. On approval, do what they say and close
  the other(s) with the guide's `mark duplicate of`.
- **Move:** to the project it belongs in, or to none, with the guide's
  `update ticket`.

A plain "ok" approves the whole list; the user can strike items by number. If
nothing stands out, say so in one line and move on. Write what they approve as
soon as they approve it.

## 2. Order of operations

Read the slice's unreviewed tickets, plus any reviewed ones the user named, and
their parent chains, with the guide's `read ticket`. For a blocked ticket with
no blocked-by link, check its comments (`read comments`) for what it waits on.

Propose an order to review them in, as a short list of ids and titles. Blockers
come before what they block. When a ticket waits on something outside the slice:

- If the blocker has an obvious end state ("the desk is clear"), review the
  ticket anyway, assuming that end state, and mention that when you present it.
- Otherwise ask the user about it when you reach it.

If much of the slice waits on another project, say so and offer to start there
instead. The user adjusts the order however they like, then you start.

## 3. Ticket by ticket

One item per message, in the agreed order:

1. The id linked to its URL, and the title.
2. Your proposed **estimate**, on the Sizing scale in Planning in your settings,
   with a few words on why, guided by how past guesses in the grooming log
   compared with what the user settled on. If it already has one (on a backend
   without an estimate field, its latest log entry's `final`), say what it is.
3. If its estimate makes it bigger than a typical sitting, one line on whether
   it looks like it splits. Some things can't, and that's fine. Pieces come up
   in the talk that follows (see Splits).
4. Usually no edits. Suggest one or two at most, only where the ticket would
   otherwise be hard to start: a title that doesn't say what it is, or a blocker
   that isn't linked. Show the exact new text, and write only what the user saw.
5. The description, exactly as written.

Make it one proposal: a plain "ok" approves all of it, and the user changes any
part in their own words. They'll very likely want to talk most tickets through,
so do that. If it splits, the estimate is for what's left of the original; if
the split came after your guess, re-propose for what's left and log that as
`guess`. "Skip" leaves the ticket unreviewed for another day.

Once a ticket is settled, write it with the guide's `update ticket` (estimate,
and any approved title, description or blocked-by link) and update the log. Do
both in the same turn that presents the next ticket (or ends the session), so
writes never make the user wait.

### Splits

- The user usually brings their own split ideas. Propose pieces only when they
  don't; otherwise just check whether they missed something obvious.
- Split pieces off as new tickets, and leave the original with its reduced
  scope. Show the exact text for the original's reduced scope and each new
  title, and write only that: the original with the guide's `update ticket`, the
  new tickets as the next bullet says. New tickets get the original's project
  and parent. When the order matters, the later ticket is blocked by the earlier
  one. Don't default to sub-tickets.
- Write new tickets with the guide's `create ticket`, the way the conventions'
  "Creating tickets when the user asks" section says. They join the end of the
  review order un-estimated, unless the user asks to do them next.

## The grooming log

The grooming log note, titled as Notes under Todo list in your settings says.
It's yours: it's how you learn to work better with the user over time. Read it
with the guide's `read note`. When it's missing, `write note` creates it with
the two sections below.

### `## How you work`

Short bullets about the user, written to them (it's their note too), on whatever
would help you do better with them next time: how they like tickets written and
split, how they like sessions to go, and what they keep correcting. Learn from
what they change, push back on or say. When something would apply again, fold it
in: rewrite and merge bullets rather than appending, and keep the section to
about 20 bullets.

### `## Estimates`

A `jsonl` code block, newest first, one object per approved estimate:

```jsonl
{"date": "YYYY-MM-DD", "id": "ABC-12", "guess": 2, "final": 3, "why": "wiring took longer than it looked"}
```

`guess` is what you proposed and `final` what the user approved, each written
the way the Sizing scale writes it (`3`, `"2 h"`, `"weekend"`). Keep `why` to a
few words: what made them change it, or what made the guess right. Keep the
newest 150 entries. On a backend without an estimate field the log is the only
record of what's reviewed, so keep every entry.

Save it with `write note` whenever you change it, leaving the rest as it was.

## Ending

When the user stops, or the slice is done, fold anything you learned into
`## How you work` and save the log, then sum up in a line or two: how many items
were reviewed, closed and split, and what's still unreviewed in the slice.
