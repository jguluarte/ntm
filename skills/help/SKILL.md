---
name: help
description: What ntm is and how to use it: the two plugins, first steps, the skills grouped by use, what can be customized, and where the user's values live. Shown when the user asks what ntm does, how to get started, or for help with ntm.
---

# ntm

ntm (Neurodivergent Task Manager) is a personal task system that runs on your own ticket board and a few scheduled tasks. It plans one task per weekday, reminds you about it in a style you choose, asks in the evening how the day went, plans every week, and can watch prices on things you want to buy.

It was built by one person for the places that got in their way: starting tasks, keeping multi-day work moving, and noticing when things have quietly gone stale. It stays low-process. If it starts bogging you down, turn pieces off.

## Two plugins

- **ntm** is the behaviour: the skills below, and three agents (planner, messenger, shopper) that carry out their steps. It holds none of your values, so it installs from a marketplace or a zip and updates like any plugin.
- **ntm-user** is yours. `/ntm:configure` generates it: `ntm-user:settings` (where your board is, your label names, how reminders reach you, anything you do differently) and `ntm-user:style` (how reminders talk to you). Keep it private; it can hold your Pushover keys.

## First steps

1. Install ntm. On the Connectors tab, connect Linear if that's your board (free for individuals, and the tested path; no Linear yet? `/ntm:configure` walks you through signing up); Claude Docs needs no connector.
2. Open a chat and run `/ntm:configure`. It asks about the trigger word, you, your board, notifications, style and schedule. It creates your scheduled tasks and hands you `ntm-user.plugin` to install.
3. Install it, open a new chat, and run `/ntm:self-test`. It runs the whole loop once on a throwaway ticket and removes it.

## Skills

Every day:

| Skill | What it does |
| --- | --- |
| `/ntm:todo-list` | What's planned: open tickets planned for today or earlier, or any scope you describe. |
| `/ntm:show-completed` | What got done over a span, and what's still open from it when you ask. |
| `/ntm:plan` | Plans the week or a day: with you in chat, or on its own for jobs. |
| `/ntm:pause` | Days when nothing gets planned automatically. |
| `/ntm:style-message` | Puts a message in your style. |
| `/ntm:notify` | Sends a notification through your channel. |
| `/ntm:morning-reminder`, `/ntm:afternoon-reminder`, `/ntm:evening-reminder` | The three daily reminders. Jobs run them; so can you ("run the morning reminder now"). |

Planning and tidying:

| Skill | What it does |
| --- | --- |
| `/ntm:review-todo-list` | Grooms the todo list with you in chat: close, size, split. |
| `/ntm:fix-todo-list` | Closes parents whose sub-tickets are all closed and clears stale planned dates. |

Price watch (on when your settings name a price watch project):

| Skill | What it does |
| --- | --- |
| `/ntm:run-price-watch` | The daily price check on the tickets in that project. |
| `/ntm:sync-price-watch-with-amazon` | Keeps Amazon's own price alerts in step with the watched items. Needs a browser on your computer. |

Setup and settings:

| Skill | What it does |
| --- | --- |
| `/ntm:configure` | The wizard. `/ntm:configure <part>` goes straight to one part. |
| `/ntm:configure-integration` | Which board, and how it's laid out. |
| `/ntm:configure-notifications` | How reminders reach you. |
| `/ntm:configure-communication-style` | How reminders talk to you. |
| `/ntm:configure-schedule` | The jobs: which, which days, what time, what title. |
| `/ntm:settings` | Shows your settings and changes them; produces a new `ntm-user.plugin`. |
| `/ntm:ready-check` | Can this session run a job? |
| `/ntm:self-test` | The whole loop once, on a throwaway ticket. |
| `/ntm:help` | This text. |
| `ntm:conventions` | The rules every skill loads first. Not run by hand. |

## What you can customize

- **The trigger word.** `ntm` in `/ntm:plan` can be any word: `/ntm:configure` asks first, and `/ntm:settings` does it any time.
- **The style.** Plain, a theme you describe, or a profile you already have: `/ntm:configure-communication-style`.
- **Labels and note titles.** The real names on your board, in `ntm-user:settings`.
- **The schedule.** Which jobs run, which days, what time, what they're called: `/ntm:configure-schedule`.
- **Deviations.** Anything you do differently from the conventions, written in your settings and read last.

## Where your values live

All of them in `ntm-user`: `ntm-user:settings` (About you, Board, Labels, Notifications, Deviations) and `ntm-user:style`. ntm has no settings file and no placeholders. Changing a value means a new `ntm-user.plugin` from `/ntm:settings`, installed in place of the old one. What the jobs write (pauses, the message history, the grooming log, price watch stores) lives in notes on your board.

## What the plugin sends where

- **Your board** (Linear, Claude Docs, or your own): tickets, planned dates, labels and the notes above.
- **Pushover**, when it's your channel: each reminder's title and message, with your app token and user key, over HTTPS from the run. With the claude-push channel nothing is sent; the scheduled task's own completion push carries the reminder.
- **The web**: searches of store sites for the items you're watching (price watch only), and, when `Template source:` names a URL, the template's own release for the trigger-word rename and the weekly upstream check.
- **Your browser**, for Amazon alert sync only: Claude in Chrome on your computer.

Nothing else leaves a run. No skill but `ntm:notify` sends anything.

## The connector it bundles

Linear, declared in `.mcp.json`, so installing ntm lists it on the Connectors tab for you to connect. On another backend, ignore it. See `CONNECTORS.md`.

## Requirements

- Scheduled tasks on your Claude account, for the reminders.
- For Pushover: an account, an application token and your user key.
- For Amazon alert sync: Claude in Chrome on your computer.
