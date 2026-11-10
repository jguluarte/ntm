---
name: plan
description: >-
    Plans the user's task list by setting planned dates, one task a weekday by
    default, and returns the plan. --auto day makes today ready; --auto with a
    range in words (week, week mon-fri, all weekdays this month) plans the days
    it covers; anything else plans with the user in chat. Run by jobs, or by the
    user ("plan my week", "plan my todo list", "plan Thursday around the
    garage").
---

# ntm:plan

Plans the user's task list: picks open tasks for days and sets their planned
dates. The user vets their own task list, so every task is real work they want
kept moving, and the pauses are theirs. Set, move and clear planned dates as
this skill says, and change nothing else on a task.

## Usage

```
/ntm:plan --auto day
/ntm:plan --auto <range>
/ntm:plan [<what to plan, in words>]
```

`--auto day` makes today ready: stale work moves to today, and today gets a task
when it has none. `--auto <range>` plans the days a range covers, such as
`week`, `week mon-fri` or `all weekdays this month`. Both run unattended.
Anything else plans with the user in chat, such as "plan the week around the
garage" or "give Thursday something small".

## Setup

Load `ntm-user:backend` to read the user's conventions, and `ntm:pause`. Read
the Planning section of the `Settings` database: the labels planning excludes,
and anything else the user said about how they want their task list planned.
Then fetch every open task.

## Defaults

Plan this way unless the job's prompt, the user's Planning settings or the user
in chat say otherwise.

| Default        | Value                                                |
| -------------- | ---------------------------------------------------- |
| Days           | weekdays                                             |
| Tasks a day    | one                                                  |
| Size           | about an hour or less, where possible                |
| Weekly message | what got done, what's still open, and the week ahead |

A bigger task can still be planned; its size is the signal to break it up.

## Choosing tasks

A candidate is an open task in a plannable status, with no planned date or a
stale one, that isn't excluded, as Excluded tasks in the conventions says.
Shortlist the likeliest picks from what the fetch shows, then read only those in
full, for their descriptions and blocked-by links. A task blocked by another
goes on a later day than its blocker, as Blocks and blocked by in the
conventions says.

Give each day as many picks as Defaults says, weighing, roughly in this order:

1. What's already planned: the next piece of the same chain or project, so the
   week reads as one theme.
2. Small and concrete: about the size in Defaults, by its estimate.
3. Unblocking: work that frees up other open work.
4. Priority, when the user set one. A missing one means nothing.

Each task is planned at most once. A day with no candidate left stays empty.

A day that holds any open task, whatever its labels or status, is already
planned. Its work is a theme for the rest of the week.

## Estimates

A task's estimate is the `Estimate:` line at the end of its description. Send
the estimator agent one Estimate request with the shortlisted tasks that have
none. The estimates judge how well a task fits a day.

## Paused days

Nothing gets planned onto a paused day. Check a span with
`/ntm:pause --check <first day> --until <last day>`: a day whose line ends
`true` is paused. A date the user set on a paused day stands.

## --auto day

### 1. Carry over

Every open task planned before today is stale. Move each one in a plannable
status to today, whatever its labels and even when another task blocks it: the
user dated it, and carrying a date isn't picking. A stale task in the blocked
status keeps its date. Carry over on a paused day too.

### 2. Plan today

When nothing is planned for today, check whether today is paused. If it is,
today stays empty. Otherwise pick today's tasks, as Choosing tasks says, and
plan them for today.

## --auto <range>

### 1. Find the days

Read the range the way a person would, counting from today. The days it names
(`mon-fri`, `weekends`, `all weekdays`) are the planning days; otherwise they're
the days in Defaults. `week` is the rest of this week, or the coming week on a
weekend.

### 2. Plan the open days

Check the planning days for pauses, then give each one that isn't paused and
holds no task its picks, in day order.

## With the user in chat

The span is what the user names, or a week when they name none (next week when a
day or less of this one is left). A day they name gets planned even when it's
outside their usual days, such as a weekend; say so in one line. Words like "the
garage" match a project, parent, label or title.

Defaults and the rules here are where you start, not the user's limits: they
have the final say. When something looks like a problem, such as a blocked chain
that can't finish in the span, say so, then do what they decide.

### 1. Show the span

Each day's tasks, and which days are paused.

### 2. Find what it's about

Go on what they said. When that isn't enough to plan from, ask what they want
the span to be about: a project, a goal, a mood, or a fresh start.

### 3. Propose a plan

Lean toward what they asked for, give each pick a one-line reason, and revise
until they approve. Any open task can move, even one already dated later in the
span; say which day it leaves empty. A task the plan bumps off a day has its
date cleared, unless they move it to a later day. Days they want empty stay
empty, a paused day gets planned when they want it, and a day that's already
planned gets more when they ask.

Before they approve, list every date the plan sets and every date it clears,
including dates they set themselves.

### 4. Save it

Write the dates, and show the saved plan as Result says.

## Result

Plain text for whoever called the skill; the job decides what reaches the user.
Each task is a task line, as the messenger agent's "What you're given" says,
with the estimate only on a task this run picked.

### --auto day

One `today:` line per task planned for today, with `(was <date>)` on one carried
over and `(started)` when work on it has begun, or `today: none`. A stale task
in the blocked status adds `kept: <id> (blocked)`. When today is paused and
empty, the single line `paused`.

### --auto <range>

One `planned:` line per task planned in the range, the user's own dates
included, in day order, or `planned: none`.

### In chat

The saved plan, as Talking to the user about tasks in the conventions says: each
day in order with its tasks, the estimate and reason for each pick, and which
days are paused or empty. Name any date that didn't save.

### Failures

`couldn't move: <id> (write failed)` for each date that still didn't save after
its retry. `Plan FAILED: <what failed>` when the task list or the pauses can't
be read.
