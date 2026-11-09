---
name: review-todo-list
description: >-
    Reviews the user's task list with them in chat: closes obsolete or duplicate
    tasks, then estimates unreviewed ones and breaks up big ones, with their
    approval. Run by the user in chat, never by a job ("let's review my list",
    "review the kitchen project", "estimate the garage work").
---

# ntm:review-todo-list

Reminders only help when they point at something the user could pick up. Review
gets tasks there. Keep it light so the user keeps doing it: a short session is a
good one, you bring proposals and they react, and their wording wins over yours.

## Setup

Load `ntm-user:backend` to read the user's conventions. If the task list can't
be read or written, say what went wrong.

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

The user names a project, part of one, or a few tasks. Without one, propose one
project with a one-line reason, such as how much of it has no estimate, and go
once they agree. Tasks with no project are reviewed a group of similar ones at a
time.

## Review

### 1. Clear out

Read the titles of every open task in the review, and of projects that overlap
it. Propose, as one numbered list, only the tasks to close as obsolete or done,
mark duplicates of the one the user keeps (quoting anything only one of them
says), or move to another project or to none. "Ok" approves the list; the user
can strike items by number. Write what they approve right away.

### 2. Set the order

Propose an order for the tasks with no estimate, plus any the user named:
blockers before what they block. Read each one's blocked-by links, and the
comments of a blocked task with none. When a blocker is outside the review and
has an obvious end state, assume it and say so; otherwise ask when you reach it.
If much of it waits on another project, offer to start there. The user adjusts
the order, then you start.

### 3. Estimate task by task

Start one estimator agent in the background at the first task, and send it every
ask in this review. It sees nothing of this chat. If it isn't available, read
`agents/estimator.md` from the newest installed `ntm` and follow it.

Ask its Estimate request for a size, with the task as it stands, any end state
you assumed, and anything the user said about size. Ask for the first task
alone, then keep it one or two tasks ahead; hold its answers until their task
comes up. If it returns an `ask:` line, put the question to the user and send
their answer back. If they ask what the ways to estimate are, ask its Explain
estimating request and pass its answer on.

Present one task per message: its id linked to its URL and its title, the
estimate, and the current one if it has one, with the estimator's few words on
why, a line on breaking it up if it doesn't fit a sitting, and the description
as written. Rarely, add up to two edits where it would be hard to start, shown
as the exact new text. "Ok" approves it all, "skip" leaves it for another day,
and anything else the user says changes it. When they correct an estimate, tell
the estimator and ask again for the tasks it answered ahead.

When a task is settled, write what they saw and send the estimator a Log request
with the settled estimate and what the user said or changed, in the same turn
you present the next task.

### 4. Break up big tasks

Use the user's pieces when they have them; otherwise propose some. Show the
exact new titles and the original's reduced scope, and write only that. New
tasks get the original's project and parent, and the later one is blocked by the
earlier when order matters. They go to the end of the review order. Ask the
estimator again for what's left of the original.

### 5. End

When the user stops or the review is done, send the estimator a Log request for
anything not yet logged. Sum up in a line or two: how many tasks were reviewed,
closed and broken up, and what's left without an estimate.
