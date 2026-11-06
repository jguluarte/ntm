# Price watch

| | |
| --- | --- |
| Default title | Price watch |
| Suggested schedule | `CRON_TZ=<timezone from About you in your settings> 0 7 * * *` (every day, paused days included, 07:00, before the jitter rule) |

--- prompt ---

Price watch.
Load `ntm:price-watch` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING are this job's.
If `ntm:price-watch` can't be loaded, end the run with `Price watch FAILED: ntm:price-watch couldn't be loaded; check the ntm plugin is installed and enabled.`
