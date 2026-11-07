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

- **ntm** is the behaviour: the skills below, three agents (planner, messenger,
  shopper) that own the procedures, and the prompts for the jobs. It holds
  nothing of yours, so it installs from a marketplace or a zip and updates like
  any plugin.
- **ntm-user** is yours. `/ntm:configure` builds it with you, and it holds your
  unique settings and style: `ntm-user:settings` (every value you agreed to:
  where your todo list is, your label names, how planning and shopping work, how
  reminders reach you, anything you do differently) and `ntm-user:style` (how
  reminders talk to you). Keep it private; it can hold your Pushover keys.

The trigger word is the plugin's name, `ntm`; to use another, fork the template
and rename it with your agent (whole-word `ntm` to yours and `NTM` to yours in
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
   once on a throwaway task, then cancels the task and empties its note.

## Skills

### Every day

- `/ntm:today`: what's planned (open tasks planned for today or earlier, or any
  scope you describe).
- `/ntm:show-completed`: what got done over a span, and what's still open from
  it when you ask.
- `/ntm:plan`: plans the week or a day, with you in chat, or on its own for
  jobs.
- `/ntm:pause`: days when nothing gets planned automatically.
- `/ntm-user:style`: puts a message in your style.
- `/ntm:notify`: sends a notification through your channel.
- `/ntm:morning-reminder`, `/ntm:afternoon-reminder`, `/ntm:evening-reminder`,
  `/ntm:weekly-planning`: the three daily reminders and the weekly planning.
  Jobs run them; so can you ("run the morning reminder now").

### Planning and tidying

- `/ntm:review-todo-list`: reviews the todo list with you in chat (close, size,
  split).
- `/ntm:fix-todo-list`: closes parents whose sub-tasks are all closed and clears
  stale planned dates.

### Price watch

On when your settings name a price watch project.

- `/ntm:price-watch`: the daily price check on the tasks in that project.
- `/ntm:sync-price-watch-to-amazon`: keeps Amazon's own price alerts in step
  with the watched items. Needs a browser Claude can drive.

### Setup and settings

- `/ntm:configure`: the wizard. `/ntm:configure <part>` goes straight to one
  part.
- `/ntm:configure-todo-list`: where your list lives, how it's laid out, and the
  planning and shopping agreements.
- `/ntm:configure-notifications`: how reminders reach you.
- `/ntm:configure-style`: how reminders talk to you.
- `/ntm:configure-schedule`: the jobs (which, which days, what time, what
  title).
- `/ntm:settings`: shows your settings and changes them; produces a new
  `ntm-user.plugin`.
- `/ntm:ready-check`: can this session run a job?
- `/ntm:self-test`: the whole loop once, on a throwaway task.
- `/ntm:help`: answers questions from this README.
- `ntm:conventions`: the rules every skill loads first. Not run by hand.

## What's what

Rules live in `ntm:conventions` and name the values they depend on by key; the
values live in `ntm-user:settings`, agreed during setup. Jobs carry no logic:
each is three lines naming the skill it runs. The reminder skills gather facts
and hand them to an agent; agents own the procedures. In the skills, a name with
a `$` in front, like $no-autoschedule, is a label you configure, written by its
default name.

- **`ntm:conventions`**: the rules for reading and writing the todo list, in
  backend-neutral terms, with a guide per backend (Linear, or the one you
  describe). Ships with ntm.
- **`ntm-user:settings`**: every value you agreed to (About you, Todo list,
  Labels, Planning, Shopping, Notifications, Deviations). Written by
  `/ntm:configure` and `/ntm:settings`, with you.
- **`ntm-user:style`**: how reminders talk to you, and the message history.
  Written by `/ntm:configure-style`, with you.
- **Jobs**: the scheduled tasks (Morning, Afternoon and Evening reminders,
  Weekly planning, Completed weekly or monthly, Price watch). Each runs one
  skill. Written by `/ntm:configure-schedule`.
- **The planner**: what is planned, what got done, is today ready? Runs the list
  skills for the reminders. Ships with ntm.
- **The messenger**: what will you actually open? Composes in your style and
  sends through your channel. Ships with ntm.
- **The shopper**: is this item a good deal today? One per watched task. Ships
  with ntm.
- **Pauses note**: the days when nothing gets planned automatically. Written by
  `/ntm:pause`.
- **Message history note**: what reminders have said, so they don't repeat
  themselves. Written by `ntm-user:style`.
- **Task review log note**: how you like tasks written and sized, learned while
  reviewing. Written by `/ntm:review-todo-list`.
- **Price watch stores note**: stores you've vouched for or blocked in replies
  to a price alert; the shopper reads it. Written by `/ntm:price-watch`.
- **Amazon alert steps note**: how to set an alert on Amazon, learned once.
  Written by `/ntm:sync-price-watch-to-amazon`.

The notes live on your todo list, under the titles in your settings.

## What you can customize

- **The style.** Plain, a theme you describe, or a persona skill you already
  have: `/ntm:configure-style`.
- **The todo list agreements.** Labels and note titles, the planning rhythm and
  days, what the weekly message includes, how the shopper judges a deal.
  `/ntm:configure-todo-list` proposes a default for each and records your
  answer.
- **The schedule.** Which jobs run, which days, what time, what they're called:
  `/ntm:configure-schedule`.
- **Deviations.** Anything you do differently from the conventions, written in
  your settings and read last.

## Where your values live

All of them in `ntm-user`: `ntm-user:settings` (About you, Todo list, Labels,
Planning, Shopping, Notifications, Deviations) and `ntm-user:style`. ntm has no
settings file and no placeholders. Changing a value means a new
`ntm-user.plugin` from `/ntm:settings`, installed in place of the old one. What
the jobs write (the notes above) lives on your todo list.

## What the plugin sends where

- **Your todo list** (Linear, or your own): tasks, planned dates, labels and the
  notes above.
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

## The connector it bundles

Linear, declared in `.mcp.json`, so installing ntm lists it on the Connectors
tab for you to connect. On another backend, ignore it. See `CONNECTORS.md`.

## Requirements

- Scheduled tasks on your Claude account, for the reminders.
- For Pushover: an account, an application token and your user key.
- For Amazon alert sync: Claude's built-in browser, or your own browser with the
  Claude extension.
