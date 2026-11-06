# Evening reminder

Header; not part of the prompt.

| | |
| --- | --- |
| Default title | Evening reminder |
| Suggested schedule | `CRON_TZ=<timezone from About you in your settings> 30 19 * * 1-5` (weekdays 19:30, before the jitter rule) |
| Connectors | the backend connector named by Board in your settings. Never a browser. |
| Notifications | push on |

--- prompt ---

Evening reminder.
Load `ntm:evening-reminder` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING are this job's.
If `ntm:evening-reminder` can't be loaded, end the run with `Evening reminder FAILED: ntm:evening-reminder couldn't be loaded; check the ntm plugin is installed and enabled.`
