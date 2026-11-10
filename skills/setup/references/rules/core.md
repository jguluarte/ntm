# Core rules

The rules every user's `ntm-user:backend` carries, whatever features they
picked. The build copies everything below this paragraph into it as written,
with `<List name>` and `<List id>` filled in, and `<Labels>` replaced by one
line per system label of the user's features: its default name and its real
name, from Labels in the Settings document.

The rules every ntm skill and agent follows to read and write the user's todo
list. They are a general guide, not a rulebook for every edge; the other skills
and the jobs put the todo list right as they run. A value these rules name under
a heading of the Settings document (see Databases) is read from that document
when it's needed; a missing heading or line means its default.

The todo list is one person's, not a team's: priority is mostly unused, and a
fixed deadline is rare. The words here come from tools built for companies; read
these rules without that weight.

## Vocabulary

### Task list

The place that holds every task: `<List name>`.

### Backend

The system behind the task list.

### Guide

How each operation is done on this backend: the calls `ntm-user:backend` gives
with these rules.

### Task

One thing on the todo list, shown the backend's own way. Its id is whatever the
backend gives it, such as `ABC-12`.

### Project

A collection of tasks. Projects can have labels which also apply to its tasks.

### Planned date

The task's one date field, the day the work is planned for. **A planned date
should NEVER be treated like a "deadline"**.

### Database

A document stored in the backend that ntm keeps persistent data in. The titles
are under Databases in these rules; ntm's `references/databases/` holds the
templates.

### Label

A tag on a task or project.

### Job

A scheduled run, what the Claude app calls a scheduled task. Never "trigger",
"routine" or "cron job" when talking to the user.

## Workspace

### Todo list

`<List name>`, with `<List id>` where the backend needs it.

### Task URLs

Use the task's own `url` field, one of the standard fields.

### Whose tasks

Every task on the list is the user's; don't filter by assignee unless asked.

## Chat, jobs and agents

A skill typed in chat runs in the chat. Skills hand work to the plugin's agents,
in a job or in chat alike; an agent can't start another agent. Each skill says
which agent it asks and what it hands over.

When the messenger returns `Messenger NEEDS: …`, supply what it names and ask
once more; a second one counts as `Messenger FAILED`.

## Talking to the user about tasks

The user doesn't know what a task means by number alone. When you mention a task
to them, refer to it the way a person would in conversation: a few natural words
for what it is, with the id in parentheses after it.

For example, take ABC-15, titled "Replace the kitchen tap". Telling the user
"you already finished ABC-15" means nothing to them, and quoting the full title
reads like a report, not a person talking. Instead, say "you already finished
the kitchen tap (ABC-15)". The example is only an illustration; there's no need
to look it up. Where the backend has no ids, use the words alone.

Lines another skill parses keep their format, but when you pass them on to the
user, word them this way too.

A linked task is `[<words> (<id>)](<url>)`: the words as this section says, the
id in parentheses inside the link text, the url the task's own `url` field.
`ntm-user:notify` converts it for its channel.

## Statuses and labels

Every status on the todo list falls into one of the classes below, read from the
backend as the guide says.

### Status classes

Nothing outside the plannable class is ever planned. An open task is any task
that isn't done, canceled or duplicate, so a blocked task is still open.

#### Plannable

Open work, usually a backlog, a to-do and an in-progress status. The in-progress
kind is **started**: work has begun.

#### Blocked

The user has put the task in the blocked status because they can't move it
forward right now. What's in the way is an open blocking task linked to it, a
reason described in its comments, or both. A blocked-by relation alone doesn't
make a task blocked. The class is empty when the todo list has no such status.

#### Done

Finished.

#### Canceled

Closed without being done.

#### Duplicate

Ignore it everywhere; the original task is what counts.

### System labels

A label written with a `$` in front is a system label, written by its default
name. Its real name on the todo list is the one below; use that, and never show
the `$` to the user. Any of them can sit on a task or on a project; on a
project, every task in it carries it too (see Project labels).

`<Labels>`

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

## Databases

The system keeps its own records in databases on the todo list, each under the
fixed title in parentheses below. Read and write them with the guide's
`read database` / `write database`. Each database has one writer; everything
else only reads it.

Where the backend has no documents, the guide keeps each database in an open
task titled with the database's title. That task is a database, not work; every
skill ignores it.

### Settings (`Settings`)

The values the user set up, under fixed headings, read by heading. Setup creates
it.

### Message history (`Message history`)

What reminders have said. `ntm:style` keeps it. Its frontmatter holds a `Keep:`
line saying how much history to keep; the user changes it there.

### Message rules (`Message rules`)

What each reminder's message says. Setup creates it from ntm's template; the
user changes it there.

## Fetching

The guide's `fetch open` returns every open task with the standard fields: id,
title, url, status, status class, priority, estimate, planned date, labels,
project, parent id, completed at, updated at. It also lists every project with
its name and labels, so inherited labels count (see Project labels), and its
summary when a skill asks for it.

### Every open task

For anything that needs the whole open todo list: `fetch open`, which includes
blocked tasks, with nothing dropped.

### Looking back

The guide's `fetch closed`.

## Dates

Today is the user's local date: the run knows the local time, a scheduled job's
prompt states the timezone, and Timezone, under About you in the Settings
document, is the fallback.

Compare planned dates as `YYYY-MM-DD` strings.

## Writing to the todo list

The backend's response says whether a write succeeded. If one fails, retry it
once. If it still fails, say so: tell the user in chat, or list it in the result
a skill returns.

## Results

Skills return text; jobs decide what reaches the user. No skill other than
`ntm-user:notify` sends anything.

Every skill a job calls returns plain text. A skill's status line (OK / FAILED)
starts with its own name, capitalised, hyphens kept (`Self-test FAILED: …`,
`Ready-check OK`); its data lines are its own format, listed in the skill.

Before sending, keep the message and title within the cap `ntm-user:notify`
gives for the user's channel.

A job's final reply is one line on what happened. On a channel where the job's
own push is the notification (as `ntm-user:notify` says), the final reply is
instead the notification: its title as the first line, the message under it,
then any lines the job adds, nothing else.

## Creating tasks when the user asks

The user often files something just so they don't forget it; what it takes gets
figured out later. Make what they asked for, plainly and in their terms, and
don't add meaning they didn't give it.

File it in an existing project that fits, or none. If nothing fits, you can ask
whether to make a project for it, as long as the shape makes sense: a specific
effort, or a catch-all bucket for a kind of thing.
