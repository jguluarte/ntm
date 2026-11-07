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
`ntm-user:settings` doesn't exist yet: use the timezone, whether a price watch
project was chosen, and the Planning days `configure` hands you.

## The kinds

Every job's prompt is these three sentences, with the kind's default title and
skill filled in:

```
<default title>.
Load `<skill>` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING
are this job's.
If `<skill>` can't be loaded, end the run with this line:
`<default title> FAILED: <skill> couldn't be loaded; check ntm is enabled.`
```

For completed, the second sentence is instead:

```
Load `ntm:show-completed` and run `/ntm:show-completed <span> --notify`. Its
Notify section's final reply and error handling are this job's.
```

The span is `the last 7 days` for Completed this week and `last month` for
Completed this month. The prompt only loads the skill, so a plugin update
reaches the jobs without touching them, and a job carries no logic of its own.
Keep the last line: without it, a job whose plugin didn't load ends without a
word. Titles and prompt text are the user's: offer the defaults, take what they
say, and lock nothing.

### Morning reminder

Runs `ntm:morning-reminder`. Default title: Morning reminder. Default days and
time: planning days (Planning in your settings; weekdays by default), 09:00.
Always offered.

### Afternoon reminder

Runs `ntm:afternoon-reminder`. Default title: Afternoon reminder. Default days
and time: planning days, 14:30. Always offered.

### Evening reminder

Runs `ntm:evening-reminder`. Default title: Evening reminder. Default days and
time: planning days, 19:30. Always offered.

### Weekly planning

Runs `ntm:weekly-planning`. Default title: Weekly planning. Default days and
time: Sunday, 22:00. Always offered.

### Price watch

Runs `ntm:price-watch`. Default title: Price watch. Default days and time: every
day, 07:00, paused days included. Always offered, except on a first run when no
price watch project was chosen. It watches the tasks carrying the $price-watch
label.

### Completed

Runs `ntm:show-completed`. Default title: Completed this week / Completed this
month. Default days and time: weekly, Sunday 20:00, or monthly, the 1st 20:00;
off by default. Always offered; the default answer is no.

## Walking the kinds

For each kind in the order above, ask: do they want it; which days (Planning
days from Planning, weekdays by default, for the three daily reminders); what
time; what title. Ask once, for all the jobs: which model should they run on? A
new job inherits the model of the chat that creates it, and that can be the
heaviest one. Suggest a lighter model, such as Opus or Sonnet, then use the one
they choose; it's the model every job gets. A title is only a label; the kind's
default title stays the name notifications and tokens are matched by. Offer the
defaults and move on when they take them. For completed, also weekly or monthly,
and the span in the prompt follows. Skip price watch on a first run when no
price watch project was chosen.

Then, for each job they want:

1. Fill in its prompt from The kinds. If they want the prompt to say something
   else, change it with them; it's theirs.
2. Pick the time. The default is the starting point; the user can name another.
   Then apply the jitter rule: never land on :00 or :30. When a time would land
   on the hour or half hour, move it 1–29 minutes earlier (the number of letters
   in the title, spaces not counted, modulo 29, plus 1), and say so. Runs that
   start between 06:00 and 09:00 Pacific time can be delayed: convert the job's
   time to Pacific, and if it falls in that window, say so and keep it unless
   they'd rather move it.
3. `create_trigger` with:
    - `name`: the title.
    - `prompt`: the prompt.
    - `cron_expression`:
      `CRON_TZ=<timezone from About you in your settings> <minute> <hour> * * <days>`,
      days as they chose (`1-5` weekdays, `0` Sunday, `*` every day); for a
      monthly completed job, the same with `1 * *` as the last three fields.
    - `notifications`: `{push: true}`. Push carries the run's completion
      summary, which is the reminder itself on the `claude-push` channel. On the
      `pushover` channel it's a second, shorter push; say so, and that the
      scheduled task's settings can turn it off.
    - `initiation`: `human_request`.
    - Leave `permission_mode` unset.
4. Set the model they chose: `update_trigger` with the new job's id and
   `model: <the id>`. This is their request from the walk, not the skill's. If
   the id is rejected, say so, leave the job on the model it inherited, and
   carry on.
5. Tell the user, in one sentence, which model the job runs on and which
   approval setting it got, and that automatic approval can be turned on in the
   scheduled task's settings if the organization allows it. The setting is
   `derived_state.permission_mode` in the result: `auto` means runs go ahead on
   their own; absent means a run stops when an action needs approval, and nobody
   is there to approve a scheduled run.
6. When the result lists the job's connectors (`mcp_connections`), check that
   the backend connector named by Todo list is among them; if it isn't, say so:
   attach the connector to this session and create the job again, or every run
   will fail its ready check. Either way, the proof is a run, once `ntm-user` is
   installed: offer `fire_trigger` (Running a job now) then, and read its ready
   check.

## Connectors

A job inherits the connectors attached to the session that creates it. A browser
is never attached to a job.

## Already set up

When jobs exist, list them and ask what to change, instead of walking the kinds
again. `list_triggers`, recurring only. Match the user's jobs by title against
the titles above, and otherwise by the first line of the stored prompt
(`derived_state.prompt`, when the `list_triggers` entry carries it; when it
doesn't, ask the user which job it is): every prompt opens with the kind's
default title and a full stop (`Morning reminder.`, `Weekly planning.`,
`Completed this week.`, `Price watch.`). Show each as: title, schedule in words
in the user's timezone (from its `CRON_TZ` cron expression), on or off, and the
last run's status in a word (succeeded, failed) and its time. Omit `trigger_id`s
unless asked. Then ask what to change: a time, the days, a title, the prompt,
the model, on or off, delete, or a kind not yet created (walk that one as
above).

## Running a job now

`fire_trigger` with `trigger_id` starts a run outside its schedule, with the
job's own prompt and connectors; that's the way to check a new job. To do a
job's work in chat instead, load its skill and follow it from step 1 ("run the
morning reminder now").

## Re-syncing a prompt

A stored prompt only goes stale when the prompt in The kinds changes. When that
happens: `list_triggers`, match each job as Already set up says, fill in the
prompt again, and `update_trigger` with `trigger_id` and the new `prompt`. Keep
anything the user added to the prompt (the stored prompt is
`derived_state.prompt`, when the entry carries it; when it doesn't, tell the
user the new prompt replaces theirs and to re-add anything they had put in);
change only what came from The kinds. Nothing else changes; the job keeps its
schedule and run history. Never delete and recreate a job to change its prompt.

## Changing a time, days or title

`update_trigger` with `trigger_id` and a new `cron_expression`, built as in
Walking the kinds steps 2 and 3, keeping whatever they didn't ask to change; or
a new `name`. Confirm the new schedule in words, and say when the jitter rule
moved the minute.

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
