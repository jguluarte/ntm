---
name: plan
description: Plans the user's ntm board, one task per weekday, by setting planned dates, and returns the plan. --auto week fills the week and --auto day makes sure today has a task, unattended; anything else plans with the user in chat. Run by the morning and weekly planning jobs, or by the user ("plan my week", "what's today's task", "plan Thursday around the garage").
---

# ntm:plan

## Usage

```
/ntm:plan --auto day
/ntm:plan --auto week
/ntm:plan [<anything>]
```

- `--auto day`: make sure today has a planned task, unattended. Used by the morning reminder. On a weekend, it plans that day: the user asked for a job that day.
- `--auto week`: fill each remaining weekday this week, today included, around whatever is already planned, unattended. Used by weekly planning. Planning is weekday-based: `--auto week` plans Monday to Friday, and on a weekend it plans next Monday to Friday.
- Anything else: plan with the user in chat, following what they say ("plan the week around the garage", "give Thursday something small", "reset today"), and asking only if it's still ambiguous. Bare `/ntm:plan` is the week as the span.

## Setup

1. Load `ntm:conventions` and `ntm:pause`.
2. Compute `TODAY` as the conventions' Dates section says.
3. Fetch the board as the conventions' Scheduling fetch says, keeping excluded tickets, and work out which tickets are parents.

If any step fails, stop and return `Plan FAILED: <what failed>`.

## Choosing a task

A candidate is an open ticket with a plannable status, no open sub-tickets, and either no planned date or a stale one. It must not be excluded by the conventions' Standard exclusions, so never a ticket carrying the `no-autoschedule` label (by its real name from Labels in your settings). A deadline ticket's own date is never stale for this purpose. Read each candidate and its ancestors with the guide's `read ticket` for descriptions and relations. Blocked-by relations follow the conventions' Blocks and blocked by rule; the picks made in this run count as planned days, so a chain can fill the week in order.

Pick one candidate per day, using judgement, and give each pick a one-line reason. Weigh, roughly in this order:

- **Deadlines.** A ticket with the `deadline` label (its real name from Labels) is a deadline ticket, and its planned date is the deadline for its sub-tickets. More than about two months out, treat each sub-ticket as an ordinary candidate. Closer than that, aim to finish its chain about a month before the deadline; if there isn't a month left, finish it by the deadline, in order. A renewal falling in mid-October gets planned in mid-September. Never plan past the deadline day. Once the deadline day has passed, its sub-tickets are ordinary candidates again.
- **What's already planned.** When other days this week already hold work, prefer picks that build on it: the next pieces of the same chain or project, so the week reads as one theme rather than scattered tasks.
- **Small and concrete.** Prefer tasks that look doable within an hour. Judge size from the title and description, and from the estimate when one is set. Sometimes something bigger needs scheduling, and that's fine: the user can do it on momentum from recent days, or break it up themselves.
- **Unblocking.** Prefer work that frees up other open work.
- **Priority, when set.** A priority the user set counts, where the backend has one. A missing one means nothing.

Each ticket is planned at most once. If no candidate is left for a day, leave it unplanned.

### What if a day already has a task?

A day already has a task when any open ticket is planned for that day, whatever its labels or status. Consider that day planned, however many tasks it holds. Use its work as a theme to anchor the other days of the week.

## Paused days

Nothing is planned onto a paused day. Before picking, run `/ntm:pause --check <first day> --until <last day>` over the span (`/ntm:pause --check` alone for today), and skip every day whose line ends `true`. If it returns `Pause FAILED`, stop and return `Plan FAILED: <its reason>`. A date the user set on a paused day stands.

## Writing

Date each pick with the guide's `set planned date` and change nothing else on the ticket. Writes follow the conventions; list any that still fail under `Couldn't write:` in the result.

## --auto week

Plan from `TODAY` through Friday. Run on a Saturday or Sunday, plan next Monday through Friday instead.

1. Check the span for paused days, as Paused days says.
2. Give each remaining day that doesn't already have a task one pick. If none are left, plan nothing.
3. Return the week's plan as Result says.

## --auto day

1. Check today, as Paused days says. If today is paused, change nothing and return `No task today: paused.`
2. If today has no task, pick one as above and date it today.
3. Return today's plan as Result says.

## In chat

Only in chat, with the user. The span is what they name, or the `--auto week` span when they name none, or today when they say "today". The rules above are your defaults, not their limits: the user has the final say. Advise them when something looks like a problem, such as work that won't fit before a deadline, then do what they decide.

1. Show the span as it stands: each day's tickets, and which days are paused.
2. Go on what they said. If it isn't enough to plan from, ask once what they want the span to be about; they may name a project, a goal or a mood, or just say "reset it".
3. Propose a plan, leaning toward what they asked for, and keep revising until they approve. Any open ticket can move, including one already dated later in the week; say which day it leaves empty. Every ticket the plan bumps off a day gets its date cleared, unless the user asks to move it to a later day. Days they want empty stay empty, and paused days get planned if they want.
4. Before writing, list every date the plan sets and every date it clears, including dates they set themselves. When they approve, write them, with `set planned date` and `clear planned date`. Return the saved plan as Result says, marking days they chose to leave empty `left open`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write each planned ticket on its own line as `Planned <date>: <id> <title> <url> (~<how long>)`, with your best guess at how long it takes. For any ticket this run picked, put its one-line reason on the next line, indented.

- `--auto week`, or the week in chat: `Week of <Monday's date>`, then the lines for each day in order, `<date>: paused` for a paused day and `<date>: nothing to plan` for a day nothing qualified for.
- `--auto day`, or today in chat: the lines for today. On a paused day, `No task today: paused.`; when nothing is planned and nothing qualifies, `No task today: nothing to plan.`
- `Couldn't write:` with any failed writes, only when there are some.
- `Plan FAILED: <what failed>` when Setup or the pause check fails.
