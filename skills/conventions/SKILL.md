---
name: conventions
description: Rules for reading and writing the user's ntm board, in backend-neutral terms, plus the backend guides that map them onto Linear or Claude Docs. Load before any board query, and before creating or editing a ticket for the user.
---

# ntm:conventions

Version: 0.2.0
Template source: none yet

This is not meant to cover every edge case. It's a general guide to working with the user's board; the other skills and the jobs keep the board self-healing.

## Loading

1. Load `ntm-user:settings` by name and read it by heading: About you, Board, Labels, Notifications, Deviations. Every value below that says "from <section> in your settings" comes from there. A missing section or line means its default. If `ntm-user:settings` won't load, say in one line "not configured; run `/ntm:configure`" and continue with the defaults below. A caller that holds values of its own, such as `ntm:configure-integration`, uses those.
2. Read the backend guide for the backend named in Board: `references/linear.md` for `linear`, `references/claude-docs.md` for `claude-docs`. For any other backend, Board itself says how each operation is done; `references/CONTRACT.md` lists the operations it covers. Skills name operations (`fetch open`, `set planned date`, `read note`); the guide says how.
3. Read Deviations last; see Deviations at the end.

## What this board is

The board is the user's personal ticket system: home projects, chores, hobbies, errands, whatever they want to keep moving. It's the backbone of a system built around the places that get in the way: starting tasks, keeping multi-day work moving, and noticing when things have quietly gone stale.

It is one person's system, not a team's. The words here come from tools built for companies, but they carry none of that weight: a deadline is rare and nothing to worry over, priority is mostly unused, there are no sprints or stakeholders, and the evening check-in is a friend asking how the day went. Read every rule below at that scale, and keep that scale when writing to the user.

Skills built on this board do three things:

- **Plan.** They give each day one planned task, by setting that task's planned date to the day. The user can add more to a day themselves, and a day they have already dated counts as planned.
- **Remind.** Jobs push the user reminders about the day's tasks.
- **Keep the board honest.** They clear stale dates, and grooming with the user sizes and splits oversized work.

Every rule below exists so that those skills, and any agent working on the board, read it the same way. When a rule seems arbitrary, the purpose above is the tie-breaker.

## Vocabulary

- **Board:** the workspace that holds every ticket (Board name in Board).
- **Backend:** the ticket system behind the board: Linear, Claude Docs, or the user's own.
- **Ticket:** one unit of work. Ids look like `<ticket prefix>-<number>`.
- **Project:** a named group of tickets. Projects carry labels their tickets inherit.
- **Parent:** a ticket with open sub-tickets. Never planned itself.
- **Sub-ticket:** a ticket under a parent.
- **Planned date:** the ticket's one date field, the day the work is planned for.
- **Started:** the one plannable status that means work has begun. Jobs give credit for it.
- **Pause:** a day or range when nothing gets planned automatically. Work the user dated themselves still gets its reminders. Kept in the pauses note.
- **Note:** a text the system keeps on the board, found by title (see Notes). A ticket titled with a note's title is a note, not work; every skill ignores it.
- **Label:** a tag on a ticket or project.
- **Estimate:** groomed size, in Fibonacci points.
- **Job:** a scheduled task. Never "trigger", "routine" or "cron job" when talking to the user.

## Workspace

- **Board:** Board name from Board in your settings, with Board id where the backend needs it. Ticket ids use Ticket prefix.
- **Ticket URLs:** use the ticket's own `url` field, one of the standard fields.
- **Scope:** the user is the only person on the board. Consider every ticket in it, regardless of assignee. Never filter by assignee unless explicitly asked.
- **Chat and jobs:** a skill typed in chat runs in the chat. Agents are for jobs; nothing in chat is routed through one.
- **Automations:** if the backend auto-closes a parent when its last sub-ticket closes, or sub-tickets when their parent closes, the backend guide says so; `ntm:fix-todo-list` accounts for it.

## Talking to the user about tickets

The user doesn't know what a ticket means by number alone. When you mention a ticket to them, refer to it the way a person would in conversation: a few natural words for what it is, with the id in parentheses after it.

For example, take ABC-15, titled "Replace the kitchen tap". Telling the user "you already finished ABC-15" means nothing to them, and quoting the full title reads like a report, not a person talking. Instead, say "you already finished the kitchen tap (ABC-15)". The example is only an illustration; there's no need to look it up.

Lines another skill parses (like `/ntm:todo-list`'s result lines) keep their format, but when you pass them on to the user, word them this way too.

A linked ticket is `[<words> (<id>)](<url>)`: the words as this section says, the id in parentheses inside the link text, the url the ticket's own `url` field. `ntm:notify` converts for its channel: Pushover html=1 gets `<a href="<url>"><words> (<id>)</a>`; claude-push keeps the markdown.

## Statuses and labels

These are the status classes and labels these rules rely on. Board in your settings maps each class to the board's real status names; don't assume other statuses exist.

### Status classes

- **plannable**: open work. Board lists the board's plannable statuses (usually a backlog, a to-do and an in-progress status); the one it names as **started** means work has begun.
- **blocked**: the user has put it in the status Board lists as blocked because they can't move it forward right now. What's in the way is an open blocking ticket linked to it, a reason described in its comments, or both. Waiting on an order usually gets the `pending-shipment` label instead. Excluded from scheduling (see Standard exclusions). A blocked-by relation alone doesn't make a ticket blocked; see Blocks and blocked by.
- **done**: done.
- **canceled**: closed without being done.
- **duplicate**: ignore it everywhere; the original ticket is what counts.

Nothing outside the plannable class is ever planned. An open ticket is any ticket that isn't done, canceled or duplicate, so a blocked ticket is still open.

### System labels

The real name for each label is in Labels in your settings; the names below are the defaults.

Issue labels:

- **`no-autoschedule`:** the user has opted this ticket out of automatic scheduling. Planners never pick it, but once the user dates it themselves, it's reminded about like any other dated ticket.
- **`pending-shipment`:** something has been ordered for this ticket and hasn't arrived, so the user can't start it.
- **`deadline`:** a real deadline. This is a personal tracking system, not a business, so the usual meaning of "deadline" doesn't apply here: deadlines are rare, and don't warrant worry or edge-case handling. It goes on a ticket, never a project. A deadline ticket's date is the deadline, not a plan: jobs never move or clear it. `ntm:fix-todo-list` leaves it alone, planners never re-date it, and the afternoon reminder stops mentioning one once its date has passed.
- **`has-amazon-price-watch`:** an Amazon price alert is set for this ticket. `ntm:sync-price-watch-with-amazon` sets and clears it.
- **`amazon-unavailable`:** the item isn't sold new on Amazon, so no alert is set.

Project labels (tickets inherit them; see Project labels):

- **`price-watch`:** the project's tickets are purchases waiting for a good price. There is no `price-watch` issue label.
- **`no-autoschedule`:** as the issue label, for every ticket in the project.

Any other label is an ordinary category as far as these rules go. A skill or job can still give a label its own meaning without any change here; the label's description on the board says what it's for.

### Project labels

Projects carry labels too. Any label on a project, system label or ordinary category, counts as a label on every ticket in that project and on their sub-tickets. Wherever a rule checks a ticket's labels, it checks the ones inherited from its project too. This holds for labels added later as well, with no change to these rules.

Price watch is on when Board names a price watch project; the watched set is the open tickets carrying the `price-watch` project label. There is no separate switch.

## Notes

The title of each note is under Notes in Board in your settings; the defaults are below. Read and write them with the guide's `read note` / `write note`.

- **pauses** (`NTM: pauses`): the pause schedule, under `## Pauses`. `ntm:pause` keeps it.
- **message history** (`NTM: message history`): what reminders have said. Its first line is `Keep: 60 entries or 8 weeks`, written when the note is created; `ntm:style-message` prunes to it.
- **grooming log** (`NTM: grooming log`): `ntm:review-todo-list` keeps it.
- **price watch stores** (`NTM: price watch stores`): kept in the price watch project. `ntm:run-price-watch` keeps it.
- **Amazon alert steps** (`NTM: Amazon alert steps`): `ntm:sync-price-watch-with-amazon` keeps it.

Where the backend has no documents, the guide keeps each note in the description of an open ticket titled with the note's title and labeled `no-autoschedule`; see Notes in `references/CONTRACT.md`.

## Fetching

The guide's `fetch open` returns every open ticket with the standard fields: id, title, url, status, status class, priority, estimate, planned date, labels, project, parent id, completed at, updated at. It also lists every project with its name and labels, so inherited labels count (see Project labels), and its summary when a skill asks for it.

- **Scheduling** (planners and reminders): `fetch open`, which includes blocked tickets so parents and ancestors are fully visible. A ticket is a parent when an open ticket in the results names it as parent id. Keep excluded tickets in the results; Standard exclusions says who skips them. Before planning a candidate, `read ticket` on it and its parent chain to see blockers.
- **Every open ticket** (grooming, and anything else that needs the whole open board): the same fetch, with nothing dropped.
- **Looking back:** the guide's `fetch closed`.

### Standard exclusions for scheduling

A ticket is excluded when it or any ancestor (project, or parent, parent's parent, and so on) has the `no-autoschedule` label, the `pending-shipment` label or the blocked status.

Planners skip excluded tickets: they never pick or date them. Reminders don't: any open ticket the user has dated gets reminded about, excluded or not.

Planners also never plan onto a paused day (`/ntm:pause --check` over the span says which days are). A date the user set on a paused day stands, and gets its reminders.

## Dates

The session's clock is UTC, and the user lives in the timezone in About you. Always compute dates in that timezone; a bare `date` in the evening can return tomorrow:

```bash
TODAY=$(TZ=<timezone from About you in your settings> date +%Y-%m-%d)
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

Parents aren't estimated; their sub-tickets are. Otherwise, **a ticket with an estimate has been groomed;** one without hasn't. Estimates are set by the user, or with their approval while grooming. Planners use an estimate when one is set and judge size from the title and description otherwise.

## Relationships

How each relation affects scheduling.

### Parent and sub-tickets

- **A ticket with no open sub-tickets** is an ordinary ticket.
- **A ticket with open sub-tickets is a parent.** Plan its open sub-tickets, never the parent. Its own planned date means nothing to planners, except on a deadline ticket, where it is the deadline.

### Blocks and blocked by

A ticket blocked by open linked tickets, directly or through its parent chain, can be planned for any day after the planned days of all those blockers. Never the same day, but not necessarily the next either: any later day works. A blocker's planned day is its planned date. A blocker with no planned date, or a stale one, has no planned day, and the tickets it blocks wait. A planner can date a blocker and then the ticket it blocks in the same run.

#### Example

If ticket `two` is blocked by ticket `one`, then `two` can be planned for Wednesday only if `one` is planned for Tuesday or earlier. If `one` has no planned day, `two` can't be planned yet.

## Writing to the board

The backend's response says whether a write succeeded. If one fails, retry it once. If it still fails, say so: tell the user in chat, or list it in the result a skill returns.

## Results

Skills return text; jobs decide what reaches the user. No skill other than `ntm:notify` sends anything.

Every skill a job calls returns plain text. A skill's status line (OK / FAILED) starts with its own name, capitalised, hyphens kept (`Plan FAILED: …`, `Fix-todo-list FAILED: …`, `Ready-check OK`); its data lines (`Planned by <TODAY> (<n>):`, `Done (<n>):`, `YYYY-MM-DD: true`) are its own format, listed in the skill. A job's final reply is one line on what happened. When `ntm:notify` returned `NOTIFY VIA FINAL REPLY`, the final reply is instead the notification's title as its first line and the message under it, nothing else. The weekly planning job adds fix-todo-list's result after the message.

## Creating tickets when the user asks

The user often files something just so they don't forget it; what it takes gets figured out later, while grooming. Make what they asked for, plainly and in their terms, and don't add meaning they didn't give it.

File it in an existing project that fits, or none. If nothing fits, you can ask whether to make a project for it, as long as the shape makes sense: a specific effort, or a catch-all bucket for a kind of thing.

## Deviations

Read Deviations in your settings last. Anything written there is how this user does things, and it overrides the rules above: where it names a value, that value wins; where it describes a rule, follow it as written. An empty section changes nothing.
