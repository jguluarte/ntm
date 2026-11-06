# Completed this week / Completed this month

| | |
| --- | --- |
| Default title | Completed this week (weekly) or Completed this month (monthly) |
| Suggested schedule | weekly: `CRON_TZ=<timezone from About you in your settings> 0 20 * * 0` (Sunday 20:00); monthly: `CRON_TZ=<timezone from About you in your settings> 0 20 1 * *` (the 1st, 20:00); both before the jitter rule |
| Span | weekly: `the last 7 days`; monthly: `last month`. For the monthly job, write `Completed this month` for the title and `last month` for the span in the prompt below. |
| Offered | off by default: offer it, and create it only when the user wants it |
| Connectors | the backend connector named by Board in your settings. Never a browser. |
| Notifications | push on |

--- prompt ---

Completed this week.
Load `ntm:completed` and run `/ntm:completed the last 7 days --notify`. Its Notify section's final reply and error handling are this job's.
If `ntm:completed` can't be loaded, end the run with `Completed this week FAILED: ntm:completed couldn't be loaded; check the ntm plugin is installed and enabled.`
