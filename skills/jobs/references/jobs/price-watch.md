# Daily price watch

Header; not part of the prompt. Optional: create this job only when the config's `price watch on` is `yes`.

| | |
| --- | --- |
| Job name | Daily price watch |
| Suggested cron | `CRON_TZ=~~timezone 0 7 * * *` (every day, including days off) |
| Connectors | the tracker connector named by the config's `tracker`. Never Claude in Chrome. |
| Notifications | push on, email off |
| Model | Tested on Opus; cheaper models haven't been. |

--- prompt ---

Daily price watch for ~~your name's board. Skills return text; you decide what reaches the user.

This job runs every day, including days off, and writes plainly: it doesn't check `/nudge:days-off` or use `/nudge:voice`.

Load `nudge:price-watch` and follow it from step 1. Its FINAL REPLY and ERROR HANDLING are this job's.
If `nudge:price-watch` can't be loaded, end the run with `Daily price watch FAILED: nudge:price-watch couldn't be loaded; check the plugin is installed and enabled.`
