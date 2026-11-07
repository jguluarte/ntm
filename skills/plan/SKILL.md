---
name: plan
description: >-
    Plans the user's todo list by setting planned dates, at the rhythm Planning
    in their settings gives, and returns the plan. --auto day makes today ready
    (carries stale work to today, plans today if it's empty); --auto week closes
    out the week and plans the next; anything else plans with the user in chat.
    Run by the morning reminder and the weekly planning, or by the user ("plan
    my week", "plan Thursday around the garage").
---

# ntm:plan

## Usage

```
/ntm:plan --auto day
/ntm:plan --auto week
/ntm:plan [<anything>]
```

- `--auto day`: make today ready, unattended. Carries stale work to today, then
  picks one task for today when nothing is planned and today isn't paused. Run
  by the morning reminder.
- `--auto week`: close out the week and plan the next, unattended. Reports what
  got done and what's still open, tidies the todo list, then fills each
  remaining planning day of the week ahead around whatever is already planned.
  Run by the weekly planning.
- Anything else: plan with the user in chat, following what they say ("plan the
  week around the garage", "give Thursday something small", "reset today"), and
  asking only if it's still ambiguous. Bare `/ntm:plan` is the week as the span.

The user vets their own todo list: every task is real work they want kept
moving, and the pauses are theirs. Set, move and clear planned dates as this
skill says, and change nothing else on a task.

## Setup

1. Load `ntm:conventions` and `ntm:pause`. Planning in your settings is how this
   user wants their todo list planned: rhythm, planning days, how far ahead the
   week plans, sizing, a day's worth, what's never picked, and anything else
   they wrote there.
2. Compute `TODAY` as the conventions' Dates section says.
3. Fetch the todo list with the guide's `fetch open`, keeping excluded tasks,
   and work out which tasks are parents. `--auto week` fetches after its tidy.

If any step fails, stop and return `Plan FAILED: <what failed>`.

## Choosing a task

A candidate is an open task with a plannable status, no open sub-tasks, and
either no planned date or a stale one, and not one Planning's Never picks rules
out (by default anything carrying the $no-autoschedule or $pending-shipment
label, by their real names from Labels, or the blocked status, itself or through
an ancestor). Read each candidate and its ancestors with the guide's `read task`
for descriptions and relations. Blocked-by relations follow the conventions'
Blocks and blocked by rule; the picks made in this run count as planned days, so
a chain can fill the week in order.

Pick as many candidates per day as Planning's Rhythm says (one by default),
using judgement; in chat, give each pick a one-line reason. Weigh, roughly in
this order:

- **What's already planned.** When other days this week already hold work,
  prefer picks that build on it: the next pieces of the same chain or project,
  so the week reads as one theme rather than scattered tasks.
- **Small and concrete.** Prefer tasks that fit A day's worth in Planning (about
  an hour by default), judging by the time the estimator gives (see A task's
  time). Sometimes something bigger needs scheduling, and that's fine: the user
  can do it on momentum from recent days, or break it up themselves.
- **Unblocking.** Prefer work that frees up other open work.
- **Priority, when set.** A priority the user set counts, where the backend has
  one. A missing one means nothing.

Each task is planned at most once. If no candidate is left for a day, leave it
unplanned.

### What if a day already has a task?

A day already has a task when any open task is planned for that day, whatever
its labels or status. Consider that day planned, however many tasks it holds.
Use its work as a theme to anchor the other days of the week.

## A task's time

Every task the result lists shows how long it should take, so the user can see
what the day asks of them. Ask the estimator agent's Time tasks once per run,
with every task that needs a time: the candidates when the run picks, and every
task the result lists. When the agent isn't loaded, follow its file as the
conventions' "Chat, jobs and agents" says.

## Paused days

Nothing is planned onto a paused day. Before picking for a span, run
`/ntm:pause --check <first day> --until <last day>` over it and skip every day
whose line ends `true`. If it returns `Pause FAILED`, stop and return
`Plan FAILED: <its reason>`. A date the user set on a paused day stands.

## Writing

Date each pick with the guide's `set planned date`. Writes follow the
conventions; Result says how to list any that still fail.

## --auto day

1. **Carry over.** Every task planned before `TODAY` is stale. Move the ones in
   the plannable class to `TODAY` with `set planned date`, whatever their labels
   and even when one blocks another: the user dated them, so they should just
   work (the conventions' Blocks rule is for picking work; carrying a date isn't
   picking). A stale task in the blocked class keeps its date. Carry over on a
   paused day too.
2. **Today.** If nothing is planned for `TODAY` after the moves, check today as
   Paused days says. Paused: return `paused` and stop. Otherwise pick for today
   as Choosing a task says, and date the pick today.
3. Return today's plan as Result says.

## --auto week

Plans ahead in Planning says how far the week ahead reaches (one week, Monday to
Friday, by default); on a day outside it, plan the next one. The span looked
back on is as long, ending today: 7 days for one week, 14 for two weeks, the
calendar month for the month.

1. Load `ntm:show-completed` and `ntm:fix-todo-list`. Run
   `/ntm:show-completed <the span looked back on> and what's still open` first,
   so it counts nothing the tidy closes. `Show-completed FAILED` isn't an error
   here: carry on with `done: unavailable`.
2. Run `/ntm:fix-todo-list`, so planning works from a tidy todo list.
   `Fix-todo-list FAILED` isn't an error here either: carry on.
3. Fetch as Setup says. The span is from `TODAY` to the end of the week ahead;
   only Planning days get picks. Check it for paused days, as Paused days says.
4. Give each remaining planning day that doesn't already have a task its picks.
   If no candidate is left, plan nothing.
5. Return the week as Result says.

## In chat

Only in chat, with the user. The span is what they name, or the `--auto week`
span when they name none (next week when a day or less of this one is left), or
today when they say "today". A day they name gets planned even when Planning
days or Deviations would leave it out, such as a weekend; say in one line that
it goes against their settings. Scope words ("the garage") match by project,
parent, label or title; when the words aren't enough to plan from, ask. The
rules above are your defaults, not their limits: the user has the final say.
Advise them when something looks like a problem, such as a blocked chain that
can't finish in the span, then do what they decide.

1. Show the span as it stands: each day's tasks, and which days are paused.
2. Go on what they said. If it isn't enough to plan from, ask what they want the
   span to be about; they may name a project, a goal or a mood, or just say
   "reset it".
3. Propose a plan, leaning toward what they asked for, and keep revising until
   they approve. Any open task can move, including one already dated later in
   the week; say which day it leaves empty. Every task the plan bumps off a day
   gets its date cleared, unless the user asks to move it to a later day. Days
   they want empty stay empty, and paused days get planned if they want.
4. Before writing, list every date the plan sets and every date it clears,
   including dates they set themselves. When they approve, write them, with
   `set planned date` and `clear planned date`. Show the saved plan as Result
   says.

## Result

Return plain text for whoever called the skill; the job or skill that called it
decides what reaches the user. The reminders hand these lines to the messenger
as they are.

- `--auto day`: one `today:` line per task planned for `TODAY`:
  `today: <id> <title> (~<time>) <url>`, then ` (was <date>)` on a task carried
  over, the date it had, then ` (started)` when its status is the started one.
  When nothing is planned and nothing qualified, the single line `today: none`.
  A stale task left where it was: `kept: <id> (blocked)`. How many days a task
  has slipped is the style's to count, from the message history; don't compute
  it here.
- `--auto week`: one `done:` line per task that closed in the span looked back
  on (`done: <id> <title> <url>`), or `done: none`, or `done: unavailable`; one
  `open:` line per task still open from it (`open: <id> <title> <url>`, then
  ` (was <date>)` when its planned date is before `TODAY`), or `open: none`; one
  `planned:` line per task planned in the week ahead, days the user had already
  dated included, in day order
  (`planned: <date>: <id> <title> (~<time>) <url>`), or the single line
  `planned: none`; then every line fix-todo-list returned, each prefixed `fix: `
  (a `Fix-todo-list FAILED: …` line the same way).
- Both: `couldn't move: <id> (write failed)` for each write that still failed.
- In chat: the saved plan, presented as the conventions' "Talking to the user
  about tasks" says: each day in order with its tasks and their times, the
  reason for each task this run picked, and which days are paused, left open or
  had nothing to plan. Name any write that failed.
- `Plan FAILED: <what failed>` when Setup or the pause check fails.
