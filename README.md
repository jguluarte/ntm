# Neurodivergent Task Manager (ntm)

ntm runs a personal task system on your own board, with a few scheduled tasks that keep it moving. It plans your days and weeks, reminds you in a style you choose, asks in the evening how the day went, tidies what has gone stale, and watches prices on things you want to buy.

It was built by one person for the places that got in their way: starting things, keeping multi-day work moving, noticing when things have quietly gone stale, not forgetting things, and buying on a good price instead of on impulse. It stays low-process. If it starts bogging you down, turn pieces off.

The price watch is there to bridge the impulse to buy. Sometimes we buy right away only so we don't forget, and we don't always still want it later. Put the item on the watch instead: it isn't forgotten, and waiting for a good price becomes the easy option.

## Two plugins

- **ntm** is the behaviour: the skills below, three agents (planner, messenger, shopper) that own the procedures, and the prompts for the scheduled tasks. It holds nothing of yours, so it installs from a marketplace or a zip and updates like any plugin.
- **ntm-user** is yours. You build it with your own agent during `/ntm:configure`, and it holds your unique settings and style: `ntm-user:settings` (every value you agreed to: where your board is, your label names, how planning and shopping work, how reminders reach you, anything you do differently) and `ntm-user:style` (how reminders talk to you). Keep it private; it can hold your Pushover keys.

The trigger word is the plugin's name, `ntm`; to use another, fork the template and rename it with your agent (whole-word `ntm` to yours and `NTM` to yours in capitals, in every file and in `plugin.json`'s `name`), then create your jobs from that copy.

## First steps

1. Install ntm. Connect whatever system holds your tickets, todos or reminders: Linear and Claude Docs are the two shipped guides (Linear from the Connectors tab; Claude Docs needs no connector), and your own backend is described during setup.
2. Open a chat and run `/ntm:configure`. It asks about you, your board, notifications, style and schedule, creates your scheduled tasks, and hands you `ntm-user.plugin` to install.
3. Install it, open a new chat, and run `/ntm:self-test`. It runs the whole loop once on a throwaway ticket and removes it.

## Skills

Every day:

| Skill | What it does |
| --- | --- |
| `/ntm:todo-list` | What's planned: open tickets planned for today or earlier, or any scope you describe. |
| `/ntm:completed` | What got done over a span, and what's still open from it when you ask. |
| `/ntm:plan` | Plans the week or a day: with you in chat, or on its own for jobs. |
| `/ntm:pause` | Days when nothing gets planned automatically. |
| `/ntm-user:style` | Puts a message in your style. |
| `/ntm:notify` | Sends a notification through your channel. |
| `/ntm:morning-reminder`, `/ntm:afternoon-reminder`, `/ntm:evening-reminder`, `/ntm:weekly-planning` | The three daily reminders and the weekly planning. Jobs run them; so can you ("run the morning reminder now"). |

Planning and tidying:

| Skill | What it does |
| --- | --- |
| `/ntm:review-todo-list` | Grooms the todo list with you in chat: close, size, split. |
| `/ntm:fix-todo-list` | Closes parents whose sub-tickets are all closed and clears stale planned dates. |

Price watch (on when your settings name a price watch project):

| Skill | What it does |
| --- | --- |
| `/ntm:price-watch` | The daily price check on the tickets in that project. |
| `/ntm:amazon-alerts` | Keeps Amazon's own price alerts in step with the watched items. Needs a browser on your computer. |

Setup and settings:

| Skill | What it does |
| --- | --- |
| `/ntm:configure` | The wizard. `/ntm:configure <part>` goes straight to one part. |
| `/ntm:configure-board` | Which board, how it's laid out, and the planning and shopping agreements. |
| `/ntm:configure-notifications` | How reminders reach you. |
| `/ntm:configure-style` | How reminders talk to you. |
| `/ntm:configure-schedule` | The jobs: which, which days, what time, what title. |
| `/ntm:settings` | Shows your settings and changes them; produces a new `ntm-user.plugin`. |
| `/ntm:ready-check` | Can this session run a job? |
| `/ntm:self-test` | The whole loop once, on a throwaway ticket. |
| `/ntm:help` | Answers questions from this README. |
| `ntm:conventions` | The rules every skill loads first. Not run by hand. |

## What's what

Rules live in `ntm:conventions` and name the values they depend on by key; the values live in `ntm-user:settings`, agreed during setup. Jobs carry no logic: each is three lines naming the skill it runs. The reminder skills gather facts and hand them to an agent; agents own the procedures.

| Noun | What it is | Who writes it |
| --- | --- | --- |
| `ntm:conventions` | The rules for reading and writing the board, in backend-neutral terms, with a guide per backend (Linear, Claude Docs, or the one you describe). | ntm |
| `ntm-user:settings` | Every value you agreed to: About you, Board, Labels, Planning, Shopping, Notifications, Deviations. | `/ntm:configure` and `/ntm:settings`, with you |
| `ntm-user:style` | How reminders talk to you, and the message history. | `/ntm:configure-style`, with you |
| Jobs | The scheduled tasks: Morning, Afternoon and Evening reminders, Weekly planning, Completed (weekly or monthly), Price watch. Each runs one skill. | `/ntm:configure-schedule` |
| The planner | What is planned, what got done, is today ready? Runs the board skills for the reminders. | ntm |
| The messenger | What will you actually open? Composes in your style and sends through your channel. | ntm |
| The shopper | Is this item a good deal today? One per watched ticket. | ntm |
| Pauses note | The days when nothing gets planned automatically. | `/ntm:pause` |
| Message history note | What reminders have said, so they don't repeat themselves. | `ntm-user:style` |
| Grooming log note | How you like tickets written and sized, learned while grooming. | `/ntm:review-todo-list` |
| Price watch stores note | Stores the shopper has vouched for, or blocked. | `/ntm:price-watch` |
| Amazon alert steps note | How to set an alert on Amazon, learned once. | `/ntm:amazon-alerts` |

The notes live on your board, under the titles in your settings.

## What you can customize

- **The style.** Plain, a theme you describe, or a profile you already have: `/ntm:configure-style`.
- **The board agreements.** Labels and note titles, the planning rhythm and days, what the weekly message includes, how the shopper judges a deal. `/ntm:configure-board` proposes a default for each and records your answer.
- **The schedule.** Which jobs run, which days, what time, what they're called: `/ntm:configure-schedule`.
- **Deviations.** Anything you do differently from the conventions, written in your settings and read last.

## Where your values live

All of them in `ntm-user`: `ntm-user:settings` (About you, Board, Labels, Planning, Shopping, Notifications, Deviations) and `ntm-user:style`. ntm has no settings file and no placeholders. Changing a value means a new `ntm-user.plugin` from `/ntm:settings`, installed in place of the old one. What the jobs write (the notes above) lives on your board.

## What the plugin sends where

- **Your board** (Linear, Claude Docs, or your own): tickets, planned dates, labels and the notes above.
- **Pushover**, when it's your channel: each reminder's title and message, with your app token and user key, over HTTPS from the run. With the claude-push channel nothing is sent; the scheduled task's own completion push carries the reminder.
- **The web**: searches of store sites for the items you're watching (price watch only), and, when `Template source:` in `ntm:conventions` names a URL, the template's own release for the weekly upstream check.
- **Your browser**, for Amazon alert sync only: Claude in Chrome on your computer.

Nothing else leaves a run. No skill but `ntm:notify` sends anything.

## The connector it bundles

Linear, declared in `.mcp.json`, so installing ntm lists it on the Connectors tab for you to connect. On another backend, ignore it. See `CONNECTORS.md`.

## Requirements

- Scheduled tasks on your Claude account, for the reminders.
- For Pushover: an account, an application token and your user key.
- For Amazon alert sync: Claude in Chrome on your computer.
