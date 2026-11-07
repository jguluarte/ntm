# ntm names

Names change only with Justin's explicit yes, and this file is the authority.

Every name here is as it is on main. "Approved" means the notes record his yes.
Anything else is a question for him, and the questions come first.

## Questions for Justin

Drifted from his yes:

1. displayName: main has `Neurodivergent Task Manager (ntm)`. He approved
   `Neurodivergent Task Manager`, and later said again: without "(ntm)". That
   later call sits with the 0.4 items. Is it for main too, or only 0.4?
2. Channel value: main has `claude-push`; he said `claude`.
3. Note title: main has `Amazon alert steps`; his entry says "Amazon alert flow"
   (the 0.1.0 title).
4. Style profile headings: main's differ from the sections he listed (see The
   style profile below). Only "What gets you to read" is a recorded keep.

Never approved:

5. Agent `estimator` (came in #15, which he merged).
6. Settings headings `About you`, `Planning`, `Shopping`.
7. Settings keys:
    - About you: `Name`, `Timezone`, `Country and currency`
    - Todo list: `Backend`, `Your tasks`, `Price watch project`, `Notes` (the
      key; each note title is classed on its own), and the status class names
    - Planning: `Rhythm`, `Planning days`, `Plans ahead`, `A day's worth`,
      `Never picks`, `Parents`, `Weekly message`
    - Shopping: `Condition`, `Delivery`, `A deal`, `Amazon interface`
    - Notifications: `Pushover app token`, `Pushover user key`
8. Came in only with merged PRs (#8, #15): `Estimate scale`, `Estimate mapping`,
   `Estimate help`. Confirm?
9. Job titles: `Completed this week` and `Completed this month`, against his job
   kind "overview". The other five titles match his job kinds, but the item was
   parked and never closed. Close it?
10. Skill arguments: `--notify`, `--notify-failure`, `--dry-run`, `--until`,
    `--stay-fresh`, `--for` and its values; every `notify` flag; the `configure`
    part names (`about-you` has a hyphen, `todo list` a space).
11. Optional: `weekly-planning` for good (his yes was tentative).

## Skills

| Name                         | What it is                                                       | Status                      |
| ---------------------------- | ---------------------------------------------------------------- | --------------------------- |
| `afternoon-reminder`         | The afternoon reminder                                           | approved                    |
| `configure`                  | The setup wizard; hands each part to its configure skill         | approved                    |
| `configure-notifications`    | Channel, Pushover keys, one test push                            | approved                    |
| `configure-schedule`         | The user's jobs: which kinds, days, times, titles                | approved                    |
| `configure-style`            | Builds or revises `ntm-user:style`                               | approved                    |
| `configure-todo-list`        | Where the list lives and the agreements ntm works by on it       | approved                    |
| `conventions`                | Rules for the todo list, and the backend guides                  | approved                    |
| `evening-reminder`           | The evening reminder                                             | approved                    |
| `fix-todo-list`              | Closes finished parents, clears stale planned dates              | approved                    |
| `help`                       | Answers from the installed README                                | approved                    |
| `morning-reminder`           | The morning reminder                                             | approved                    |
| `notify`                     | Sends a notification on the user's channel                       | approved                    |
| `pause`                      | Days when nothing gets planned automatically                     | approved                    |
| `plan`                       | Sets planned dates: `--auto day`, `--auto week`, or in chat      | approved                    |
| `price-watch`                | Which watched items are a good deal today                        | approved                    |
| `ready-check`                | Proves a session can run a job                                   | approved                    |
| `review-todo-list`           | Reviews the list with the user, in chat only                     | approved                    |
| `self-test`                  | The whole loop on a throwaway task and note                      | approved                    |
| `settings`                   | Shows and changes settings; the one builder of `ntm-user.plugin` | approved                    |
| `show-completed`             | What got done over a span                                        | approved                    |
| `sync-price-watch-to-amazon` | Amazon alerts for watched items, through the browser             | approved                    |
| `today`                      | What's planned (default: today and earlier)                      | approved                    |
| `weekly-planning`            | Closes out the week, tidies, plans the next                      | approved, tentatively (Q11) |

## Agents

| Name        | What it is                                     | Status                      |
| ----------- | ---------------------------------------------- | --------------------------- |
| `messenger` | Writes and sends reminders in the user's style | approved                    |
| `shopper`   | Checks one watched task for a good deal        | approved                    |
| `estimator` | Estimates, time guesses, review support        | NEVER APPROVED by name (Q5) |

## Plugins

| Name                                | What it is                  | Status       |
| ----------------------------------- | --------------------------- | ------------ |
| `ntm`                               | The base plugin             | approved     |
| `ntm-user`                          | The user's generated plugin | approved     |
| `ntm-user:settings`                 | The user's settings         | approved     |
| `ntm-user:style`                    | The user's style            | approved     |
| `ntm-user.plugin`                   | The file the user installs  | approved     |
| `Neurodivergent Task Manager (ntm)` | displayName in plugin.json  | DRIFTED (Q1) |

## Settings headings (`ntm-user:settings`)

| Name            | Status              |
| --------------- | ------------------- |
| `Todo list`     | approved            |
| `Labels`        | approved            |
| `Notifications` | approved            |
| `Deviations`    | approved            |
| `About you`     | NEVER APPROVED (Q6) |
| `Planning`      | NEVER APPROVED (Q6) |
| `Shopping`      | NEVER APPROVED (Q6) |

## Settings keys

| Heading       | Name                                                                                                  | Status                       |
| ------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------- |
| Todo list     | `List name`, `List id`, `Task prefix`                                                                 | approved                     |
| Todo list     | `Notes` (one key per note title)                                                                      | NEVER APPROVED as a key (Q7) |
| Notifications | `Channel`                                                                                             | approved                     |
| Notifications | channel value `pushover`                                                                              | approved                     |
| Notifications | channel value `claude-push`                                                                           | DRIFTED (Q2)                 |
| About you     | `Name`, `Timezone`, `Country and currency`                                                            | NEVER APPROVED (Q7)          |
| Todo list     | `Backend`, `Your tasks`, `Price watch project`                                                        | NEVER APPROVED (Q7)          |
| Todo list     | status classes `plannable`, `started`, `blocked`, `done`, `canceled`, `duplicate`                     | NEVER APPROVED (Q7)          |
| Planning      | `Rhythm`, `Planning days`, `Plans ahead`, `A day's worth`, `Never picks`, `Parents`, `Weekly message` | NEVER APPROVED (Q7)          |
| Planning      | `Estimate scale`, `Estimate mapping`, `Estimate help`                                                 | only by merged PR (Q8)       |
| Shopping      | `Condition`, `Delivery`, `A deal`, `Amazon interface`                                                 | NEVER APPROVED (Q7)          |
| Notifications | `Pushover app token`, `Pushover user key`                                                             | NEVER APPROVED (Q7)          |

## Note titles (on the todo list)

| Name                 | Status       |
| -------------------- | ------------ |
| `Pauses`             | approved     |
| `Message history`    | approved     |
| `Task review log`    | approved     |
| `Price watch stores` | approved     |
| `Amazon alert steps` | DRIFTED (Q3) |

## Default labels

| Name                | What it is             | Status   |
| ------------------- | ---------------------- | -------- |
| $no-autoschedule    | Task and project label | approved |
| $pending-shipment   | Task label             | approved |
| $amazon-unavailable | Task label             | approved |
| $has-amazon-alert   | Task label             | approved |
| $price-watch        | Project label          | approved |

## Default job titles

| Name                                                                                           | Status                    |
| ---------------------------------------------------------------------------------------------- | ------------------------- |
| `Morning reminder`, `Afternoon reminder`, `Evening reminder`, `Weekly planning`, `Price watch` | parked, never closed (Q9) |
| `Completed this week`, `Completed this month`, `Completed` for other spans                     | NEVER APPROVED (Q9)       |

## Skill arguments

| Name                                                                                          | Status               |
| --------------------------------------------------------------------------------------------- | -------------------- |
| `plan --auto day`, `plan --auto week`                                                         | approved             |
| `pause --check`                                                                               | approved             |
| `configure-todo-list [linear\|<name>]`                                                        | approved             |
| `pause --until`                                                                               | NEVER APPROVED (Q10) |
| `fix-todo-list --dry-run`                                                                     | NEVER APPROVED (Q10) |
| `show-completed <span in words> [--notify]`                                                   | NEVER APPROVED (Q10) |
| `ready-check --notify-failure "<job name>"`                                                   | NEVER APPROVED (Q10) |
| `notify --title --message --url --priority --from --app-token --user-key`                     | NEVER APPROVED (Q10) |
| `ntm-user:style --stay-fresh`, `--for` (morning, afternoon, evening, week, completed), a tone | NEVER APPROVED (Q10) |
| `configure <part>`: `about-you`, `todo list`, `notifications`, `style`, `schedule`            | NEVER APPROVED (Q10) |

## Internal markers

| Name                | Status   |
| ------------------- | -------- |
| `Messenger FAILED:` | approved |
| `Title:`            | approved |

## The style profile

Headings on main: Register, What gets you to read, The reminders, When something
keeps slipping, Motifs, Off limits, Examples. His list was register, the hook,
escalation, signature moves, what stays untouched, examples. Only "What gets you
to read" is approved; the rest are Q4.

## In open PRs, not on main yet

- #18: `Notify TOO LONG`, `Messenger NEEDS`.

## 0.4 only (decided for 0.4, not on main)

- Base plugin `neurodivergent-task-manager`, user plugin `ntm`, and an optional
  alias plugin named with the user's own word.
- `setup` and `update` as more ways into `configure`; the base drops `settings`.
- Contracts in the user plugin: `settings`, `style`, `notify`, `todo-list`,
  `ready-check` (user plugin only), `self-test` (both plugins).
- From the old 0.4 design page, not attributed to Justin: the `Version:` line in
  settings, `configure/references/generator.md`,
  `configure/references/versions/<version>.md`.
