---
name: conventions
description: >-
    Rules for reading and writing the user's todo list, in backend-neutral
    terms, plus the guide that maps them onto Linear. Load before any list
    query, and before creating or editing a task for the user.
---

# ntm:conventions

Version: 0.3.2

Template source: none yet

The rules every ntm skill and agent follows to read and write the user's todo
list. Load them before any list query, and before creating or editing a task.
They are a general guide, not a rulebook for every edge; the other skills and
the jobs put the todo list right as they run. Every value these rules depend on
is one the user agreed to during setup and can change in `ntm-user:settings`:
the rules name the value, the settings hold it.

## Loading

1. Load `ntm-user:settings` by name and read it by heading: About you, Todo
   list, Labels, Planning, Shopping, Notifications, Deviations. "Your settings"
   in these rules means `ntm-user:settings`: "List name under Todo list in your
   settings" is that line of it. A missing section or line means its default. If
   `ntm-user:settings` won't load, say in one line "not configured; run
   `/ntm:configure`" and continue with the defaults below. A caller that holds
   values of its own, such as `ntm:configure-todo-list`, uses those.
2. Read the backend guide for the backend named in Todo list:
   `references/linear.md` for `linear`. For any other backend, the user
   described each operation under Todo list in their own words, and that
   description is the guide; `references/CONTRACT.md` lists the operations it
   covers. Skills name operations (`fetch open`, `set planned date`,
   `read note`); the guide says how each one is done.
3. Read Deviations last; see Deviations at the end.

## What this todo list is

The todo list is the user's personal task system: home projects, chores,
hobbies, errands, things to buy when the price is right, whatever they want to
keep moving or not forget. It's the backbone of a system built around the points
where things get stuck: starting tasks, keeping multi-day work moving, noticing
when things have quietly gone stale, and buying on a good price instead of on
impulse.

It is one person's system, not a team's. The words here come from tools built
for companies, but they carry none of that weight: there are no sprints or
stakeholders, priority is mostly unused, a hard due date is rare and the user
plans it by hand, and the evening reminder is a friend asking how the day went.
Read every rule below at that scale, and keep that scale when writing to the
user.

Skills built on this todo list do three things:

- **Plan.** They give each planning day one planned task, by setting that task's
  planned date to the day. The user can add more to a day themselves, and a day
  they have already dated counts as planned.
- **Remind.** Jobs push the user reminders about the day's tasks.
- **Keep the todo list honest.** They clear stale dates, and reviewing the list
  with the user sizes and splits oversized work.

Every rule below exists so that those skills, and any agent working on the todo
list, read it the same way. When a rule seems arbitrary, the purpose above is
the tie-breaker.

## Vocabulary

- **Todo list:** the place that holds every task (List name under Todo list in
  your settings): a Linear team, a Claude Doc, a Todoist project, whatever the
  user keeps tasks in.
- **Backend:** the system behind the todo list: Linear, or the user's own.
- **Guide:** how each operation is done on this backend: `references/linear.md`,
  or the user's own description under Todo list (see Loading).
- **Task:** one thing on the todo list. Each backend shows a task its own way: a
  [Linear issue](https://linear.app/docs/conceptual-model), a row in a Claude
  Doc's table, a reminder, a todo. Ids look like `<task prefix>-<number>` where
  the backend has a prefix.
- **Project:** a named group of tasks, whatever the backend calls it. Projects
  carry labels their tasks inherit.
- **Parent task:** a task with open sub-tasks.
- **Sub-task:** a task under a parent task, where the backend has that relation.
- **Planned date:** the task's one date field, the day the work is planned for.
- **Planner:** a skill or agent that picks tasks and sets their planned dates,
  such as `ntm:plan` and the planner agent.
- **Started:** the one plannable status (see Status classes) that means work has
  begun. Jobs give credit for it.
- **Pause:** a day or range when nothing gets planned automatically. Work the
  user dated themselves still gets its reminders. Kept in the pauses note.
- **Note:** a text the system keeps on the todo list, found by title (see
  Notes). A task titled with a note's title is a note, not work; every skill
  ignores it.
- **Label:** a tag on a task or project.
- **Estimate:** how big a task is; Estimating in the planner agent
  (`agents/planner.md`) says what it means.
- **Job:** a scheduled run, what the Claude app calls a scheduled task. Never
  "trigger", "routine" or "cron job" when talking to the user.

## Workspace

- **Todo list:** List name from Todo list in your settings, with List id where
  the backend needs it. Task ids use Task prefix.
- **Task URLs:** use the task's own `url` field, one of the standard fields.
- **Whose tasks:** Your tasks under Todo list in your settings says which tasks
  on the list are the user's; by default, every task, regardless of assignee.
  Consider only those, and filter no further unless explicitly asked.

## Chat, jobs and agents

A skill typed in chat runs in the chat. The reminder skills,
`show-completed --notify` and the price watch hand their work to the plugin's
agents (planner, messenger, shopper), in a job or in chat alike; reviewing and
setting up the todo list ask the planner about estimates. Each says what it
hands over.

When an agent isn't available in the session, read its file from the installed
plugin and do what it says yourself, with the same request:
`find ~/.claude/plugins -path '*ntm*' -path '*/agents/<name>.md'` (the plugin
may sit under a versioned folder; the two `-path` tests find it either way). The
agent's file is the only copy of its procedure, so it runs the same either way;
say nothing to the user about which way it ran.

## Talking to the user about tasks

The user doesn't know what a task means by number alone. When you mention a task
to them, refer to it the way a person would in conversation: a few natural words
for what it is, with the id in parentheses after it.

For example, take ABC-15, titled "Replace the kitchen tap". Telling the user
"you already finished ABC-15" means nothing to them, and quoting the full title
reads like a report, not a person talking. Instead, say "you already finished
the kitchen tap (ABC-15)". The example is only an illustration; there's no need
to look it up. Where the backend has no ids, use the words alone.

Lines another skill parses (like `/ntm:today`'s result lines) keep their format,
but when you pass them on to the user, word them this way too.

A linked task is `[<words> (<id>)](<url>)`: the words as this section says, the
id in parentheses inside the link text, the url the task's own `url` field.
`ntm:notify` converts for its channel: Pushover html=1 gets
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
- **blocked**: the user has put the task in the blocked status (its name is on
  the blocked line in Todo list in your settings) because they can't move it
  forward right now. What's in the way is an open blocking task linked to it, a
  reason described in its comments, or both. Waiting on an order usually gets
  the $pending-shipment label instead. A blocked-by relation alone doesn't make
  a task blocked; see Blocks and blocked by. The blocked line is blank when the
  todo list has no such status.
- **done**: finished.
- **canceled**: closed without being done.
- **duplicate**: ignore it everywhere; the original task is what counts.

Nothing outside the plannable class is ever planned. An open task is any task
that isn't done, canceled or duplicate, so a blocked task is still open.

### System labels

Each label below has a line in Labels in your settings that gives its real name
on the todo list; the names shown here are the defaults. A label written with a
`$` in front, like $no-autoschedule, is one the user configures, written by its
default name: use its real name from Labels, and never show the `$` to the user.

Task labels:

- **$no-autoschedule:** the user has opted this task out of automatic planning.
  Planners never pick it, but once the user dates it themselves, it's reminded
  about like any other dated task.
- **$pending-shipment:** something has been ordered for this task and hasn't
  arrived, so the user can't start it.
- **$has-amazon-alert:** an Amazon price alert is set for this task.
  `ntm:sync-price-watch-to-amazon` sets and clears it.
- **$amazon-unavailable:** the item isn't sold new on Amazon, so no alert is
  set.

Labels set on a project (its tasks inherit them; see Project labels):

- **$price-watch:** the project's tasks are purchases waiting for a good price.
  There is no $price-watch task label. Price watch is on when Todo list names a
  price watch project; the watched tasks are the open tasks carrying this label.
  There is no separate switch.
- **$no-autoschedule:** as the task label, for every task in the project.

Any other label is an ordinary category as far as these rules go. A skill or job
can still give a label its own meaning without any change here; the label's
description on the todo list says what it's for.

### Project labels

Projects carry labels too. Any label on a project, system label or ordinary
category, counts as a label on every task in that project and on their
sub-tasks. Wherever a rule checks a task's labels, it checks the ones inherited
from its project too. This holds for labels added later as well, with no change
to these rules. Where the backend can't put labels on groups, the guide says so
and the user puts the labels on tasks directly.

## Notes

Each note's title is set under Notes in Todo list in your settings; the default
titles are in parentheses below. Read and write notes with the guide's
`read note` / `write note`. Each note has one writer; everything else only reads
it.

- **pauses** (`Pauses`): the pause schedule, under `## Pauses`. `ntm:pause`
  keeps it.
- **message history** (`Message history`): what reminders have said.
  `ntm-user:style` keeps it. Its first line is a `Keep:` line saying how much
  history to keep; the style template says what it writes.
- **task review log** (`Task review log`): `ntm:review-todo-list` keeps it.
- **price watch stores** (`Price watch stores`): stored in the price watch
  project, not at list level. `ntm:price-watch` keeps it, from the user's vouch
  and block replies; the shopper reads it.
- **Amazon alert steps** (`Amazon alert steps`):
  `ntm:sync-price-watch-to-amazon` keeps it.

Where the backend has no documents, the guide keeps each note in the description
of an open task titled with the note's title and labeled $no-autoschedule; see
Notes in `references/CONTRACT.md`.

## Fetching

The guide's `fetch open` returns every open task with the standard fields: id,
title, url, status, status class, priority, estimate, planned date, labels,
project, parent id, completed at, updated at. It also lists every project with
its name and labels, so inherited labels count (see Project labels), and its
summary when a skill asks for it.

- **For planning and reminders:** `fetch open`, which includes blocked tasks so
  parents and ancestors are fully visible. A task is a parent when an open task
  in the results names it as parent id. Keep excluded tasks in the results;
  Never picks says who skips them. Before planning a candidate, `read task` on
  it and its parent chain to see blockers.
- **Every open task** (reviewing, and anything else that needs the whole open
  todo list): the same fetch, with nothing dropped.
- **Looking back:** the guide's `fetch closed`.

### Never picks

Never picks in Planning in your settings lists what planners never pick; the
default is: a task that, itself or through any ancestor (project, or parent,
parent's parent, and so on), has the $no-autoschedule label, the
$pending-shipment label or the blocked status.

Planners skip excluded tasks: they never pick or date them. Reminders don't: any
open task the user has dated gets reminded about, excluded or not.

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

Planners set, move and clear planned dates freely.

A date is **stale** when it's earlier than today (`planned date < TODAY`) and
the task is still open.

## Relationships

How each relation affects planning. Planning in your settings can say otherwise;
these are the defaults.

### Parent and sub-tasks

- **A task with no open sub-tasks** is an ordinary task.
- **A task with open sub-tasks is a parent.** Plan its open sub-tasks, never the
  parent.

### Blocks and blocked by

A task blocked by open linked tasks, directly or through its parent chain, can
be planned for any day after the planned days of all those blockers. Never the
same day, but not necessarily the next either: any later day works. A blocker's
planned day is its planned date. A blocker with no planned date, or a stale one,
has no planned day, and the tasks it blocks wait. A planner can date a blocker
and then the task it blocks in the same run.

For example, if task `two` is blocked by task `one`, then `two` can be planned
for Wednesday only if `one` is planned for Tuesday or earlier. If `one` has no
planned day, `two` can't be planned yet.

The user also uses blocked-by loosely, to push one thing behind another; that's
fine, and nothing to question them about.

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
`Done (<n>):`, `YYYY-MM-DD: true`) are its own format, listed in the skill.

A job's final reply is one line on what happened. When `ntm:notify` returned
`NOTIFY VIA FINAL REPLY`, the final reply is instead the notification's title as
its first line and the message under it, nothing else. The weekly planning adds
fix-todo-list's result after the message, the morning reminder its `kept:` and
`couldn't move:` lines, and the price watch its per-item report.

## Creating tasks when the user asks

The user often files something just so they don't forget it; what it takes gets
figured out later, while reviewing. Make what they asked for, plainly and in
their terms, and don't add meaning they didn't give it.

File it in an existing project that fits, or none. If nothing fits, you can ask
whether to make a project for it, as long as the shape makes sense: a specific
effort, or a catch-all bucket for a kind of thing.

## Deviations

Read Deviations in your settings last. Anything written there is how this user
does things, and it overrides the rules above: where it names a value, that
value wins; where it describes a rule, follow it as written. An empty section
changes nothing.
