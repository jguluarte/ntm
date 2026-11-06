# Afternoon nudge

Header; not part of the prompt.

| | |
| --- | --- |
| Job name | Afternoon nudge |
| Suggested cron | `CRON_TZ=~~timezone 30 14 * * 1-5` (weekdays) |
| Connectors | the tracker connector named by the config's `tracker`. Never Claude in Chrome. |
| Notifications | push on, email off |
| Model | Tested on Opus; cheaper models haven't been. |

--- prompt ---

Afternoon nudge for ~~your name's board.
Load `nudge:afternoon` and follow it from step 1.
Its FINAL REPLY and ERROR HANDLING are this job's.
If `nudge:afternoon` can't be loaded, end the run with `Afternoon nudge FAILED: nudge:afternoon couldn't be loaded; check the plugin is installed and enabled.`
