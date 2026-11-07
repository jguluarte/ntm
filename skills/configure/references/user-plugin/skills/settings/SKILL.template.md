---
name: settings
description: Your settings for ntm. Read by neurodivergent-task-manager:conventions; change them with /neurodivergent-task-manager:settings.
---

Values for ntm, read by `neurodivergent-task-manager:conventions`. Shown only
when a person invokes this
skill directly.

Each section is read by heading. Every line is something you agreed to during
setup; a line that is missing means its default. Prose is fine: say what you do
in your own words.

## About you

- Name: <!-- how a message title addresses you -->
- Timezone: <!-- IANA zone, e.g. America/Chicago. Every date in the system is
  computed in it -->
- Country and currency: <!-- for price watch, e.g. US, USD -->

## Todo list

- Backend: <!-- linear | claude-docs | describe your own below -->
- List name: <!-- the team, doc, project or workspace that holds every task,
  as the backend names it -->
- List id: <!-- if the backend needs one for lookups; blank otherwise -->
- Task prefix: <!-- e.g. HOME for HOME-12; blank where ids carry none -->
- Statuses — the list's real names for each class:
  - plannable: <!-- usually three: a backlog, a to-do and an in-progress status -->
  - started: <!-- which of the plannable statuses means work has begun -->
  - blocked: <!-- open, but you can't move it right now; blank if the todo list
    has none -->
  - done:
  - canceled:
  - duplicate:
- Price watch project: <!-- the project whose tasks are purchases waiting for
  a good price; blank = price watch off -->
- Notes — the title of each note the system keeps:
  - pauses: Pauses
  - message history: Message history
  - grooming log: Grooming log
  - price watch stores: Price watch stores
  - Amazon alert steps: Amazon alert steps

<!-- If your backend isn't linear or claude-docs, describe here how to do each
operation neurodivergent-task-manager:conventions' contract lists, in your
words.
/neurodivergent-task-manager:configure-todo-list walks through them with you. -->

## Labels

The real name on your todo list for each label the system uses.

- Task labels:
  - no-autoschedule: no-autoschedule
  - pending-shipment: pending-shipment
  - has-amazon-alert: has-amazon-alert
  - amazon-unavailable: amazon-unavailable
- Project labels (tasks inherit them):
  - price-watch: price-watch
  - no-autoschedule: no-autoschedule

## Planning

How the planner works your todo list. Read by
`neurodivergent-task-manager:plan`, the planner agent and
the weekly planning.

- Rhythm: one task per weekday <!-- or: one per day; two per weekday; whatever
  you keep up with -->
- Planning days: weekdays <!-- the days that get a task automatically -->
- Plans ahead: one week <!-- how far the weekly planning plans: one week (Monday
  to Friday); two weeks; the month -->
- Sizing: Fibonacci points; 1 finishes in a night, 2 is iffy for one evening, 3
  or more is multi-day <!-- what an estimate means on your todo list; the
  planner guesses from the title when a task has none -->
- A day's worth: about an hour <!-- what the planner aims for when it picks -->
- Never picks: no-autoschedule, pending-shipment, blocked status <!-- the
  exclusions, each checked on the task and its ancestors -->
- Parents: plan the open sub-tasks, never the parent
- Weekly message: what got done, what's still open, the week ahead <!-- the
  halves the weekly planning message carries -->

<!-- Anything else about how you want planning done, as you'd say it: "nothing
heavy on Fridays", "garage work only on weekends". -->

## Shopping

How the price watch judges a deal. Read by
`neurodivergent-task-manager:price-watch` and the shopper
agent; Amazon interface by
`neurodivergent-task-manager:sync-price-watch-to-amazon`.

- Condition: new <!-- unless a task says otherwise -->
- Delivery: online only, to your country
- A deal: at or near the task's target, or well below the usual price
  <!-- what gets you an alert -->
- Amazon interface: <!-- how
  /neurodivergent-task-manager:sync-price-watch-to-amazon reaches Amazon:
  Claude's built-in browser, your own browser through the Claude extension, or
  off; blank means it asks -->

<!-- Anything else about how you shop: stores you always or never use are kept
in the price watch stores note; say here what counts beyond that. -->

## Notifications

- Channel: <!-- pushover | claude-push -->
- Pushover app token: <!-- only with pushover -->
- Pushover user key: <!-- only with pushover -->

<!-- Anything about how you want to be notified, as you'd say it: quiet hours,
priorities. A different app token for one reminder goes on its own line:
`Pushover app token for Morning reminder: …`. neurodivergent-task-manager:notify
follows what's written
here. -->

## Deviations

<!-- Anything you do differently from ntm's conventions.
neurodivergent-task-manager:conventions reads
this last and lets it override. -->
