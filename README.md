# Neurodivergent Task Manager (ntm)

ntm runs a personal task system on your own todo list, with a few scheduled
jobs that keep it moving. It plans your days and weeks, reminds you in a style
you choose, asks in the evening how the day went, tidies what has gone stale,
and watches prices on things you want to buy.

It was built by one person for the places that got in their way: starting
things, keeping multi-day work moving, noticing when things have quietly gone
stale, not forgetting things, and buying on a good price instead of on impulse.
It stays low-process. If it starts bogging you down, turn pieces off.

The price watch is there to bridge the impulse to buy. Sometimes we buy right
away only so we don't forget, and we don't always still want it later. Put the
item on the watch instead: it isn't forgotten, and waiting for a good price
becomes the easy option.

## Two plugins

- **neurodivergent-task-manager** is the behaviour: the skills below, three
  agents (planner, messenger, shopper) that own the procedures, and the prompts
  for the jobs. It holds nothing of yours, so it installs from a marketplace or
  a zip and updates like any plugin.
- **ntm** is yours. `/neurodivergent-task-manager:configure` builds it with you,
  and it holds your
  unique settings and style: `ntm:settings` (every value you agreed to:
  where your todo list is, your label names, how planning and shopping work, how
  reminders reach you, anything you do differently) and `ntm:style` (how
  reminders talk to you). Keep it private; it can hold your Pushover keys.

The trigger word is the plugin's name, `neurodivergent-task-manager`; to use
another, fork the template and rename it with your agent (whole-word
`neurodivergent-task-manager` to yours and `NTM` to yours in capitals, in every
file and in `plugin.json`'s `name`), then create your jobs from that copy.

## First steps

1. Install neurodivergent-task-manager. Connect whatever system holds your
   tasks, todos or reminders: Linear and Claude Docs are the two shipped guides
   (Linear from the Connectors tab; Claude Docs needs no connector), and your
   own backend is described during setup.
2. Open a chat and run `/neurodivergent-task-manager:configure`. It asks about
   you, your todo list,
   notifications, style and schedule, creates your scheduled tasks, and hands
   you `ntm.plugin` to install.
3. Install it, open a new chat, and run
   `/neurodivergent-task-manager:self-test`. It runs the whole loop
   once on a throwaway task, then cancels the task and empties its note.

## Skills

Every day:

| Skill | What it does |
| --- | --- |
| `/neurodivergent-task-manager:today` | What's planned: open tasks planned for today or earlier, or any scope you describe. |
| `/neurodivergent-task-manager:show-completed` | What got done over a span, and what's still open from it when you ask. |
| `/neurodivergent-task-manager:plan` | Plans the week or a day: with you in chat, or on its own for jobs. |
| `/neurodivergent-task-manager:pause` | Days when nothing gets planned automatically. |
| `/ntm:style` | Puts a message in your style. |
| `/neurodivergent-task-manager:notify` | Sends a notification through your channel. |
| `/neurodivergent-task-manager:morning-reminder`, `/neurodivergent-task-manager:afternoon-reminder`, `/neurodivergent-task-manager:evening-reminder`, `/neurodivergent-task-manager:weekly-planning` | The three daily reminders and the weekly planning. Jobs run them; so can you ("run the morning reminder now"). |

Planning and tidying:

| Skill | What it does |
| --- | --- |
| `/neurodivergent-task-manager:review-todo-list` | Reviews the todo list with you in chat: close, size, split. |
| `/neurodivergent-task-manager:fix-todo-list` | Closes parents whose sub-tasks are all closed and clears stale planned dates. |

Price watch (on when your settings name a price watch project):

| Skill | What it does |
| --- | --- |
| `/neurodivergent-task-manager:price-watch` | The daily price check on the tasks in that project. |
| `/neurodivergent-task-manager:sync-price-watch-to-amazon` | Keeps Amazon's own price alerts in step with the watched items. Needs a browser Claude can drive. |

Setup and settings:

| Skill | What it does |
| --- | --- |
| `/neurodivergent-task-manager:configure` | The wizard. `/neurodivergent-task-manager:configure <part>` goes straight to one part. |
| `/neurodivergent-task-manager:configure-todo-list` | Where your list lives, how it's laid out, and the planning and shopping agreements. |
| `/neurodivergent-task-manager:configure-notifications` | How reminders reach you. |
| `/neurodivergent-task-manager:configure-style` | How reminders talk to you. |
| `/neurodivergent-task-manager:configure-schedule` | The jobs: which, which days, what time, what title. |
| `/neurodivergent-task-manager:settings` | Shows your settings and changes them; produces a new `ntm.plugin`. |
| `/ntm:ready-check` | Can this session run a job? |
| `/neurodivergent-task-manager:self-test` | The whole loop once, on a throwaway task. |
| `/neurodivergent-task-manager:help` | Answers questions from this README. |
| `neurodivergent-task-manager:conventions` | The rules every skill loads first. Not run by hand. |

## What's what

Rules live in `neurodivergent-task-manager:conventions` and name the values they
depend on by key; the
values live in `ntm:settings`, agreed during setup. Jobs carry no logic:
each is three lines naming the skill it runs. The reminder skills gather facts
and hand them to an agent; agents own the procedures.

In the skills, a name with a `$` in front, like $no-autoschedule, is a label
you configure, written by its default name; the skills use its real name from
Labels in `ntm:settings`, and never show you the `$`.

| Noun | What it is | Who writes it |
| --- | --- | --- |
| `neurodivergent-task-manager:conventions` | The rules for reading and writing the todo list, in backend-neutral terms, with a guide per backend (Linear, Claude Docs, or the one you describe). | neurodivergent-task-manager |
| `ntm:settings` | Every value you agreed to: About you, Todo list, Labels, Planning, Shopping, Notifications, Deviations. | `/neurodivergent-task-manager:configure` and `/neurodivergent-task-manager:settings`, with you |
| `ntm:style` | How reminders talk to you, and the message history. | `/neurodivergent-task-manager:configure-style`, with you |
| Jobs | The scheduled tasks: Morning, Afternoon and Evening reminders, Weekly planning, Completed (weekly or monthly), Price watch. Each runs one skill. | `/neurodivergent-task-manager:configure-schedule` |
| The planner | What is planned, what got done, is today ready? Runs the list skills for the reminders. | neurodivergent-task-manager |
| The messenger | What will you actually open? Composes in your style and sends through your channel. | neurodivergent-task-manager |
| The shopper | Is this item a good deal today? One per watched task. | neurodivergent-task-manager |
| Pauses note | The days when nothing gets planned automatically. | `/neurodivergent-task-manager:pause` |
| Message history note | What reminders have said, so they don't repeat themselves. | `ntm:style` |
| Task review log note | How you like tasks written and sized, learned while reviewing. | `/neurodivergent-task-manager:review-todo-list` |
| Price watch stores note | Stores you've vouched for or blocked in replies to a price alert; the shopper reads it. | `/neurodivergent-task-manager:price-watch` |
| Amazon alert steps note | How to set an alert on Amazon, learned once. | `/neurodivergent-task-manager:sync-price-watch-to-amazon` |

The notes live on your todo list, under the titles in your settings.

## What you can customize

- **The style.** Plain, a theme you describe, or a persona skill you already
  have: `/neurodivergent-task-manager:configure-style`.
- **The todo list agreements.** Labels and note titles, the planning rhythm and
  days, what the weekly message includes, how the shopper judges a deal.
  `/neurodivergent-task-manager:configure-todo-list` proposes a default for each
  and records your
  answer.
- **The schedule.** Which jobs run, which days, what time, what they're called:
  `/neurodivergent-task-manager:configure-schedule`.
- **Deviations.** Anything you do differently from the conventions, written in
  your settings and read last.

## Where your values live

All of them in `ntm`: `ntm:settings` (About you, Todo list, Labels, Planning,
Shopping, Notifications, Deviations) and `ntm:style`.
neurodivergent-task-manager has no settings file and no placeholders. Changing a
value means a new `ntm.plugin` from `/neurodivergent-task-manager:settings`,
installed in place of the old one. What the jobs write (the notes above) lives
on your todo list.

## What the plugin sends where

- **Your todo list** (Linear, Claude Docs, or your own): tasks, planned dates,
  labels and the notes above.
- **Pushover**, when it's your channel: each reminder's title and message, with
  your app token and user key, over HTTPS from the run. With the claude-push
  channel nothing is sent; the scheduled task's own completion push carries the
  reminder.
- **The web**: searches of store sites for the items you're watching (price
  watch only).
- **Your browser**, for Amazon alert sync only: Claude's built-in browser, or
  your own through the Claude extension (Amazon interface under Shopping in your
  settings).

Nothing else leaves a run. No skill but `neurodivergent-task-manager:notify`
sends anything.

## The connector it bundles

Linear, declared in `.mcp.json`, so installing neurodivergent-task-manager
lists it on the Connectors tab for you to connect. On another backend, ignore
it. See `CONNECTORS.md`.

## Requirements

- Scheduled tasks on your Claude account, for the reminders.
- For Pushover: an account, an application token and your user key.
- For Amazon alert sync: Claude's built-in browser, or your own browser with the
  Claude extension.
