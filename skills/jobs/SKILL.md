---
name: jobs
description: Creates and maintains the user's scheduled tasks (jobs) from the plugin's job templates: list them, create one, run one now, re-sync a prompt after a template change, change its time, turn it off or on, delete. Used by nudge:setup and when the user asks about their nudge jobs.
---

# nudge:jobs

The jobs are scheduled tasks. Call them "scheduled task" or "job" with the user, never trigger, routine or cron job.

## Tools

Load the scheduling tools with ToolSearch: `select:mcp__claude-code-remote__list_triggers,mcp__claude-code-remote__create_trigger,mcp__claude-code-remote__update_trigger,mcp__claude-code-remote__delete_trigger,mcp__claude-code-remote__fire_trigger`. If none of them exist, scheduled tasks aren't available from here; say so and stop.

Load `nudge:board` first: the config holds the values the templates need (`timezone`, `your name`, `price watch on`). When `nudge:setup` is running you, don't: it gives you the copy, whose config and templates are already filled.

## The jobs

Templates are in `references/jobs/`: `morning.md`, `afternoon.md`, `evening.md`, `week.md`, `price-watch.md`. Each starts with a header (job name, suggested cron, connectors, notifications, model note), then a `--- prompt ---` line; everything after that line is the prompt, verbatim, once its placeholders are filled. The header owns the job's name, default time and days.

The jobs are Morning plan, Afternoon nudge, Evening check-in, Weekly recap and plan, and Daily price watch (only when the config's `price watch on` is `yes`). Each prompt is a short wrapper that loads the job's skill, `nudge:morning`, `nudge:afternoon`, `nudge:evening`, `nudge:week` or `nudge:price-watch`, which holds the procedure.

Times are in the config's `timezone`.

## Connectors

A job inherits the connectors attached to the session that creates it. The tracker connector must be attached to this session now, or every run of the job will fail its connection check. Claude in Chrome is never attached to a job.

## Listing

`list_triggers`, recurring only. Match the user's jobs by name against the job names above. Show each as: name, schedule in words in the user's timezone (from its `CRON_TZ` cron), on or off, and the last run's status and time. Omit `trigger_id`s unless asked.

## Creating

For each job the user wants:

1. Read its template. Replace every `~~` placeholder in the prompt with the matching config value (the placeholder named for each config key with that key's value). Grep the result for `~~` to confirm none are left.
2. Pick the time. The header's default is the starting point; the user can name another. Then apply the jitter rule: never land on :00 or :30. When a time would land on the hour or half hour, move it 1–29 minutes earlier (the number of letters in the job's name, modulo 29, plus 1), and say so. Runs that start between 06:00 and 09:00 Pacific time can be delayed. Convert the job's time to Pacific; if it falls in that window, say so and keep it unless they'd rather move it.
3. `create_trigger` with:
   - `name`: the job name from the header.
   - `prompt`: the filled prompt.
   - `cron_expression`: `CRON_TZ=<timezone from the config> <minute> <hour> * * <days>`, days from the header (`1-5` weekdays, `0` Sunday, `*` every day), unless the user chose otherwise.
   - `notifications`: `{push: true, email: false}`, unless the user asks for email.
   - `initiation`: `human_request`.
   - Leave `permission_mode` unset.
4. Tell the user, in one sentence, which approval mode the task got (`derived_state.permission_mode` in the result: `auto` means runs go ahead on their own; absent means a run stops when an action needs approval, and nobody is there to approve a scheduled run), and that automatic approval can be turned on in the task's settings if the organization allows it.

Create the price watch job only when the config's `price watch on` is `yes`.

## Running a job now

`fire_trigger` with `trigger_id` starts a run outside its schedule, with the job's own prompt and connectors; that's the way to check a new job. To do a job's work in chat instead, load its skill and follow it from step 1 ("run the morning plan now").

## Re-syncing a prompt

The prompts stored in the scheduled tasks are wrappers: the procedure lives in each job's skill, so a plugin update reaches the jobs without touching them. A stored prompt only goes stale when its template changes, which is rare. When one does: `list_triggers`, match each job by name, fill the template again as in Creating step 1, and `update_trigger` with `trigger_id` and the new `prompt`. Nothing else changes; the job keeps its schedule and run history. Never delete and recreate a job to change its prompt.

## Changing a time

`update_trigger` with `trigger_id` and a new `cron_expression`, built as in Creating steps 2 and 3, keeping the job's current days. Confirm the new schedule in words, and say when the jitter rule moved the minute.

## Turning a job off and on

`update_trigger` with `trigger_id` and `enabled: false` to turn a job off, `enabled: true` to turn it on. A job that's off stays stored and never fires. This is for stretches when the user wants no jobs at all; for days off, `/nudge:days-off` is the lighter tool, since dated work still gets its reminders.

## Deleting

Confirm with the user first; deleting also removes the sessions the job started. Then `delete_trigger` with `trigger_id`. To stop a job without losing its history, turn it off instead.
