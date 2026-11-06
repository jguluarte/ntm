# Afternoon reminder

| | |
| --- | --- |
| Default title | Afternoon reminder |
| Suggested schedule | `CRON_TZ=<timezone from About you in your settings> 30 14 * * 1-5` (weekdays 14:30, before the jitter rule) |
| Connectors | the backend connector named by Board in your settings. Never a browser. |
| Notifications | push on |

--- prompt ---

Afternoon reminder.
Load `ntm:afternoon-reminder` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING are this job's.
If `ntm:afternoon-reminder` can't be loaded, end the run with `Afternoon reminder FAILED: ntm:afternoon-reminder couldn't be loaded; check the ntm plugin is installed and enabled.`
