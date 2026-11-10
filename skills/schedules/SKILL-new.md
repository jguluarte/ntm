---
name: schedules
description: >-
    Sets up and changes the user's ntm jobs, the scheduled tasks that remind
    them and plan their task list: which jobs run, on which days, at what time,
    under what title and on which model. Lists them, runs one now, turns one off
    or on, deletes one. Run with --setup from setup's handoff, or when the user
    asks about their jobs ("set up my reminders", "change the morning time",
    "turn off the evening reminder", "run the morning reminder now").
---

# ntm:schedules

A job is a scheduled task in the user's AI app whose prompt runs a few ntm
skills in order. The user decides which jobs they want, when each runs and what
it's called. The scheduled tasks are the only record of the jobs, so a change
edits the scheduled task itself.

## Setup

Load `ntm-user:backend` to read the user's conventions, then read Timezone under
About you in the Settings document: every job runs in it.

## Usage

```
/ntm:schedules [--setup "<schedules and model>"] [<what to change, in words>]
```

With `--setup`, create the jobs the user agreed in setup, as From setup's
handoff says. Otherwise, find their jobs among the scheduled tasks: the ones
whose prompt loads an `ntm:` skill. With none, set them up with the user. With
some, show them and ask what to change.

With words, go straight to that change under Changing the jobs.

## The jobs

ntm suggests these jobs. Offer the ones for the features the Built line in
`ntm-user:backend` names: `price-watch` for price watch, the rest for task
management.

| Job           | What it does                                        | Suggested        |
| ------------- | --------------------------------------------------- | ---------------- |
| `morning`     | Makes today ready, then sends what's on today       | Weekdays, 08:44  |
| `afternoon`   | What's still open today                             | Weekdays, 14:26  |
| `evening`     | How the day went                                    | Weekdays, 19:23  |
| `week`        | Plans the week ahead and looks back on the last one | Sunday, 21:50    |
| `price-watch` | Which watched items are a good deal                 | Every day, 06:57 |

A job never starts on :00 or :30: scheduled tasks everywhere start on those
marks, so a job off them doesn't run in the rush. Move such a time a few minutes
earlier, by a different number of minutes for each job.

After the ready check, a job runs the skills below in order, one step each that
loads the skill and runs it. A job can run any other ntm skill the user asks
for, the same way.

### morning

`/ntm:plan --auto day`, then `/ntm:reminder --type morning` with what plan
returned. The final reply adds plan's `couldn't move:` lines.

### afternoon

`/ntm:reminder --type afternoon`.

### evening

`/ntm:reminder --type evening`.

### week

`/ntm:fix-todo-list`; on `Fix-todo-list FAILED`, carry on. Then
`/ntm:plan --auto <range>`, the range being the days it plans, in words:
`week mon-fri` by default.

When the week message looks back on what got done, it then runs
`/ntm:show-completed <span> and what's still open`, the span being how far it
looks back, ending today: `the last 7 days`. On `Show-completed FAILED`, carry
on with `done: unavailable` and `open: unavailable`.

Last, `/ntm:reminder --type week` with what the steps before it returned,
show-completed's Still open tasks going as `open:`. The final reply adds
fix-todo-list's lines, what it cleared and what it couldn't write, and plan's
`couldn't move:` lines.

### price-watch

`/ntm:price-watch`.

## The prompt

Every job's prompt is this frame, filled in with its steps. It only loads
skills, so an update to ntm reaches every job without touching it.

```
<Title>.
Timezone: <Timezone>.
1. Load `ntm:ready-check` and run
   `/ntm:ready-check --notify-failure <job>`.
   On `Ready-check FAILED`, end the run with what it returned.
<the job's steps>
Final reply: what the last step returned, as the Results rules in
`ntm-user:backend` say.
```

`<job>` is the job's name in The jobs, such as `morning`, or a short name for a
job of the user's own.

### Planning and the weekly message

When the user plans differently from `ntm:plan`'s defaults, the morning and week
jobs say how in one line after the timezone line, such as
`Planning: two tasks a day, weekends too.` When the week job's message covers
something other than plan's default, it says what in a line such as
`Weekly message: the week ahead only.` With nothing different, neither line.

### A job's own Pushover app

On the `pushover` channel, a job can send from its own Pushover app. When the
user gives a job its app token, add this after the timezone line, and never
repeat the token back or show it:

```
Pushover app token for this job: <token>. Hand it to every
`ntm-user:notify` call as `--app-token`, and to the messenger agent
as `app token:`.
```

## Setting up the jobs

### 1. Propose a schedule

Show one short table, one row per job: job, days, time and title. Start from The
jobs, with a plain title for each, such as "Morning reminder".

Under the table, one line each:

- planning: weekdays, one task a day, about an hour or less (`ntm:plan`'s
  defaults)
- the week job: plans `week mon-fri`, looks back on `the last 7 days`, and its
  message covers what got done, what's still open and the week ahead

For example:

| Job       | Days     | Time  | Title            |
| --------- | -------- | ----- | ---------------- |
| `morning` | Weekdays | 08:44 | Morning reminder |
| `week`    | Sunday   | 21:50 | Week ahead       |

### 2. Agree on it

A simple affirmation approves it all. They keep, drop, add or change anything in
their own words, and the titles are theirs. Revise until they approve; create
nothing before that.

### 3. Choose the model

Ask once, for all the jobs: which model should they run on? A new job inherits
the model of the chat that creates it, and that can be the heaviest one. Suggest
a lighter model than the one running this chat, from the ones this app offers,
then use the one they choose; it's the model every job gets.

### 4. Create each job

Fill in its prompt from The prompt, with a `Planning:` or `Weekly message:` line
for whatever they changed from step 1's defaults. Then create the scheduled
task:

| Setting           | Value                                                               |
| ----------------- | ------------------------------------------------------------------- |
| `name`            | the title                                                           |
| `prompt`          | the filled-in prompt                                                |
| `cron_expression` | weekdays at 08:44 in Berlin is `CRON_TZ=Europe/Berlin 44 8 * * 1-5` |
| `notifications`   | `{push: true}`                                                      |
| `initiation`      | `human_request`                                                     |
| `permission_mode` | left unset                                                          |

Once it's created, update the job's `model` to the id this app gives the model
they chose.

The push carries the run's final reply: on the `claude-push` channel that's the
reminder itself, and on the `pushover` channel a second, shorter push. A job has
the connectors of the chat that creates it, and never a browser, so
`sync-price-watch-to-amazon` can't run as one.

### 5. Say how they run

Tell the user the model the jobs run on, whether their runs go ahead on their
own or stop at an action that needs approval (each job's permission mode says),
and on the `pushover` channel that the second push can be turned off in a job's
settings. Then offer to run one now: its ready check proves the job can reach
their task list.

## From setup's handoff

`--setup "<schedules and model>"` carries what the user agreed at the end of
setup: the jobs, their days and times, and the model. Don't ask again. Take it
as the approved schedule and the model they chose, give each job a plain title
unless the text names one, and go on from step 4.

## Changing the jobs

Show the jobs in one table: title, schedule in words in the user's timezone, on
or off, and the last run (succeeded or failed, and when). Tell the jobs apart by
their steps, never by title. Never show an app token. Then ask what to change.

### A time, the days or a title

Update the job, keeping what they didn't ask to change. Confirm the new schedule
in words, and say when a time moved.

### The prompt

The prompt is the user's: change it with them when they ask. Update the
scheduled task in place; deleting and recreating it loses its history. When
ntm's frame or a job's steps change, fill the prompt in again, keeping anything
the user added and its app token line.

### The model

Show the current one, then set the one they ask for.

### Off and on

A job that's off stays stored and never runs. Say "off" and "on", never
"paused": off is for stretches with no reminders at all. For a day or a range,
`/ntm:pause` is the lighter tool, since work they dated themselves still gets
its reminders.

### Deleting

Confirm first: deleting a job also removes the sessions it started. Turning it
off keeps its history.

### A new job

Set it up as Setting up the jobs says, for that job alone.

## Running a job now

Start a run of the job outside its schedule, with its own prompt and connectors.
That's how to check a job, and what "run the morning reminder now" means.

## Result

End with one line per job: title, schedule in words, on or off.
