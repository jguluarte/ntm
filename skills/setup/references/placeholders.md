# Placeholders

Every `~~placeholder` in the template, which setup phase settles it, and its default. `grep -rn '~~\w'` across the plugin finds them all; after setup, only this file and `CONNECTORS.md` still contain them.

Phases: 1 the tracker, 2 notifications, 3 price watch, 4 rhythm, 5 the messenger. Phase 6 (the copy) gives anything unsettled its default.

| Placeholder | Phase | Default |
| --- | --- | --- |
| `~~your name` | 4 | — |
| `~~timezone` | 4 | — |
| `~~country and currency` | 3 | `US, USD` |
| `~~tracker` | 1 | `linear` |
| `~~board name` | 1 | — |
| `~~board id` | 1 | — |
| `~~ticket prefix` | 1 | — |
| `~~plannable statuses` | 1 | `Backlog, Todo, In Progress` |
| `~~started status` | 1 | `In Progress` |
| `~~blocked status` | 1 | `Blocked` |
| `~~done status` | 1 | `Done` |
| `~~canceled status` | 1 | `Canceled` |
| `~~duplicate status` | 1 | `Duplicate` |
| `~~no-autoschedule label` | 1 | `no-autoschedule` |
| `~~pending-shipment label` | 1 | `pending-shipment` |
| `~~deadline label` | 1 | `deadline` |
| `~~price-watch label` | 1 | `price-watch` |
| `~~amazon-alert label` | 1 | `amazon-alert` |
| `~~amazon-unavailable label` | 1 | `amazon-unavailable` |
| `~~days off note` | 1 | `Nudge: days off` |
| `~~voice history note` | 1 | `Nudge: voice history` |
| `~~grooming log note` | 1 | `Nudge: grooming log` |
| `~~amazon alert flow note` | 1 | `Nudge: Amazon alert flow` |
| `~~messenger note` | 1 | `Nudge: messenger` |
| `~~stores note` | 1 | `Nudge: price-watch stores` |
| `~~voice on` | 4 | `yes` |
| `~~messenger name` | 5 | — |
| `~~voice history length` | 4 | `60 entries or 8 weeks` |
| `~~channel` | 2 | `claude-push` |
| `~~pushover app token` | 2 | blank unless pushover |
| `~~pushover user key` | 2 | blank unless pushover |
| `~~price watch on` | 3 | `no` |
| `~~price watch project` | 3 | `Price Watch` |

When `voice on` is `no`, `messenger name` is blank. When `price watch on` is `no`, `price watch project` and `stores note` keep their defaults.
