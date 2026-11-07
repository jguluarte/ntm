---
name: plan
description: >-
    Plans the user's todo list by setting planned dates, at the rhythm Planning
    in their settings gives, and returns the plan. --auto week fills the week
    ahead and --auto day picks one task for today, unattended; anything else
    plans with the user in chat. Run by the planner agent for the morning and
    weekly planning, or by the user ("plan my week", "plan Thursday around the
    garage").
---

# ntm:plan

## Usage

```
/ntm:plan --auto day
/ntm:plan --auto week
/ntm:plan [<anything>]
```

- `--auto day`: pick one task for today and date it, unattended. The planner
  agent runs it from the morning reminder once it has checked that today is
  empty and not paused; run by the user in chat, their asking is the check.
- `--auto week`: fill each remaining planning day of the week ahead, today
  included, around whatever is already planned, unattended. Run by the planner
  agent from the weekly planning. Plans ahead and Planning days in Planning in
  your settings say what the week is (Monday to Friday by default); on a day
  outside it, plan the next one.
- Anything else: plan with the user in chat, following what they say ("plan the
  week around the garage", "give Thursday something small", "reset today"), and
  asking only if it's still ambiguous. Bare `/ntm:plan` is the week as the span.

## Setup

1. Load `ntm:conventions` and `ntm:pause`. Planning in your settings is how this
   user wants their todo list planned: rhythm, planning days, sizing, a day's
   worth, what's never picked, and anything else they wrote there.
2. Compute `TODAY` as the conventions' Dates section says.
3. Fetch the todo list with the guide's `fetch open`, keeping excluded tickets,
   and work out which tickets are parents.

If any step fails, stop and return `Plan FAILED: <what failed>`.

## Choosing a task

A candidate is an open ticket with a plannable status, no open sub-tickets, and
either no planned date or a stale one, and not one Planning's Never picks rules
out (by default anything carrying the `no-autoschedule` or `pending-shipment`
label, by their real names from Labels, or the blocked status, itself or through
an ancestor). Read each candidate and its ancestors with the guide's
`read ticket` for descriptions and relations. Blocked-by relations follow the
conventions' Blocks and blocked by rule; the picks made in this run count as
planned days, so a chain can fill the week in order.

Pick as many candidates per day as Planning's Rhythm says (one by default),
using judgement, and give each pick a one-line reason. Weigh, roughly in this
order:

- **What's already planned.** When other days this week already hold work,
  prefer picks that build on it: the next pieces of the same chain or project,
  so the week reads as one theme rather than scattered tasks.
- **Small and concrete.** Prefer tasks that fit A day's worth in Planning (about
  an hour by default). Judge size from the title and description, and from the
  estimate on Planning's Sizing scale when one is set. Sometimes something
  bigger needs scheduling, and that's fine: the user can do it on momentum from
  recent days, or break it up themselves.
- **Unblocking.** Prefer work that frees up other open work.
- **Priority, when set.** A priority the user set counts, where the backend has
  one. A missing one means nothing.

Each ticket is planned at most once. If no candidate is left for a day, leave it
unplanned.

### What if a day already has a task?

A day already has a task when any open ticket is planned for that day, whatever
its labels or status. Consider that day planned, however many tasks it holds.
Use its work as a theme to anchor the other days of the week.

## Paused days

Nothing is planned onto a paused day. Before picking a span, run
`/ntm:pause --check <first day> --until <last day>` over it and skip every day
whose line ends `true`. `--auto day` doesn't check: its caller has (the planner
agent), or the user asked. If it returns `Pause FAILED`, stop and return
`Plan FAILED: <its reason>`. A date the user set on a paused day stands.

## Writing

Date each pick with the guide's `set planned date` and change nothing else on
the ticket. Writes follow the conventions; list any that still fail under
`Couldn't write:` in the result.

## --auto week

The span is from `TODAY` to the end of the week ahead as Planning defines it
(Friday by default); on a day outside it, the next week ahead. Only Planning
days get picks.

1. Check the span for paused days, as Paused days says.
2. Give each remaining planning day that doesn't already have a task its picks.
   If no candidate is left, plan nothing.
3. Return the week's plan as Result says.

## --auto day

1. Pick for today as Choosing a task says, and date the pick today.
2. Return today's plan as Result says.

## In chat

Only in chat, with the user. The span is what they name, or the `--auto week`
span when they name none (next week when a day or less of this one is left), or
today when they say "today". Scope words ("the garage") match by project,
parent, label or title; when the words aren't enough to plan from, ask. The
rules above are your defaults, not their limits: the user has the final say.
Advise them when something looks like a problem, such as a blocked chain that
can't finish in the span, then do what they decide.

1. Show the span as it stands: each day's tickets, and which days are paused.
2. Go on what they said. If it isn't enough to plan from, ask what they want the
   span to be about; they may name a project, a goal or a mood, or just say
   "reset it".
3. Propose a plan, leaning toward what they asked for, and keep revising until
   they approve. Any open ticket can move, including one already dated later in
   the week; say which day it leaves empty. Every ticket the plan bumps off a
   day gets its date cleared, unless the user asks to move it to a later day.
   Days they want empty stay empty, and paused days get planned if they want.
4. Before writing, list every date the plan sets and every date it clears,
   including dates they set themselves. When they approve, write them, with
   `set planned date` and `clear planned date`. Return the saved plan as Result
   says, marking days they chose to leave empty `left open`.

## Result

Return plain text for whoever called the skill; the job or skill that called it
decides what to tell the user and how. Typed in chat, present it as the
conventions' "Talking to the user about tickets" says. Write each planned ticket
on its own line as `Planned <date>: <id> <title> (~<time>) <url>`, with your
best guess at how long it takes; a day the user had already dated is listed the
same way. For any ticket this run picked, put its one-line reason on the next
line, indented.

- `--auto week`, or the week in chat: `Week of <Monday's date>`, then the lines
  for each day in order, `<date>: paused` for a paused day and
  `<date>: nothing to plan` for a day nothing qualified for.
- `--auto day`, or today in chat: the lines for today; when nothing qualifies,
  `No task today: nothing to plan.`
- `Couldn't write: <id> (<why>)`, one line per failed write, only when there are
  some.
- `Plan FAILED: <what failed>` when Setup or the pause check fails.
