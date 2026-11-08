---
name: configure-schedule
description: >-
    Sets up and maintains the user's ntm jobs, the scheduled tasks that send
    their reminders: which kinds they want, on which days, at what time, under
    what title. Creates and updates the jobs, lists them, runs one now, turns
    one off or on, deletes. Run from /ntm:configure, or when the user asks about
    their reminders' schedule ("set up my reminders", "change the morning time",
    "turn off the evening reminder").
---

# ntm:configure-schedule

The jobs are scheduled tasks. With the user, call them "scheduled task" or
"job", never trigger, routine or cron job. Work in short chat rounds; the user's
answers win. This skill writes no file and changes nothing in
`ntm-user:settings`: the jobs are the result.

## Before you start

Use this session's scheduling tools to list, create, update, delete and run
scheduled tasks. If it has none, say scheduled tasks aren't available here and
stop.

Load `ntm:conventions`. Every job runs in Timezone, under About you in your
settings. On a first run from `ntm:configure`, `ntm-user:settings` doesn't exist
yet: use the timezone, the Planning days, and whether a price watch project was
chosen, as `configure` hands them to you.

## The kinds

| Kind               | Skill                    | Default days and time                            |
| ------------------ | ------------------------ | ------------------------------------------------ |
| Morning reminder   | `ntm:morning-reminder`   | Planning days, 09:00                             |
| Afternoon reminder | `ntm:afternoon-reminder` | Planning days, 14:30                             |
| Evening reminder   | `ntm:evening-reminder`   | Planning days, 19:30                             |
| Weekly planning    | `ntm:weekly-planning`    | Sunday, 22:00                                    |
| Price watch        | `ntm:price-watch`        | Every day, 07:00, paused days too                |
| Completed          | `ntm:show-completed`     | Weekly, Sunday 20:00; or monthly, the 1st, 20:00 |

- Planning days come from Planning in your settings; weekdays by default.
- A kind's default title is its name. Completed's is Completed this week
  (weekly) or Completed this month (monthly).
- Offer every kind. Completed is off unless they ask for it.
- Price watch watches the tasks carrying the $price-watch label. On a first run
  with no price watch project chosen, skip it.

### The job prompt

Every job's prompt is this, with the kind's default title and skill filled in:

```
<default title>.
Load `<skill>` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING
are this job's.
If `<skill>` can't be loaded, end the run with this line:
`<default title> FAILED: <skill> couldn't be loaded; check ntm is enabled.`
```

For Completed, the middle sentence is instead this, where `<span>` is
`the last 7 days` (weekly) or `last month` (monthly):

```
Load `ntm:show-completed` and run `/ntm:show-completed <span> --notify`. Its
Notify section's final reply and error handling are this job's.
```

The prompt only loads the skill, so a plugin update reaches the jobs without
touching them. Keep the last line: without it, a job whose plugin didn't load
ends without a word. Titles and prompt text are the user's: offer the defaults,
take what they say, and lock nothing.

## Walking the kinds

Go through the kinds in order. For each, ask whether they want it, which days,
what time and what title; for Completed, also weekly or monthly, which sets its
title, span and cron form. Offer the defaults and move on when they take them. A
title is only a label: notifications and tokens still match on the kind's
default title.

Ask once, for all the jobs, which model they run on. A new job inherits the
model of the chat that creates it, which can be the heaviest one. Suggest a
lighter one, such as Opus or Sonnet, and use their choice for every job.

## Creating a job

For each job they want, fill in The job prompt, changing it with them if they
want it to say something else. Then take these steps.

### 1. Pick the time

Start from the default, or the time they name. Never land on :00 or :30: move
such a time 1 to 29 minutes earlier, rolling back the hour if needed (the
letters in the job's title, spaces not counted, modulo 29, plus 1), and say so.

Runs that start between 06:00 and 09:00 Pacific time can be delayed. If the
job's time, converted to Pacific, falls in that window, say so and keep it
unless they'd rather move it.

### 2. Create it

`create_trigger` with:

- `name`: the title.
- `prompt`: the prompt.
- `cron_expression`: one of the forms below.
- `notifications`: `{push: true}`. See the note below.
- `initiation`: `human_request`.
- Leave `permission_mode` unset.

The cron forms, with the days as they chose (`1-5` weekdays, `0` Sunday, `*`
every day):

```
# any days
CRON_TZ=<timezone> <minute> <hour> * * <days>
# monthly Completed, the 1st
CRON_TZ=<timezone> <minute> <hour> 1 * *
```

Note: push carries the run's completion summary. On the `claude-push` channel
that's the reminder itself. On `pushover` it's a second, shorter push: tell the
user, and that the scheduled task's settings can turn it off.

### 3. Set the model

`update_trigger` with the `trigger_id` from the create result and
`model: <model id>`. The user chose it in the walk; it isn't this skill's
choice. If the model id is rejected, say so, leave the job on the model it
inherited, and carry on.

### 4. Report the model and approval

In one sentence, tell the user which model the job runs on, which approval
setting it got, and that automatic approval can be turned on in the scheduled
task's settings if their organization allows it. The setting is
`derived_state.permission_mode` in the result: `auto` means runs go ahead on
their own; absent means a run stops at any action that needs approval, and
nobody is there to approve a scheduled run.

### 5. Check the connectors

A job inherits the connectors attached to the session that creates it; a browser
is never attached. When the result lists them (`mcp_connections`), check that
the backend connector named by Todo list is there. If it isn't, tell the user to
attach it to this session and create the job again, or every run will fail its
ready check.

Either way, only a run proves it. Once `ntm-user` is installed, offer to run the
job now and read its ready check.

## Already set up

When jobs exist, list them instead of walking the kinds again: `list_triggers`,
recurring only. Match each job to a kind by its title, or else by the first line
of its stored prompt, which is the kind's default title and a full stop
(`Morning reminder.`, `Completed this week.`). The stored prompt is
`derived_state.prompt` when the entry carries it; when it doesn't, ask the user
which job it is.

Show each job as: title, schedule in words in the user's timezone (from its
`CRON_TZ`), on or off, and the last run's status in a word (succeeded, failed)
and time. Leave out `trigger_id`s unless asked.

Then ask what to change: a time, the days, a title, the prompt, the model, on or
off, delete, or a kind not yet created (walk that one as above).

## Running a job now

`fire_trigger` with `trigger_id` starts a run outside the schedule, with the
job's own prompt and connectors; use it to check a new job. To do a job's work
in chat instead ("run the morning reminder now"), load its skill and follow it
from step 1.

## Re-syncing a prompt

A stored prompt goes stale only when The job prompt changes. Then, for each job:
match it as Already set up says, fill in the prompt again, and `update_trigger`
with `trigger_id` and the new `prompt`. Change only what came from The job
prompt and keep what the user added. If the entry doesn't carry
`derived_state.prompt`, tell the user the new prompt replaces theirs and to
re-add anything they'd put in. The job keeps its schedule and run history. Never
delete and recreate a job to change its prompt.

## Changing a time, days or title

`update_trigger` with `trigger_id` and a new `name`, or a new `cron_expression`
built as in Creating a job, steps 1 and 2, keeping what they didn't ask to
change. Confirm the new schedule in words, and say if Pick the time moved it.

## Changing the model

Only when the user asks for it in their own words: `update_trigger` with
`trigger_id` and `model`. First show the current one when the entry carries it
(`derived_state.model`).

## Turning a job off and on

`update_trigger` with `trigger_id` and `enabled: false` (off) or `enabled: true`
(on). A job that's off stays stored and never fires. Say "off" and "on", never
"paused": this is for stretches with no reminders at all. For a day or a range,
`/ntm:pause` is lighter, since work they dated themselves still gets its
reminders.

## Deleting

Confirm first: deleting also removes the sessions the job started. Then
`delete_trigger` with `trigger_id`. To stop a job and keep its history, turn it
off instead.

## Finishing

End with one line per job: title, schedule in words, on or off. When run from
`ntm:configure`, that list goes back to it. Nothing here needs `ntm-user.plugin`
regenerated.
