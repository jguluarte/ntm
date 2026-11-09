---
name: review-todo-list
description: >-
    Reviews the user's todo list with them in chat: closes obsolete or duplicate
    tasks, then estimates unreviewed ones and breaks up big ones, with their
    approval. Run by the user in chat, never by a job ("let's review my list",
    "review the kitchen project", "estimate the garage work").
---

# ntm:review-todo-list

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

What to review is a project, part of one, or a few tasks; see What to review.
Without it, the review proposes one.

## Before you start

Load `ntm-user:backend` to read the user's conventions. If the todo list can't
be read or written, say what went wrong.

## Why review exists

Daily reminders only help when they point at something the user could pick up.
Reviewing gets tasks there, and it has to stay cheap enough that the user keeps
doing it: if it turns into a process, they'll stop. When in doubt, take the
lighter option:

- **A short session is a good session.** One project, or three items, is fine.
  Stop the moment the user wants to, and never push for more.
- **You bring proposals; the user reacts.** Never make them fill in fields, and
  never hit them with a list of questions.
- **Good enough is complete.** A task can be rough, or just a checklist, as long
  as the user says it's adequate.
- **The user drives the wording.** Your unvetted wording tends toward filler, so
  propose enough, keep it short, and never expand their descriptions unless they
  ask.

## Setup

1. Read the task review log (see The task review log), and the Estimate pattern
   from the Planning section of the Settings document.
2. Find every open task, and each project with its summary.

A task is **unreviewed** when it's open and has no estimate.

When Estimate pattern is blank, ask the estimate question before going on.

## The estimate question

Estimate pattern stays blank until the user's first review. Ask one high-level
question: how would they like to estimate their tasks? It stands on its own, and
most people just answer it. Only when they ask for more on the ways to estimate,
ask the estimator agent's Explain estimating request and pass its ways on; when
the agent isn't available, read `agents/estimator.md` from the newest installed
`ntm` and follow it.

When `ntm-user:backend` says how to fit their estimates to the list's own scale,
work that out with them as it says. Then write their answer, in their words with
any mapping you agreed, as the Estimate pattern line under Planning in the
Settings document, as `ntm-user:backend` says. Use it for the rest of this
review.

## What to review

The user names what to review however they like: a project, part of one, a few
tasks, or something already reviewed that they want to look at again. Take what
they say.

If they don't name one, use what Setup fetched to propose one project, with a
one-line reason such as how much is left unreviewed. Go once they agree.

Tasks with no project get grouped by likeness and reviewed a group at a time. A
group can also be a reason to propose a project to file it under, even a new
one.

## 1. Overview

Clear out what doesn't belong before looking at details. Look over every open
task in this review by title, reading a description only where the title isn't
enough. Also skim the titles in projects whose names or topics overlap with it,
for tasks logged twice or filed in the wrong place.

Propose, as one numbered list, one short line each, only for tasks you'd change:

- **Close as obsolete:** canceled, or done if it looks like it already happened.
- **Duplicates:** identify all of the tasks that are ultimately duplicated, and
  quote anything that appears only on a specific one. You can propose what to
  do, but the user has the final say. On approval, do what they say and mark the
  other(s) as duplicates of the one kept.
- **Move:** to the project it belongs in, or to none.

A plain "ok" approves the whole list; the user can strike items by number. If
nothing stands out, say so in one line and move on. Write what they approve as
soon as they approve it.

## 2. Order of operations

Read each unreviewed task in this review, plus any reviewed ones the user named,
with its blocked-by links. For a blocked task with no blocked-by link, check its
comments for what it waits on.

Propose an order to review them in, as a short list of ids and titles. Blockers
come before what they block. When a task waits on something outside this review:

- If the blocker has an obvious end state ("the desk is clear"), review the task
  anyway, assuming that end state, and mention that when you present it.
- Otherwise ask the user about it when you reach it.

If much of this review waits on another project, say so and offer to start there
instead. The user adjusts the order however they like, then you start.

## 3. Task by task

One estimator agent proposes every estimate in this review. Start it once, at
the first task, and hand it what it needs then: the Estimate pattern, and the
log's `## How you work` and recent `## Estimates` entries, which Setup already
read. It sees nothing of this chat, only what you hand it, so this hand-off is
what lets it load nothing itself. Start it in the background, and send every
later ask to that same agent; don't start a new one. When the agent isn't
available, read `agents/estimator.md` from the newest installed `ntm` and follow
it.

Ask its Estimate request for a size for the first task alone, so the first
proposal comes fast. Wait for that answer only; never wait on an ask ahead
before presenting the current task. Then keep it one or two tasks ahead of the
user in the agreed order, so the next estimate is ready when they finish, and no
further, so it's free when the user wants to talk the current task over. With
each task, send it as it stands now, any blocker end state you're assuming, and
anything the user said this session that bears on size.

Its answers wait until their task comes up. Never interrupt the user with them,
or mention them early.

One item per message, in the agreed order:

1. The id linked to its URL, and the title.
2. Your proposed **estimate**, in the user's own terms (their Estimate pattern),
   with a few words on why, from the estimator. If the task already has one, say
   what it is.
3. If the estimator says it doesn't fit a sitting, one line on whether it could
   be broken up. Some things can't, and that's fine. Pieces come up in the talk
   that follows (see Breaking up tasks).
4. Usually no edits. Suggest one or two at most, only where the task would
   otherwise be hard to start: a title that doesn't say what it is, or a blocker
   that isn't linked. Show the exact new text, and write only what the user saw.
5. The description, exactly as written.

Make it one proposal: a plain "ok" approves all of it, and the user changes any
part in their own words. They'll very likely want to talk most tasks through, so
do that. "Skip" leaves the task unreviewed for another day.

If it's broken up, the estimate is for what's left of the original.

After a task is broken up, ask the estimator again for what's left of the
original. After the user corrects an estimate, pass the correction along, ask
again for any task it already answered ahead, and drop those early answers. When
the task was broken up after your guess, log the new proposal as `guess`.

Once a task is settled, in the same turn that presents the next one (or ends the
session): write the settled estimate (and any approved title, description or
blocked-by link), add its `## Estimates` entry to the log, and pass the settled
estimate to the estimator with its next ask, so writes never make the user wait.

## Breaking up tasks

Sometimes a single task is too big to do all at the same time. Or sometimes the
user just wants to tease things apart so they can do it in smaller pieces.

- The user may bring their own ideas for how to split a task. When they do, use
  their pieces, and only point out a piece they seem to have left out. When they
  don't, propose the pieces yourself.
- Split pieces off as new tasks, and leave the original with its reduced scope.
  Show the exact text for the original's reduced scope and each new title, and
  write only that: the original, then the new tasks as the next bullet says. New
  tasks get the original's project and parent. When the order matters, the later
  task is blocked by the earlier one. Don't default to sub-tasks.
- Create each new task as `ntm-user:backend`'s rules for creating tasks say.
  They join the end of the review order un-estimated, unless the user asks to do
  them next.

## The task review log

The `Task review log` database: it's how reviewing learns to work better with
the user over time. Read and write it where `ntm-user:backend` keeps it. When
it's missing, the first write creates it with the two sections below. Save it
whenever you change it, leaving the rest as it was.

**`## How you work`:** how the user estimates and breaks up tasks, learned so
that review can come to propose most of their list the way they would. Short
bullets, written to them (it's theirs too), grouped by topic: how they estimate,
how they like tasks written and broken up, how they like sessions to go, whether
they're new to estimating, and what they keep correcting. Learn from what they
change, push back on or say. Keep it tidy, not short: fold related bullets
together and rewrite rather than append, and let it run as long as it needs.

**`## Estimates`:** a `jsonl` code block, newest first, one object per approved
estimate:

<!-- prettier-ignore -->
```jsonl
{"date":"YYYY-MM-DD","id":"ABC-12","guess":2,"final":3,"why":"wiring was slow"}
```

`date` is today. `guess` is what you proposed and `final` what the user
approved, each written the way the Estimate pattern writes it (`3`, `"2 h"`,
`"weekend"`). Keep `why` to a few words: what made them change it, or what made
the guess right. Keep the newest 150 entries.

## Ending

When the user stops, or this review is done, fold anything you learned into
`## How you work` and save the log, then sum up in a line or two: how many items
were reviewed, closed and broken up, and what's still unreviewed in it.
