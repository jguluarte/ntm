---
name: board
description: Rules for reading and writing the user's nudge board, in tracker-neutral terms, plus the adapter that maps them to the user's tracker. Load before any board query, and before creating or editing a ticket for the user.
---

# nudge:board

This is not meant to cover every edge case. It's a general guide to working with the user's board; the other skills and the scheduled jobs keep the board self-healing.

## Loading

1. Read `references/config.md`. Every value below that says "from the config" comes from there.
2. Read the adapter named by the config's `tracker` key: `references/adapters/<tracker>.md` (`linear.md` for Linear). It says which tool calls carry out each operation named here. Skills name operations (`fetch open`, `set planned date`, `read note`); the adapter says how.

If the config still holds `~~` placeholders, this copy of the plugin hasn't been set up. Stop and say the user needs to run `/nudge:setup`.

## What this board is

The board is the user's personal tracker: home projects, chores, hobbies, errands, whatever they want to keep moving. It's the backbone of a system built around the places that get in the way: starting tasks, keeping multi-day work moving, and noticing when things have quietly gone stale.

It is one person's system, not a team's. The words here come from trackers built for companies, but they carry none of that weight: a deadline is rare and nothing to worry over, priority is mostly unused, there are no sprints, stakeholders or reviews, and the evening check-in is a friend asking how the day went. Read every rule below at that scale, and keep that scale when writing to the user.

Skills built on this board do three things:

- **Plan.** They give each day one planned task, by setting that task's planned date to the day. The user can add more to a day themselves, and a day they have already dated counts as planned.
- **Remind.** Jobs push the user reminders about the day's tasks.
- **Keep the board honest.** They clear stale dates, and grooming with the user sizes and splits oversized work.

Every rule below exists so that those skills, and any agent working on the board, read it the same way. When a rule seems arbitrary, the purpose above is the tie-breaker.

## Vocabulary

- **Board:** the workspace that holds every ticket (the config's `board name`).
- **Ticket:** one unit of work. Ids look like `<ticket prefix>-<number>`.
- **Project:** a named group of tickets. Projects carry labels their tickets inherit.
- **Container:** a ticket with open sub-tickets.
- **Planned date:** the ticket's one date field, the day the work is planned for.
- **Note:** a shared text the system keeps on the board, found by name (the config's Notes section). A ticket titled with a configured note name is a note, not work; every skill ignores it.

## Workspace

- **Board:** `board name` from the config, with `board id` where the tracker needs it. Ticket ids use `ticket prefix`.
- **Ticket URLs:** use the ticket's own `url` field, one of the standard fields.
- **Scope:** the user is the only person on the board. Consider every ticket in it, regardless of assignee. Never filter by assignee unless explicitly asked.
- **Automations:** if the tracker auto-closes a container when its last sub-ticket closes, or sub-tickets when their parent closes, the adapter says so; cleanup accounts for it.

## Talking to the user about tickets

The user doesn't know what a ticket means by number alone. When you mention a ticket to them, refer to it the way a person would in conversation: a few natural words for what it is, with the id in parentheses after it.

For example, take ABC-15, titled "Replace the kitchen tap". Telling the user "you already finished ABC-15" means nothing to them, and quoting the full title reads like a report, not a person talking. Instead, say "you already finished the kitchen tap (ABC-15)". The example is only an illustration; there's no need to look it up.

Lines another skill parses (like `/nudge:due`'s result lines) keep their format, but when you pass them on to the user, word them this way too.

## Statuses and labels

These are the status classes and labels these rules rely on. The config maps each class to the board's real status names; don't assume other statuses exist.

### Status classes

- **plannable**: open work. The config lists the board's plannable statuses (usually a backlog, a to-do and an in-progress status); the one it names as **started** means work has begun.
- **blocked**: the user can't move it forward right now, because of an open blocking ticket linked to it, a reason described in its comments, or both. Waiting on an order usually gets the `pending-shipment label` instead. Excluded from scheduling (see Standard exclusions). A blocked-by relation alone doesn't make a ticket blocked; see Blocks and blocked by.
- **done**: done.
- **canceled**: closed without being done.
- **duplicate**: ignore it everywhere; the original ticket is what counts.

Nothing outside the plannable class is ever planned. An open ticket is any ticket that isn't done, canceled or duplicate, so a blocked ticket is still open.

### System labels

Names come from the config's Labels section.

- **`no-autoschedule label`:** the user has opted this ticket out of automatic scheduling. Planners never pick it, but once the user dates it themselves, it's reminded about like any other dated ticket.
- **`pending-shipment label`:** something has been ordered for this ticket and hasn't arrived, so the user can't start it.
- **`deadline label`:** a real deadline. This is a personal tracking system, not a business, so the usual meaning of "deadline" doesn't apply here: deadlines are rare, and don't warrant worry or edge-case handling. It goes on a ticket, never a project. A deadline ticket's date is the deadline, not a plan: jobs never move or clear it. Cleanup leaves it alone, planners never re-date it, and the afternoon job stops nudging about one once its date has passed.

Any other label is an ordinary category as far as these rules go. A skill or job can still give a label its own meaning without any change here; the label's description on the board says what it's for.

### Project labels

Projects carry labels too. Any label on a project, system label or ordinary category, counts as a label on every ticket in that project, and on their sub-tickets, so wherever a rule checks a ticket's labels, it checks the ones inherited from its project too. This holds for labels added later as well, with no change to these rules.

## Fetching

The adapter's `fetch open` returns every open ticket with the standard fields: id, title, url, status, status class, priority, estimate, planned date, labels, project, parent id, completed at, updated at. It also lists every project with its name and labels, so inherited labels count (see Project labels), and its summary when a skill asks for it.

- **Scheduling** (planners and reminders): `fetch open`, which includes blocked tickets so parents and ancestors are fully visible. Merge the results and work out which tickets are containers. Keep excluded tickets in the results; Standard exclusions says who skips them. Before planning a candidate, `read ticket` on it and its parent chain to see blockers.
- **Every open ticket** (grooming, and anything else that needs the whole open board): the same fetch, with nothing dropped.
- **Looking back:** the adapter's `fetch closed`.

### Standard exclusions for scheduling

A ticket is excluded when it or any ancestor (project, or parent, parent's parent, and so on) has the `no-autoschedule label`, the `pending-shipment label` or the blocked status.

Planners skip excluded tickets: they never pick or date them. Reminders don't: any open ticket the user has dated gets reminded about, excluded or not.

## Dates

The cloud container's clock is UTC, and the user lives in the config's `timezone`. Always compute dates in that timezone; a bare `date` in the evening can return tomorrow:

```bash
TODAY=$(TZ=<timezone from the config> date +%Y-%m-%d)
```

Compare planned dates as `YYYY-MM-DD` strings.

## Planned dates

A ticket has one date field, the planned date: the day the work is planned for. Planners set, move and clear these dates freely.

A date is **stale** when it's earlier than today (`planned date < TODAY`) and the ticket is still open.

## Estimates

Estimates are Fibonacci points (1, 2, 3, 5, 8, …). They measure complexity and/or effort, not hours:

- **1:** definitely finishes in a night.
- **2:** iffy for one evening; might spill over.
- **3 or more:** definitely a multi-day effort.

Containers aren't estimated; their sub-tickets are. Otherwise, **a ticket with an estimate has been groomed;** one without hasn't. Estimates are set by the user, or with their approval while grooming. Planners use an estimate when one is set and judge size from the title and description otherwise.

## Relationships

How each relation affects scheduling.

### Parent and sub-tickets

- **A ticket with no open sub-tickets** is an ordinary ticket.
- **A parent with open sub-tickets is a container.** Plan its open sub-tickets, never the parent. Its own planned date means nothing to planners, except on a deadline ticket, where it is the deadline.

### Blocks and blocked by

A ticket blocked by open linked tickets, directly or through its parent chain, can be planned for any day after the planned days of all those blockers, never the same day. It doesn't have to be the very next day; any day after works. A blocker's planned day is its planned date. A blocker with no planned date, or a stale one, has no planned day, and the tickets it blocks wait. A planner can date a blocker and then the ticket it blocks in the same run.

#### Example

If ticket `two` is blocked by ticket `one`, then `two` can be planned for Wednesday only if `one` is planned for Tuesday or earlier. If `one` has no planned day, `two` can't be planned yet.

## Writing to the board

The tracker's response says whether a write succeeded. If one fails, retry it once. If it still fails, say so: tell the user in chat, or list it in the result a skill returns.

## Results

Every skill a job calls returns plain text. The first line says what happened; on failure it is `<Skill> FAILED: <why>`. A job's final reply is one line on what happened, unless `nudge:notify` returned `NOTIFY VIA FINAL REPLY`: then the final reply is everything after that line, verbatim, followed by anything else the job's FINAL REPLY calls for. (nudge:ping's lines are `Board OK` / `Board FAILED: …`, the board being what it reports on.)

## Creating tickets when the user asks

The user often files something just so they don't forget it; what it takes gets figured out later, while grooming. Make what they asked for, plainly and in their terms, and don't add meaning they didn't give it.

File it in an existing project that fits, or none. If nothing fits, you can ask whether to make a project for it, as long as the shape makes sense: a specific effort, or a catch-all bucket for a kind of thing.
