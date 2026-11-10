# Neurodivergent Task Manager (ntm)

ntm runs a personal task system on your own todo list, with a few scheduled jobs
that keep it moving. It plans your days and weeks, reminds you in a style you
choose, asks in the evening how the day went, tidies what has gone stale, and
watches prices on things you want to buy.

It was built by one person for the places that got in their way: starting
things, keeping multi-day work moving, noticing when things have quietly gone
stale, not forgetting things, and buying on a good price instead of on impulse.
It stays low-process. If it starts bogging you down, turn pieces off.

The price watch is there to bridge the impulse to buy. Sometimes we buy right
away only so we don't forget, and we don't always still want it later. Put the
item on the watch instead: it isn't forgotten, and waiting for a good price
becomes the easy option.

## Two plugins

- **ntm** is the behaviour: the skills below, three agents (messenger, shopper,
  estimator) that own the procedures, and the prompts for the jobs. It holds
  nothing of yours, so it installs from a marketplace or a zip and updates like
  any plugin.
- **ntm-user** is yours. `/ntm:configure` builds it with you, and it holds your
  unique settings and style: `ntm-user:settings` (every value you agreed to:
  where your todo list is, your label names, how planning and shopping work, how
  reminders reach you, anything you do differently) and `ntm-user:style` (how
  reminders talk to you). Keep it private; it can hold your Pushover keys.

The trigger word is the plugin's name, `ntm`; to use another, fork ntm and
rename it with your agent (whole-word `ntm` to yours and `NTM` to yours in
capitals, in every file and in `plugin.json`'s `name`), then create your jobs
from that copy.

## First steps

1. Install ntm. Connect whatever system holds your tasks, todos or reminders:
   Linear is the shipped guide (connect it from the Connectors tab), and your
   own backend is described during setup.
2. Open a chat and run `/ntm:configure`. It asks about you, your todo list,
   notifications, style and schedule, creates your scheduled tasks, and hands
   you `ntm-user.plugin` to install.
3. Install it, open a new chat, and run `/ntm:self-test`. It runs the whole loop
   once on a throwaway task, then cancels the task and empties its test
   database.

## Skills

### Every day

#### `/ntm:today`

What's planned: open tasks planned for today or earlier, or any scope you
describe.

#### `/ntm:show-completed`

What got done over a span, and what's still open from it when you ask.

#### `/ntm:plan`

Plans the week or a day: with you in chat, or on its own for jobs.

#### `/ntm:pause`

Days when nothing gets planned automatically.

#### `/ntm-user:style`

Puts a message in your style.

#### `/ntm:notify`

Sends a notification through your channel.

#### `/ntm:morning-reminder`

The morning reminder: what's on the table today. A job runs it; so can you ("run
the morning reminder now").

#### `/ntm:afternoon-reminder`

The afternoon reminder: what's still open today. A job runs it; so can you.

#### `/ntm:evening-reminder`

The evening reminder: how the day went, what closed and what's still open. A job
runs it; so can you.

### Planning and tidying

- `/ntm:review-todo-list`: reviews the todo list with you in chat (close,
  estimate, break up).
- `/ntm:fix-todo-list`: clears stale planned dates.

### Price watch

On when a project carries the $price-watch label and the Price watch job is
scheduled.

- `/ntm:price-watch`: the daily price check on the tasks in that project.
- `/ntm:sync-price-watch-to-amazon`: keeps Amazon's own price alerts in step
  with the watched items. Needs a browser Claude can drive.

Each watched task names the exact item, with its model and variant. Its
description gives the target price and anything that differs from the defaults:
the condition (new), how it reaches you (ordered online and delivered), and what
counts as a deal (at or near the target, or well below the usual price). For
example: "Target 80. Refurbished is fine."

### Setup and settings

| Skill                          | What it does                                                                        |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| `/ntm:configure`               | The wizard. `/ntm:configure <part>` goes straight to one part.                      |
| `/ntm:configure-todo-list`     | Where your list lives, how it's laid out, and the planning and shopping agreements. |
| `/ntm:configure-notifications` | How reminders reach you.                                                            |
| `/ntm:configure-style`         | How reminders talk to you.                                                          |
| `/ntm:configure-schedule`      | The jobs: which, which days, what time, what title.                                 |
| `/ntm:settings`                | Shows your settings and changes them; produces a new `ntm-user.plugin`.             |
| `/ntm:ready-check`             | Can this session run a job?                                                         |
| `/ntm:self-test`               | The whole loop once, on a throwaway task.                                           |
| `/ntm:help`                    | Answers questions from this README.                                                 |
| `ntm:conventions`              | The rules every skill loads first. Not run by hand.                                 |

## What's what

Rules live in `ntm:conventions` and name the values they depend on by key; the
values live in `ntm-user:settings`, agreed during setup. Jobs carry little
logic: most just name the skill they run. The reminder skills gather facts and
hand them to an agent; agents own the procedures. In the skills, a name with a
`$` in front, like $no-autoschedule, is a label you configure, written by its
default name. ntm keeps its own records in databases on your todo list, each
under a fixed title (Paused dates, Message history and the others below). If you
rename one, say so under Deviations in your settings.

### `ntm:conventions`

The rules for reading and writing the todo list, in backend-neutral terms, with
a guide per backend (Linear, or the one you describe). Ships with ntm.

### `ntm-user:settings`

Every value you agreed to: About you, Todo list, Labels, Planning, Shopping,
Notifications, Deviations. Written by `/ntm:configure` and `/ntm:settings`, with
you.

### `ntm-user:style`

How reminders talk to you, and the message history. Written by
`/ntm:configure-style`, with you.

### Jobs

The scheduled tasks that run the skills on your schedule, under titles you
choose: the reminders, bulk planning (weekly, say), what you got done, the price
watch. Built with you by `/ntm:configure-schedule`.

### The messenger

What will you actually open? Composes in your style and sends through your
channel. Ships with ntm.

### The shopper

Is this item a good deal today? One per watched task. Ships with ntm.

### The estimator

How big is each task, on your own scale, and does it fit one sitting? Proposes
each task's estimate when `/ntm:review-todo-list` reviews the todo list with
you, guesses how long each task takes when tasks are planned, and explains the
ways to estimate when you want to know. Ships with ntm.

### Paused dates database

The days when nothing gets planned automatically. Written by `/ntm:pause`.

### Message history database

What reminders have said, so they don't repeat themselves. Written by
`ntm-user:style`.

### Task review log database

How you like tasks written and estimated, learned while reviewing. Written by
the estimator agent during reviews.

### Price watch stores database

Stores you've vouched for or blocked in replies to a price alert; the shopper
reads it. Written by `/ntm:price-watch`.

## What you can customize

- **The style.** Plain, a theme you describe, or a persona skill you already
  have: `/ntm:configure-style`.
- **The todo list agreements.** Labels, the labels planning skips, whether you
  want Amazon price alerts. `/ntm:configure-todo-list` proposes a default for
  each and records your answer.
- **The schedule.** Which jobs run, which days, what time, what they're called:
  `/ntm:configure-schedule`.
- **Deviations.** Anything you do differently from the conventions, written in
  your settings and read last.

## Where your values live

All of them in `ntm-user`: `ntm-user:settings` (About you, Todo list, Labels,
Planning, Shopping, Notifications, Deviations) and `ntm-user:style`. ntm has no
settings file and no placeholders. Changing a value means a new
`ntm-user.plugin` from `/ntm:settings`, installed in place of the old one. What
the jobs write (the databases above) lives on your todo list.

## What the plugin sends where

- **Your todo list** (Linear, or your own): tasks, planned dates, labels and the
  databases above.
- **Pushover**, when it's your channel: each reminder's title and message, with
  your app token and user key, over HTTPS from the run. With the claude-push
  channel nothing is sent; the scheduled task's own completion push carries the
  reminder.
- **The web**: searches of store sites for the items you're watching (price
  watch only).
- **Your browser**, for Amazon alert sync only: Claude's built-in browser, or
  your own through the Claude extension (Amazon interface under Shopping in your
  settings).

Nothing else leaves a run. No skill but `ntm:notify` sends anything.

## Connectors

ntm bundles none. For Linear, add it on the Connectors tab in Claude's settings;
setup walks you through it. See `CONNECTORS.md`.

## Requirements

- Scheduled tasks on your Claude account, for the reminders.
- For Pushover: an account, an application token and your user key.
- For Amazon alert sync: Claude's built-in browser, or your own browser with the
  Claude extension.
