---
name: conventions
description: >-
    Rules for reading and writing the user's todo list, in backend-neutral
    terms, plus the backend guides that map them onto Linear or Claude Docs.
    Load before any list query, and before creating or editing a ticket for the
    user.
---

# ntm:conventions

Version: 0.3.2

Template source: none yet

This is a general guide to working with the user's todo list, not a rulebook for
every edge. The other skills and the jobs keep the todo list self-healing. Every
value these rules depend on is one the user agreed to during setup and can
change in `ntm-user:settings`; the rules here name the value, the settings hold
it.

## Loading

1. Load `ntm-user:settings` by name and read it by heading: About you, Todo
   list, Labels, Planning, Shopping, Notifications, Deviations. Every value
   below that says "from <section> in your settings" comes from there. A missing
   section or line means its default. If `ntm-user:settings` won't load, say in
   one line "not configured; run `/ntm:configure`" and continue with the
   defaults below. A caller that holds values of its own, such as
   `ntm:configure-todo-list`, uses those.
2. Read the backend guide for the backend named in Todo list:
   `references/linear.md` for `linear`, `references/claude-docs.md` for
   `claude-docs`. For any other backend, Todo list itself says how each
   operation is done; `references/CONTRACT.md` lists the operations it covers.
   Skills name operations (`fetch open`, `set planned date`, `read note`); the
   guide says how.
3. Read Deviations last; see Deviations at the end.

## What this todo list is

The todo list is the user's personal task system: home projects, chores,
hobbies, errands, things to buy when the price is right, whatever they want to
keep moving or not forget. It's the backbone of a system built around the places
that get in the way: starting tasks, keeping multi-day work moving, noticing
when things have quietly gone stale, and buying on a good price instead of on
impulse.

It is one person's system, not a team's. The words here come from tools built
for companies, but they carry none of that weight: there are no sprints or
stakeholders, priority is mostly unused, a hard due date is rare and the user
plans it by hand, and the evening check-in is a friend asking how the day went.
Read every rule below at that scale, and keep that scale when writing to the
user.

Skills built on this todo list do three things:

- **Plan.** They give each planning day one planned task, by setting that task's
  planned date to the day. The user can add more to a day themselves, and a day
  they have already dated counts as planned.
- **Remind.** Jobs push the user reminders about the day's tasks.
- **Keep the todo list honest.** They clear stale dates, and grooming with the
  user sizes and splits oversized work.

Every rule below exists so that those skills, and any agent working on the todo
list, read it the same way. When a rule seems arbitrary, the purpose above is
the tie-breaker.

## Vocabulary

- **Todo list:** the place that holds every ticket (List name under Todo list in
  your settings): a Linear team, a Claude Doc, a Todoist project, whatever the
  user keeps tasks in.
- **Backend:** the system behind the todo list: Linear, Claude Docs, or the
  user's own.
- **Ticket:** one thing on the todo list. This plugin's word for it; the user's
  system may call it an issue, a task, a todo or a reminder, and so may the
  user. Ids look like `<ticket prefix>-<number>` where the backend has a prefix.
- **Project:** a named group of tickets, whatever the backend calls it. Projects
  carry labels their tickets inherit.
- **Parent:** a ticket with open sub-tickets.
- **Sub-ticket:** a ticket under a parent, where the backend has that relation.
- **Planned date:** the ticket's one date field, the day the work is planned
  for.
- **Started:** the one plannable status that means work has begun. Jobs give
  credit for it.
- **Pause:** a day or range when nothing gets planned automatically. Work the
  user dated themselves still gets its reminders. Kept in the pauses note.
- **Note:** a text the system keeps on the todo list, found by title (see
  Notes). A ticket titled with a note's title is a note, not work; every skill
  ignores it.
- **Label:** a tag on a ticket or project.
- **Estimate:** groomed size, on the scale Planning in your settings names.
- **Job:** a scheduled task. Never "trigger", "routine" or "cron job" when
  talking to the user.

## Workspace

- **Todo list:** List name from Todo list in your settings, with List id where
  the backend needs it. Ticket ids use Ticket prefix.
- **Ticket URLs:** use the ticket's own `url` field, one of the standard fields.
- **Scope:** the user is the only person on the todo list. Consider every ticket
  in it, regardless of assignee. Never filter by assignee unless explicitly
  asked.
- **Chat, jobs and agents:** a skill typed in chat runs in the chat. The
  reminder skills, `completed --notify` and the price watch hand their work to
  the plugin's agents (planner, messenger, shopper), in a job or in chat alike;
  each says what it hands over. When an agent isn't available in the session,
  read its file from the installed plugin and do what it says yourself, with the
  same request:
  `find ~/.claude/plugins -path '*ntm*' -path '*/agents/<name>.md'` (the plugin
  may sit under a versioned folder; the two `-path` tests find it either way).
  One copy of each procedure, either way; say nothing to the user about which
  way it ran.
- **Automations:** if the backend auto-closes a parent when its last sub-ticket
  closes, or sub-tickets when their parent closes, the backend guide says so;
  `ntm:fix-todo-list` accounts for it.

## Talking to the user about tickets

The user doesn't know what a ticket means by number alone. When you mention a
ticket to them, refer to it the way a person would in conversation: a few
natural words for what it is, with the id in parentheses after it.

For example, take ABC-15, titled "Replace the kitchen tap". Telling the user
"you already finished ABC-15" means nothing to them, and quoting the full title
reads like a report, not a person talking. Instead, say "you already finished
the kitchen tap (ABC-15)". The example is only an illustration; there's no need
to look it up. Where the backend has no ids, the words alone.

Lines another skill parses (like `/ntm:today`'s result lines) keep their format,
but when you pass them on to the user, word them this way too.

A linked ticket is `[<words> (<id>)](<url>)`: the words as this section says,
the id in parentheses inside the link text, the url the ticket's own `url`
field. `ntm:notify` converts for its channel: Pushover html=1 gets
`<a href="<url>"><words> (<id>)</a>`; claude-push keeps the markdown.

## Statuses and labels

Todo list in your settings maps each status class to the list's real status
names, and Labels gives the real name of each label the system uses. Don't
assume other statuses exist. The defaults below are what
`/ntm:configure-todo-list` proposes; the user's todo list may use other names,
and the settings are what count.

### Status classes

- **plannable**: open work. Todo list in your settings lists the plannable
  statuses (usually a backlog, a to-do and an in-progress status); the one it
  names as **started** means work has begun.
- **blocked**: the user has put it in the status Todo list in your settings
  names as blocked because they can't move it forward right now. What's in the
  way is an open blocking ticket linked to it, a reason described in its
  comments, or both. Waiting on an order usually gets the `pending-shipment`
  label instead. A blocked-by relation alone doesn't make a ticket blocked; see
  Blocks and blocked by. Blank in Todo list when the todo list has no such
  status.
- **done**: done.
- **canceled**: closed without being done.
- **duplicate**: ignore it everywhere; the original ticket is what counts.

Nothing outside the plannable class is ever planned. An open ticket is any
ticket that isn't done, canceled or duplicate, so a blocked ticket is still
open.

### System labels

Each label below is named by its line in Labels in your settings; the names
shown are the defaults.

Ticket labels:

- **`no-autoschedule`:** the user has opted this ticket out of automatic
  planning. Planners never pick it, but once the user dates it themselves, it's
  reminded about like any other dated ticket.
- **`pending-shipment`:** something has been ordered for this ticket and hasn't
  arrived, so the user can't start it.
- **`has-amazon-alert`:** an Amazon price alert is set for this ticket.
  `ntm:sync-price-watch-to-amazon` sets and clears it.
- **`amazon-unavailable`:** the item isn't sold new on Amazon, so no alert is
  set.

Project labels (tickets inherit them; see Project labels):

- **`price-watch`:** the project's tickets are purchases waiting for a good
  price. There is no `price-watch` ticket label.
- **`no-autoschedule`:** as the ticket label, for every ticket in the project.

Any other label is an ordinary category as far as these rules go. A skill or job
can still give a label its own meaning without any change here; the label's
description on the todo list says what it's for.

### Project labels

Projects carry labels too. Any label on a project, system label or ordinary
category, counts as a label on every ticket in that project and on their
sub-tickets. Wherever a rule checks a ticket's labels, it checks the ones
inherited from its project too. This holds for labels added later as well, with
no change to these rules. Where the backend can't put labels on groups, the
guide says so and the user puts the labels on tickets directly.

Price watch is on when Todo list names a price watch project; the watched set is
the open tickets carrying the `price-watch` project label. There is no separate
switch.

## Notes

The title of each note is under Notes under Todo list in your settings; the
defaults are the plain names below. Read and write them with the guide's
`read note` / `write note`. Each note has one writer; everything else only reads
it.

- **pauses** (default title `Pauses`): the pause schedule, under `## Pauses`.
  `ntm:pause` keeps it.
- **message history** (`Message history`): what reminders have said. Its first
  line is a `Keep:` line that `ntm-user:style`, its writer, prunes to; the style
  template says what it writes.
- **grooming log** (`Grooming log`): `ntm:configure-todo-list` keeps it.
- **price watch stores** (`Price watch stores`): kept in the price watch
  project. `ntm:price-watch` keeps it, from the user's vouch and block replies;
  the shopper reads it.
- **Amazon alert steps** (`Amazon alert steps`):
  `ntm:sync-price-watch-to-amazon` keeps it.

Where the backend has no documents, the guide keeps each note in the description
of an open ticket titled with the note's title and labeled `no-autoschedule`;
see Notes in `references/CONTRACT.md`.

## Fetching

The guide's `fetch open` returns every open ticket with the standard fields: id,
title, url, status, status class, priority, estimate, planned date, labels,
project, parent id, completed at, updated at. It also lists every project with
its name and labels, so inherited labels count (see Project labels), and its
summary when a skill asks for it.

- **For planning and reminders:** `fetch open`, which includes blocked tickets
  so parents and ancestors are fully visible. A ticket is a parent when an open
  ticket in the results names it as parent id. Keep excluded tickets in the
  results; Never picks says who skips them. Before planning a candidate,
  `read ticket` on it and its parent chain to see blockers.
- **Every open ticket** (grooming, and anything else that needs the whole open
  todo list): the same fetch, with nothing dropped.
- **Looking back:** the guide's `fetch closed`.

### Never picks

Never picks in Planning in your settings lists what planners never pick; the
default is: a ticket that, itself or through any ancestor (project, or parent,
parent's parent, and so on), has the `no-autoschedule` label, the
`pending-shipment` label or the blocked status.

Planners skip excluded tickets: they never pick or date them. Reminders don't:
any open ticket the user has dated gets reminded about, excluded or not.

Planners also never plan onto a paused day (`/ntm:pause --check` over the span
says which days are). A date the user set on a paused day stands, and gets its
reminders.

## Dates

The session's clock is UTC, and the user lives in the timezone in About you.
Always compute dates in that timezone; a bare `date` in the evening can return
tomorrow:

```bash
TODAY=$(TZ=<timezone from About you in your settings> date +%Y-%m-%d)
```

Compare planned dates as `YYYY-MM-DD` strings.

## Planned dates

A ticket has one date field, the planned date: the day the work is planned for.
Planners set, move and clear these dates freely.

A date is **stale** when it's earlier than today (`planned date < TODAY`) and
the ticket is still open.

## Estimates

Sizing in Planning in your settings says what an estimate means on this todo
list. The default scale is Fibonacci points (1, 2, 3, 5, 8, …) measuring
complexity and effort, not hours: 1 definitely finishes in a night; 2 is iffy
for one evening; 3 or more is a multi-day effort.

Parents aren't estimated; their sub-tickets are. Otherwise, **a ticket with an
estimate has been groomed;** one without hasn't. Estimates are set by the user,
or with their approval while grooming. Planners use an estimate when one is set
and judge size from the title and description otherwise. On a backend with no
estimate field, the grooming log's Estimates block is the record.

## Relationships

How each relation affects planning. Planning in your settings can say otherwise;
these are the defaults.

### Parent and sub-tickets

- **A ticket with no open sub-tickets** is an ordinary ticket.
- **A ticket with open sub-tickets is a parent.** Plan its open sub-tickets,
  never the parent; its own planned date means nothing to planners.

### Blocks and blocked by

A ticket blocked by open linked tickets, directly or through its parent chain,
can be planned for any day after the planned days of all those blockers. Never
the same day, but not necessarily the next either: any later day works. A
blocker's planned day is its planned date. A blocker with no planned date, or a
stale one, has no planned day, and the tickets it blocks wait. A planner can
date a blocker and then the ticket it blocks in the same run. The user also uses
blocked-by loosely, to push one thing behind another; that's fine, and nothing
to query.

#### Example

If ticket `two` is blocked by ticket `one`, then `two` can be planned for
Wednesday only if `one` is planned for Tuesday or earlier. If `one` has no
planned day, `two` can't be planned yet.

## Writing to the todo list

The backend's response says whether a write succeeded. If one fails, retry it
once. If it still fails, say so: tell the user in chat, or list it in the result
a skill returns.

## Results

Skills return text; jobs decide what reaches the user. No skill other than
`ntm:notify` sends anything.

Every skill a job calls returns plain text. A skill's status line (OK / FAILED)
starts with its own name, capitalised, hyphens kept (`Plan FAILED: …`,
`Fix-todo-list FAILED: …`, `Ready-check OK`); its data lines (`Planned <date>:`,
`Done (<n>):`, `YYYY-MM-DD: true`) are its own format, listed in the skill. A
job's final reply is one line on what happened. When `ntm:notify` returned
`NOTIFY VIA FINAL REPLY`, the final reply is instead the notification's title as
its first line and the message under it, nothing else. The weekly planning adds
fix-todo-list's result after the message, the morning reminder its `kept:` and
`couldn't move:` lines, and the price watch its per-item report.

## Creating tickets when the user asks

The user often files something just so they don't forget it; what it takes gets
figured out later, while grooming. Make what they asked for, plainly and in
their terms, and don't add meaning they didn't give it.

File it in an existing project that fits, or none. If nothing fits, you can ask
whether to make a project for it, as long as the shape makes sense: a specific
effort, or a catch-all bucket for a kind of thing.

## Deviations

Read Deviations in your settings last. Anything written there is how this user
does things, and it overrides the rules above: where it names a value, that
value wins; where it describes a rule, follow it as written. An empty section
changes nothing.
