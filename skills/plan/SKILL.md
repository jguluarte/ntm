---
name: plan
description: >-
    Plans the user's task list by setting planned dates, one task a weekday by
    default, and returns the plan. --auto day carries earlier days' unfinished
    work to today and gives an empty today a task; --auto with a range such as
    week gives each empty weekday in it a task; anything else plans with the
    user in chat. Run by the morning reminder and weekly setup jobs, or by the
    user ("plan my week", "plan my todo list", "plan Thursday around the
    garage").
---

# ntm:plan

Plan gives the user's days their tasks by setting planned dates. It sets and
moves dates, and clears one only when the user agrees to it in chat. A stale
date it moves or clears goes into the task's `Planned date history` first, as
ntm's core rules say.

## Usage

```
/ntm:plan --auto day
/ntm:plan --auto <range>
/ntm:plan [<what to plan, in words>]
```

`--auto` plans unattended, in a job. Anything else plans with the user in chat.

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

Read the task management rules,
`${CLAUDE_PLUGIN_ROOT}/references/rules/task-management.md`.

Read the Paused dates part of `%Paused-dates`. Each item is a paused day, or a
range with both ends included, then an optional reason.

## Days to plan

The Planning part of `%Settings` says which days to plan, and how many tasks of
what size each one gets. A day is empty when no open task is planned for it,
whatever its labels or status.

## Picking tasks

Pick from the plannable tasks with no planned date, or a stale one. Prefer,
roughly in this order:

- the next pieces of a project or chain already planned, so the week reads as
  one theme
- small, concrete tasks, of the size the Planning part says
- work that unblocks other open work
- a priority the user set

Plan each task once. When nothing is left to pick for a day, leave it empty.

## Estimates

Judge a task's size by the `Estimate:` line in its description. For likely picks
without one, ask the estimator agent once, with an Estimate request for all of
them.

## `--auto day`

### 1. Carry over

Move every open task planned before today to today, even when today is paused,
adding each old date to the task's `Planned date history` first.

### 2. Fill today

If today is still empty and isn't paused, pick its tasks.

## `--auto <range>`

The range is in words, such as `week` or `month`, read as a person would. `week`
is the rest of this week, or the coming one on a weekend.

Each day to plan in the range gets its tasks when it's empty and not paused.

## In chat

The span is what the user names, such as "today" or "next week". With none
named, it's this week, or the next one when this one is nearly over.

The user has the final say; the rest of this skill is where you start. A day
they name gets planned even when the Planning part leaves it out, such as a
weekend: say in a line that it's outside their usual plan. A paused day gets
planned when they ask. When something looks like a problem, such as a blocked
chain that can't finish in the span, say so, then do what they decide.

### 1. Show the span

Each day's tasks, and which days are paused.

### 2. Find out what they want

Go on what they said. Words like "the garage" match by project, parent, label or
title. If what they said isn't enough to plan from, ask what they want the span
to be about: a project, a goal, a mood, or just "reset it".

### 3. Propose a plan

Lean toward what they asked for, give each pick its estimate and a one-line
reason, and revise until they approve. Any open task can move, even one dated
later in the span; say which day it leaves empty. A task bumped off a day has
its date cleared, unless they want it on a later day. A day that has tasks takes
one more when they ask for more on it. Days they want empty stay empty.

### 4. Save

List every date the plan sets and every date it clears, dates they set
themselves included, and ask to save. Once they agree, write them.

## Result

### `--auto`

Today or the range as planned, in day order: a line for each task planned in it,
including those planned before this run, and for each day to plan that's paused
or still empty.

```
<date>: <id> <title> <url>
<date>: <id> <title> <url> (carried over from <date>)
<date>: <id> <title> <url> (picked, <estimate>)
<date>: paused
<date>: nothing to plan
```

### In chat

The saved plan, day by day: each day's tasks, the estimate and reason for each
pick, and which days are paused or left empty.
