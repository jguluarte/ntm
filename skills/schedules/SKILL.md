---
name: schedules
description: >-
    Sets up and maintains the user's ntm jobs, the scheduled tasks that send
    their reminders: works out with them which skills run on which days, at what
    time, under what title, and builds the jobs from that. Creates and updates
    the jobs, lists them, runs one now, turns one off or on, deletes. Run from
    /ntm:configure, or when the user asks about their reminders' schedule ("set
    up my reminders", "change the morning time", "turn off the evening
    reminder").
---

# ntm:configure-schedule

The jobs are scheduled tasks. Call them "scheduled task" or "job" with the user,
never trigger, routine or cron job. This is a chat conversation: short rounds,
the user's answers win. It changes nothing in `ntm-user:settings` and writes no
file: the jobs it creates are the result.

## Tools

Use the scheduling tools this session has: they list, create, update, delete and
run scheduled tasks. If there are none, scheduled tasks aren't available from
here; say so and stop.

Load `ntm:conventions`: Timezone under About you in your settings is the
timezone every job runs in. On a first run from `ntm:configure`,
`ntm-user:settings` doesn't exist yet: use the timezone `configure` hands you,
and whether a price watch project was chosen.

## What a job can run

There are no fixed jobs. Each job runs one skill, or the bulk planning below,
and the user decides which they want, when, and what each is called. The times
here are only suggestions:

| Job                  | What it does                        | Suggested                         |
| -------------------- | ----------------------------------- | --------------------------------- |
| `morning-reminder`   | What's on the table today           | Weekdays, 09:00                   |
| `afternoon-reminder` | What's still open today             | Weekdays, 14:30                   |
| `evening-reminder`   | How the day went                    | Weekdays, 19:30                   |
| Bulk planning        | Plans a range of days at once       | Weekly, Sunday 22:00              |
| `show-completed`     | What got done over a span, sent     | Sunday 20:00, for the last 7 days |
| `price-watch`        | Which watched items are a good deal | Every day, 07:00                  |

Offer `price-watch` on every later run. On a first run, offer it only when
`configure` says a price watch project was chosen. It runs on paused days too.

## The prompt

Every prompt opens with the job's title and the user's timezone. A job that runs
one skill:

```
<title>.
Timezone: <Timezone under About you in your settings>.
Load `ntm:<skill>` and follow it from step 1. Its FINAL REPLY and
ERROR HANDLING are this job's.
If `ntm:<skill>` can't be loaded, end the run with this line:
`<title> FAILED: ntm:<skill> couldn't be loaded; check ntm is enabled.`
```

For `show-completed`, the sentence that loads the skill is instead:

```
Load `ntm:show-completed` and run
`/ntm:show-completed <span> --notify`. Its Notify section's final
reply and error handling are this job's.
```

The span is in words, as the user wants it: `the last 7 days` for a weekly one,
`last month` for a monthly one.

On the `pushover` channel, a job can send from its own Pushover app;
`ntm:configure-notifications` offers it. Don't ask here. When the user has given
a token for a job, never repeat it back, and add this after the timezone line:

```
Pushover app token for this job: <token>. Hand it to every
`ntm:notify` call as `--app-token`, and to the messenger agent as
`app token:`.
```

The prompt only loads skills, so a plugin update reaches the jobs without
touching them. Keep the last line: without it, a job whose plugin didn't load
ends without a word. The prompt is the user's: change it with them when they
ask.

### Bulk planning

Plans a range of days at once, after closing out the span just past. Its
defaults go under the schedule table (Walking the schedule, step 1), and the
user can change any of them:

- how often it runs: weekly by default;
- the range it plans, in words: `week mon-fri` by default, or `next two weeks`,
  `all weekdays this month`;
- the span it looks back on, as long, ending today: `the last 7 days` for one
  week;
- what the message covers: what got done, what's still open, the week ahead, by
  default.

The suggested prompt:

```
<title>.
Timezone: <Timezone under About you in your settings>.
1. Run `/ntm:ready-check --notify-failure plan`. On
   `Ready-check FAILED`, end the run with what it returned and
   nothing more.
2. Load `ntm:show-completed` and run
   `/ntm:show-completed <span> and what's still open`.
   On `Show-completed FAILED`, carry on with `done: unavailable`.
3. Load `ntm:fix-todo-list` and run `/ntm:fix-todo-list`. On
   `Fix-todo-list FAILED`, carry on.
4. Load `ntm:plan` and run `/ntm:plan --auto <range>`.
5. Ask the messenger agent, or follow `agents/messenger.md` from the
   installed plugin when it isn't available. Hand it these lines,
   plus `wording:` as the conventions' "Chat, jobs and agents" says:
       type: reminders.week
       job: plan
       weekly message: <what the message covers>
   then one `done:` line per Done task from step 2, or `done: none`;
   one `open:` line per Still open task, with `was` its date when
   that's before today, or `open: none`; each a task line as the
   messenger's "What you're given" says; and plan's `planned:` lines.
Final reply: when the messenger returned a delivery block, the title
and message under its marker line, verbatim; otherwise one short
line on what happened. Then fix-todo-list's lines and plan's
`couldn't move:` lines. For any error after step 1, including a
`… FAILED` line, never use `ntm:notify`: end the run with the error
stated plainly.
If a skill can't be loaded, end the run with this line:
`<title> FAILED: <skill> couldn't be loaded; check ntm is enabled.`
```

## Walking the schedule

1. Propose a schedule as one short table, one row per job: job, days, time,
   title. Start from What a job can run, with a plain title for each ("Morning
   reminder"), and each time set by the jitter rule: a job never starts on :00
   or :30, so move such a time a few minutes earlier, a different number for
   each job. Under the table, one line each:
    - planning, for bulk planning and `morning-reminder`: weekdays, one task a
      day, about an hour or less (`ntm:plan`'s defaults);
    - bulk planning: the defaults in The prompt's Bulk planning;
    - `show-completed`: weekly, for the last 7 days.
2. A plain "ok" takes it all. They keep, drop, add or change anything in their
   own words; the titles are theirs. Revise until they approve. Create nothing
   before that.
3. Write only what differs from `ntm:plan`'s defaults into the prompts of bulk
   planning and `morning-reminder`, as one line after the timezone line, such as
   `Planning: two tasks a day, weekends too.`; when nothing differs, add none.
4. Ask once, for all the jobs: which model should they run on? A new job
   inherits the model of the chat that creates it, and that can be the heaviest
   one. Suggest a lighter model, such as Opus or Sonnet, then use the one they
   choose; it's the model every job gets.

The table in step 1, for example:

| Job                | Days     | Time  | Title            |
| ------------------ | -------- | ----- | ---------------- |
| `morning-reminder` | Weekdays | 08:44 | Morning reminder |
| Bulk planning      | Sunday   | 21:50 | Week ahead       |

Then create each job, in the order below.

### Fill in its prompt

Fill in its prompt from The prompt. If they want the prompt to say something
else, change it with them; it's theirs.

### Create it

`create_trigger` with:

- `name`: the title.
- `prompt`: the prompt.
- `cron_expression`: the timezone from the prompt, then minute, hour, day of the
  month, month and days of the week, with the days as they chose (`1-5`
  weekdays, `0` Sunday, `*` every day); for a monthly job, `1 * *` as the last
  three fields.
- `notifications`: `{push: true}`. Push carries the run's completion summary,
  which is the reminder itself on the `claude-push` channel. On the `pushover`
  channel it's a second, shorter push.
- `initiation`: `human_request`.
- Leave `permission_mode` unset.

For example, the `cron_expression` for weekdays at 08:44:

```
CRON_TZ=Europe/Berlin 44 8 * * 1-5
```

### Set the model

`update_trigger` with the new job's id and `model: <the id>`. This is their
request from the walk, not the skill's. If the id is rejected, say so, leave the
job on the model it inherited, and carry on.

### Check its connectors

If the backend uses a connector and the result lists the job's connectors
(`mcp_connections`), check that the backend connector is among them. Keep any
job that lacks it for the sentence below.

### Once all are created

Tell the user in one sentence, for all the jobs: the model they run on; whether
runs go ahead on their own or stop when an action needs approval, and that
automatic approval can be turned on in a scheduled task's settings if the
organization allows it; on the `pushover` channel, that each run also sends a
second, shorter push its settings can turn off. The approval setting is
`derived_state.permission_mode` in each result: `auto` means runs go ahead on
their own; absent means a run stops when an action needs approval, and nobody is
there to approve a scheduled run.

Say more only for a job that lacks the backend connector: attach the connector
to this session and create the job again, or every run will fail its ready
check.

For every job, the proof is a run once `ntm-user` is installed: offer
`fire_trigger` (Running a job now) then, and read its ready check.

## Connectors

A job inherits the connectors attached to the session that creates it. A browser
is never attached to a job.

## When the schedule is already established

When jobs exist, list them and ask what to change, instead of walking the
schedule again. `list_triggers`, recurring only. Tell the user's jobs by the
skill their stored prompt loads (`derived_state.prompt`, when the
`list_triggers` entry carries it; when it doesn't, ask the user which job it
is), never by title: bulk planning is the one that runs `ntm:plan`. Show each
as: title, schedule in words in the user's timezone (from its `CRON_TZ` cron
expression), on or off, and the last run's status in a word (succeeded, failed)
and its time. Omit `trigger_id`s unless asked, and never show an app token. Then
ask what to change: a time, the days, a title, the prompt, the model, on or off,
delete, or a new job (walk that one as above).

## Running a job now

`fire_trigger` with `trigger_id` starts a run outside its schedule, with the
job's own prompt and connectors; that's the way to check a new job. To do a
job's work in chat instead, load its skill and follow it from step 1 ("run the
morning reminder now").

## Re-syncing a prompt

A stored prompt only goes stale when a prompt in The prompt changes. When that
happens: `list_triggers`, tell each job as When the schedule is already
established says, fill in the prompt again, and `update_trigger` with
`trigger_id` and the new `prompt`. Keep anything the user added to the prompt,
and its app token line (the stored prompt is `derived_state.prompt`, when the
entry carries it; when it doesn't, tell the user the new prompt replaces theirs
and to re-add anything they had put in); change only what came from The prompt.
Nothing else changes; the job keeps its schedule and run history. Never delete
and recreate a job to change its prompt.

## Changing a time, days or title

`update_trigger` with `trigger_id` and a new `cron_expression`, built as in
Walking the schedule, keeping whatever they didn't ask to change; or a new
`name`. Confirm the new schedule in words, and say when the jitter rule moved
the minute.

## Changing the model

`update_trigger` with `trigger_id` and `model`, only when the user asks for it
in their own words. Show the current one first when the `list_triggers` entry
carries it (`derived_state.model`).

## Turning a job off and on

`update_trigger` with `trigger_id` and `enabled: false` to turn a job off,
`enabled: true` to turn it on. A job that's off stays stored and never fires.
Say "off" and "on", never "paused": this is for stretches when the user wants no
reminders at all. For a day or a range, `/ntm:pause` is the lighter tool, since
work they dated themselves still gets its reminders.

## Deleting

Confirm with the user first; deleting also removes the sessions the job started.
Then `delete_trigger` with `trigger_id`. To stop a job without losing its
history, turn it off instead.

## Finishing

End with one line per job: title, schedule in words, on or off. Run from
`ntm:configure`, that list goes back to it; nothing here needs `ntm-user.plugin`
regenerated.
