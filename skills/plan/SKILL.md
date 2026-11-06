---
name: plan
description: Plans the user's nudge board, one task per weekday, by setting planned dates, and returns the plan. --weekly fills the week; --daily makes sure today has a task; --replan reworks either with the user in chat. Run by the morning and week jobs, or by the user ("plan my week", "what's today's task").
---

# nudge:plan

## Usage

```
/nudge:plan --weekly [--replan]
/nudge:plan --daily [--replan]
```

- `--weekly`: fill each remaining weekday this week, today included, around whatever is already planned. On a weekend, plan next Monday to Friday. Planning is weekday-based: `--weekly` plans Monday to Friday, and a morning job that runs on a weekend plans that day with `--daily`.
- `--daily`: make sure today has a planned task.
- `--replan`: in chat, rework the week (with `--weekly`) or today (with `--daily`) with the user, instead of planning on your own.

## Setup

1. Load `nudge:board` and `nudge:days-off`.
2. Compute `TODAY` as the board rules' Dates section says.
3. Fetch the board as the board rules' Scheduling fetch says, keeping excluded tickets, and work out containers.

If any step fails, stop and return `Plan FAILED: <what failed>`.

## Choosing a task

A candidate is an open ticket with a plannable status that isn't excluded by the board rules' Standard exclusions (so never a ticket with the `no-autoschedule label`), no open sub-tickets, and either no planned date or a stale one. A deadline ticket's own date is never stale for this purpose. Read each candidate and its ancestors with the adapter's `read ticket` for descriptions and relations. Blocked-by relations follow the board rules' Blocks and blocked by rule; the picks made in this run count as planned days, so a chain can fill the week in order.

Pick one candidate per day, using judgement, and give each pick a one-line reason. Weigh, roughly in this order:

- **Deadlines.** A ticket with the `deadline label` is a deadline ticket, and its planned date is the deadline for its sub-tickets. More than about two months out, treat each sub-ticket as an ordinary candidate. Closer than that, aim to finish its chain about a month before the deadline; if there isn't a month left, finish it by the deadline, in order. A renewal falling in mid-October gets planned in mid-September. Never plan past the deadline day. Once the deadline day has passed, its sub-tickets are ordinary candidates again.
- **What's already planned.** When other days this week already hold work, prefer picks that build on it: the next pieces of the same chain or project, so the week reads as one theme rather than scattered tasks.
- **Small and concrete.** Prefer tasks that look doable within an hour. Judge size from the title and description, and from the estimate when one is set. Sometimes something bigger needs scheduling, and that's fine: the user can do it on momentum from recent days, or break it up themselves.
- **Unblocking.** Prefer work that frees up other open work.
- **Priority, when set.** A priority the user set counts, where the tracker has one. A missing one means nothing.

Each ticket is planned at most once. If no candidate is left for a day, leave it unplanned.

### What if a day already has a task?

A day already has a task when any open ticket is planned for that day, whatever its labels or status. Consider that day planned, however many tasks it holds. Use its work as a theme to anchor the other days of the week.

## Writing

Date each pick with the adapter's `set planned date` and change nothing else on the ticket. Writes follow the board rules; list any that still fail under `Couldn't write:` in the result.

## --weekly

Plan from `TODAY` through Friday. Run on a Saturday or Sunday, plan next Monday through Friday instead.

1. Run `/nudge:days-off --check <first day> --until <last day>`, and skip every day whose line ends `true`. If it returns `Days off FAILED`, stop and return `Plan FAILED: <its reason>`.
2. Give each remaining day that doesn't already have a task one pick. If none are left, plan nothing.
3. Return the week's plan as Result says.

## --daily

1. Run `/nudge:days-off --check`. If today is a day off, change nothing and return `No task today: day off.` If it returns `Days off FAILED`, stop and return `Plan FAILED: <its reason>`.
2. If today has no task, pick one as above and date it today.
3. Return today's plan as Result says.

## --replan

Only in chat, with the user, on the `--weekly` span or on today with `--daily`. The rules above are your defaults, not their limits: the user has the final say. Advise them when something looks like a problem, such as work that won't fit before a deadline, then do what they decide.

1. Show the span as it stands: each day's tickets, and which days are days off.
2. Unless they already said, ask what they want it to be about. They may name a project, a goal or a mood, or just say "reset it".
3. Propose a plan, leaning toward what they asked for, and keep revising until they approve. Any open ticket can move, including one already dated later in the week; say which day it leaves empty. Every ticket the plan bumps off a day gets its date cleared, unless the user asks to move it to a later day. Days they want empty stay empty, and days off get planned if they want.
4. Before writing, list every date the plan sets and every date it clears, including dates they set themselves. When they approve, write them, with `set planned date` and `clear planned date`. Return the saved plan as Result says, marking days they chose to leave empty `left open`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write each ticket as `<ID> <title> (~<time>) <url>`, with your best guess at the time, and the one-line reason for any this run picked.

- `--weekly`: `Week of <Monday's date>`, then `<date>:` for each day with every ticket planned for that day on its own line under it, `<date>: day off` for a day off and `<date>: nothing to plan` for a day nothing qualified for.
- `--daily`: `<date>:` then each ticket planned for today, one per line. On a day off, `No task today: day off.`; when nothing is planned and nothing qualifies, `No task today: nothing to plan.`
- `Couldn't write:` with any failed writes, only when there are some.
- `Plan FAILED: <what failed>` when Setup or the days-off check fails.
