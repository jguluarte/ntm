---
name: review-todo-list
description: >-
    Reviews the user's task list with them in chat: closes obsolete or duplicate
    tasks, then estimates unreviewed ones and breaks up big ones, with their
    approval. Run by the user in chat, never by a job ("let's review my list",
    "review my todo list", "review the kitchen project", "estimate the garage
    work").
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

Start by telling the user they can stop whenever they like, even mid-task: they
just say so, and you save what's settled.

### 1. Health check. Merge duplicates, close obsolete tasks

Read the titles of every open task in the review, and of projects that overlap
it. Propose, as one numbered list, only the tasks to close as obsolete or done,
to merge into a duplicate the user keeps (quoting anything only one of them
says), or to move to another project or to none. A simple affirmation likely
approves the list; the user can strike items by number. Save these changes
before proceeding.

### 2. Decide what to review

Propose an order for the tasks with no estimate, plus any the user named:
blockers before what they block. Read each one's blocked-by links. For a task in
a blocked status with no blocked-by link, read its comments to find what it
waits on. When a blocker is outside the review and has an obvious end state,
assume it and say so; otherwise ask when you reach it. If many of these tasks
wait on another project, offer to review that one first. The user adjusts the
order, then you start.

### 3. Estimate one task at a time

Start an estimator agent in the background at the first task, and send it every
ask in this review. It sees nothing of this chat. If it isn't available, read
`agents/estimator.md` from the newest installed `ntm` and follow it. **Use one
estimator for this entire run, so they persist context**. When the estimator
finishes the first one, give it the next two so they're ready for the user
quickly. Keep it alive in case the user has more questions.

Send it an Estimate request for a size, with the task as it stands, any end
state you assumed, and anything the user said about size. Hold its answers until
their task comes up. If the user asks what the ways to estimate are, send it an
Explain estimating request and pass its answer on.

Present one task per message:

- its id, linked to its URL, and its title
- the proposed estimate, with the estimator's few words on why
- the estimate already on the task, if any
- a line on breaking it up, when the estimator says it doesn't fit a sitting
- the description as written

Rarely, when the task as written would be hard to start, propose up to two edits
to its title or description, shown as the exact new text. A simple affirmation
likely approves it all, asking to skip leaves it for another day, and anything
else the user says changes it. When they correct an estimate, tell the estimator
and ask again for the tasks it answered ahead.

When a task is settled, save any approved edits and its estimate, as the last
line of its description (`Estimate: 2 hours`), replacing any earlier one. Send
the estimator a Log request with the settled estimate and what the user said or
changed, in the same turn you present the next task.

#### Breaking up big tasks

When the estimator says a task doesn't fit a sitting, or the user says it's too
big, help the user break it up: suggest a few ways to split it. Not every task
splits, but try. Use the user's pieces when they have them. Show the exact new
titles and the original's reduced scope, and write only that. New tasks get the
original's project and parent, and the later one is blocked by the earlier when
order matters. They go to the end of the review order. Ask the estimator again
for what's left of the original.

### 4. End

When the user stops, however abruptly, or the review is done, send the estimator
a Log request for anything not yet logged. Sum up in a line or two: how many
tasks were reviewed, closed and broken up, and what's left without an estimate.
