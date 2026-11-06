# Morning reminder

| | |
| --- | --- |
| Default title | Morning reminder |
| Suggested schedule | `CRON_TZ=<timezone from About you in your settings> 0 9 * * 1-5` (weekdays 09:00, before the jitter rule) |

--- prompt ---

Morning reminder.
Load `ntm:morning-reminder` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING are this job's.
If `ntm:morning-reminder` can't be loaded, end the run with `Morning reminder FAILED: ntm:morning-reminder couldn't be loaded; check the ntm plugin is installed and enabled.`
