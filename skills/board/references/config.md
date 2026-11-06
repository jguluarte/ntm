# Config

Every value this system depends on, in one place. In the template each value is a placeholder (two tildes, then its key); `nudge:setup` fills them in and produces a personalized copy of the plugin. Skills read values from here by key and never hardcode them.

A personalized copy that holds Pushover credentials must stay private. Share the template, not your copy.

## Identity

| Key | Value | Meaning |
| --- | --- | --- |
| your name | ~~your name | How the job prompts name you, e.g. "Morning plan for ~~your name's board". |
| timezone | ~~timezone | IANA zone, e.g. `America/Chicago`. Every date in the system is computed in it. |
| country and currency | ~~country and currency | For price watch: where things ship and what prices are in, e.g. "US, USD". |

## Tracker

| Key | Value | Meaning |
| --- | --- | --- |
| tracker | ~~tracker | `linear`, `claude-docs`, or the name of a custom adapter file under `references/adapters/`, without `.md`. |
| board name | ~~board name | The team or workspace that holds every ticket, as the tracker names it. |
| board id | ~~board id | The board's id, if the tracker needs one for lookups. Blank otherwise. |
| ticket prefix | ~~ticket prefix | The prefix on ticket ids, e.g. `HOME` for `HOME-12`. |

## Statuses

The board's real status names for each status class. Skills reason in classes; the adapter translates. Rows the board has no status for are blank.

| Class | Value | Meaning |
| --- | --- | --- |
| plannable | ~~plannable statuses | Open work that can be planned. Usually three: a backlog, a to-do and an in-progress status. |
| started | ~~started status | The one plannable status that means work has begun. Jobs give credit for it. |
| blocked | ~~blocked status | Open, but the user can't move it right now. Never planned. Blank when the board has no such status. |
| done | ~~done status | Closed, finished. |
| canceled | ~~canceled status | Closed without being done. |
| duplicate | ~~duplicate status | Closed as a duplicate. Ignored everywhere. |

## Labels

| Key | Value | Default | Meaning |
| --- | --- | --- | --- |
| no-autoschedule label | ~~no-autoschedule label | `no-autoschedule` | Opted out of automatic planning. |
| pending-shipment label | ~~pending-shipment label | `pending-shipment` | Something ordered for this ticket hasn't arrived. |
| deadline label | ~~deadline label | `deadline` | A real deadline. Rare; see the board rules. |
| price-watch label | ~~price-watch label | `price-watch` | A purchase whose price is being watched. |
| amazon-alert label | ~~amazon-alert label | `amazon-alert` | An Amazon price alert is set for this item. |
| amazon-unavailable label | ~~amazon-unavailable label | `amazon-unavailable` | The item isn't sold new on Amazon. |

## Notes

Shared texts the system keeps on the board. Each is found by its name.

| Key | Value | Default | Meaning |
| --- | --- | --- | --- |
| days off note | ~~days off note | `Nudge: days off` | Days when nothing gets planned automatically. |
| voice history note | ~~voice history note | `Nudge: voice history` | Recent lines the voice wrote, so they stay fresh. |
| grooming log note | ~~grooming log note | `Nudge: grooming log` | What grooming has learned about how you work, and past estimates. |
| stores note | ~~stores note | `Nudge: price-watch stores` | Seed, vouched and blocked stores for price watch. |
| amazon alert flow note | ~~amazon alert flow note | `Nudge: Amazon alert flow` | How to set and remove Amazon price alerts, as last learned. |
| messenger note | ~~messenger note | `Nudge: messenger` | The messenger profile: voice, what gets you to read, what happens when something keeps slipping, motifs and examples, written by `nudge:messenger`. |

## Voice

| Key | Value | Meaning |
| --- | --- | --- |
| voice on | ~~voice on | `yes` to run reminders through `nudge:voice` and the messenger profile; `no` for reminders as the jobs write them. |
| messenger name | ~~messenger name | What you call the messenger, e.g. "the Butler". Used in chat ("run that through the Butler"). |
| voice history length | ~~voice history length | How much history to keep. Default: 60 entries or 8 weeks, whichever is less. |

The messenger profile itself lives in the note named by `messenger note`, written by `nudge:messenger`.

## Notifications

| Key | Value | Meaning |
| --- | --- | --- |
| channel | ~~channel | `pushover`, or `claude-push` to use the scheduled task's own completion notification. |
| pushover app token | ~~pushover app token | Only with the pushover channel. From your Pushover application. |
| pushover user key | ~~pushover user key | Only with the pushover channel. From your Pushover account page. |

## Price watch

| Key | Value | Meaning |
| --- | --- | --- |
| price watch on | ~~price watch on | `yes` to run the daily price watch job. |
| price watch project | ~~price watch project | The project whose tickets are purchases waiting on a good price. It carries the price-watch and no-autoschedule labels, so its tickets inherit them. |
