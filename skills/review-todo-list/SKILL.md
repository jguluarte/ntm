---
name: review-todo-list
description: >-
    Reviews the user's todo list with them in chat: closes obsolete or duplicate
    tasks, then estimates and splits unreviewed ones with their approval. Run by
    the user in chat, never by a job ("let's review my list", "review the
    kitchen project", "estimate the garage work").
---

# ntm:review-todo-list

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

What to review is a project, part of one, or a few tasks; see What to review.
Without it, the review proposes one.

## Before you start

Load `ntm:conventions` first: it holds your settings and the list's rules, and
names the guide that carries out each list operation below.

## Why review exists

Daily reminders only help when they point at something the user could pick up.
Reviewing gets tasks there, and it has to stay cheap enough that the user keeps
doing it: if it turns into a process, they'll stop. When in doubt, take the
lighter option:

- **A short session is a good session.** One project, or three items, is fine.
  Stop the moment the user wants to, and never push for more.
- **You bring proposals; the user reacts.** Never make them fill in fields, and
  never hit them with a list of questions.
- **Good enough reminders complete.** A task can be rough, or just a checklist,
  as long as the user says it's adequate.
- **The user drives the wording.** Your unvetted wording tends toward filler, so
  propose enough, keep it short, and never expand their descriptions unless they
  ask.

## Setup

1. Read the task review log (see The task review log).
2. Fetch every open task and list the projects, both as the conventions'
   Fetching says. Add each project's summary to the project fields, as the guide
   says.

A task is **unreviewed** when it's open, has no estimate, and isn't a parent
with open sub-tasks.

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

- **Close as obsolete:** canceled, or done if it looks like it already happened,
  with the guide's `set status`.
- **Duplicates:** identify all of the tasks that are ultimately duplicated, and
  quote anything that appears only on a specific one. You can propose what to
  do, but the user has the final say. On approval, do what they say and close
  the other(s) with the guide's `mark duplicate of`.
- **Move:** to the project it belongs in, or to none, with the guide's
  `update task`.

A plain "ok" approves the whole list; the user can strike items by number. If
nothing stands out, say so in one line and move on. Write what they approve as
soon as they approve it.

## 2. Order of operations

Read the unreviewed tasks in this review, plus any reviewed ones the user named,
with the guide's `read task`. For a blocked task with no blocked-by link, check
its comments (`read comments`) for what it waits on.

Propose an order to review them in, as a short list of ids and titles. Blockers
come before what they block. When a task waits on something outside this review:

- If the blocker has an obvious end state ("the desk is clear"), review the task
  anyway, assuming that end state, and mention that when you present it.
- Otherwise ask the user about it when you reach it.

If much of this review waits on another project, say so and offer to start there
instead. The user adjusts the order however they like, then you start.

## 3. Task by task

Each estimate comes from the estimator agent: ask its Estimate request for a
size, with any blocker end state you're assuming. When the agent isn't
available, follow its file as the conventions' "Chat, jobs and agents" says.

One item per message, in the agreed order:

1. The id linked to its URL, and the title.
2. Your proposed **estimate**, in the user's own terms (their Estimate pattern),
   with a few words on why, from the estimator. If the task already has one, say
   what it is.
3. If the estimator says it doesn't fit a sitting, one line on whether it looks
   like it splits. Some things can't, and that's fine. Pieces come up in the
   talk that follows (see Splits).
4. Usually no edits. Suggest one or two at most, only where the task would
   otherwise be hard to start: a title that doesn't say what it is, or a blocker
   that isn't linked. Show the exact new text, and write only what the user saw.
5. The description, exactly as written.

Make it one proposal: a plain "ok" approves all of it, and the user changes any
part in their own words. They'll very likely want to talk most tasks through, so
do that. "Skip" leaves the task unreviewed for another day.

If it splits, the estimate is for what's left of the original.

If the split came after your guess, re-propose for what's left, asking the
estimator again, and log that as `guess`.

Once a task is settled, in the same turn that presents the next one (or ends the
session): write it with the guide's `update task` (the estimate, plus any
approved title, description or blocked-by link), add its `## Estimates` entry to
the log, then ask the estimator about the next task.

## Splits

- The user usually brings their own ideas for how to split a task. When they do,
  use their pieces, and only point out a piece they seem to have left out. When
  they don't, propose the pieces yourself.
- Split pieces off as new tasks, and leave the original with its reduced scope.
  Show the exact text for the original's reduced scope and each new title, and
  write only that: the original with the guide's `update task`, the new tasks as
  the next bullet says. New tasks get the original's project and parent. When
  the order matters, the later task is blocked by the earlier one. Don't default
  to sub-tasks.
- Write new tasks with the guide's `create task`, the way the conventions'
  "Creating tasks when the user asks" section says. They join the end of the
  review order un-estimated, unless the user asks to do them next.

## The task review log

The `Task review log` database (see Databases in `ntm:conventions`): it's how
reviewing learns to work better with the user over time. Read it with the
guide's `read database`. When it's missing, `write database` creates it with the
two sections below. Save it with `write database` whenever you change it,
leaving the rest as it was.

**`## How you work`:** short bullets about the user, written to them (it's
theirs too), on whatever would help you do better with them next time: how they
like tasks written and split, how they like sessions to go, whether they're new
to estimating, and what they keep correcting. Learn from what they change, push
back on or say. When something would apply again, fold it in: rewrite and merge
bullets rather than appending, and keep the section to about 20 bullets.

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
were reviewed, closed and split, and what's still unreviewed in it.
