# Evening check-in

Header; not part of the prompt.

| | |
| --- | --- |
| Job name | Evening check-in |
| Suggested cron | `CRON_TZ=~~timezone 30 19 * * 1-5` (weekdays) |
| Connectors | the tracker connector named by the config's `tracker`. Never Claude in Chrome. |
| Notifications | push on, email off |
| Model | Tested on Opus; cheaper models haven't been. |

--- prompt ---

Evening check-in for ~~your name's board.
Load `nudge:evening` and follow it from step 1.
Its FINAL REPLY and ERROR HANDLING are this job's.
If `nudge:evening` can't be loaded, end the run with `Evening check-in FAILED: nudge:evening couldn't be loaded; check the plugin is installed and enabled.`
