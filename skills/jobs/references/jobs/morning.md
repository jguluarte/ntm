# Morning plan

Header; not part of the prompt.

| | |
| --- | --- |
| Job name | Morning plan |
| Suggested cron | `CRON_TZ=~~timezone 0 9 * * 1-5` (weekdays) |
| Connectors | the tracker connector named by the config's `tracker`. Never Claude in Chrome. |
| Notifications | push on, email off |
| Model | Tested on Opus; cheaper models haven't been. |

--- prompt ---

Morning plan for ~~your name's board.
Load `nudge:morning` and follow it from step 1.
Its FINAL REPLY and ERROR HANDLING are this job's.
If `nudge:morning` can't be loaded, end the run with `Morning plan FAILED: nudge:morning couldn't be loaded; check the plugin is installed and enabled.`
