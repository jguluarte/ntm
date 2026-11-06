# Weekly recap and plan

Header; not part of the prompt.

| | |
| --- | --- |
| Job name | Weekly recap and plan |
| Suggested cron | `CRON_TZ=~~timezone 0 22 * * 0` (Sunday) |
| Connectors | the tracker connector named by the config's `tracker`. Never Claude in Chrome. |
| Notifications | push on, email off |
| Model | Tested on Opus; cheaper models haven't been. |

--- prompt ---

Weekly recap and plan for ~~your name's board.
Load `nudge:week` and follow it from step 1.
Its FINAL REPLY and ERROR HANDLING are this job's.
If `nudge:week` can't be loaded, end the run with `Weekly recap and plan FAILED: nudge:week couldn't be loaded; check the plugin is installed and enabled.`
