# ntm names

User-facing names change only with Justin's explicit yes, and this file is the
authority. Plugin-internal names (agent requests, status, delivery and result
lines, database headings) don't need his yes and aren't listed: they never reach
the user as they are, and anything a user reads is plain words.

Every name here is as it is on main, unless it's marked "decided, not yet on
main"; `DECISIONS.md` has the work to build it. The last section is 0.4 only.
"Approved" means the notes record his yes, and a time or a source says where. A
yes counts when his words name the thing: case and hyphens in his prose lists
don't matter ("price-watch stores" is `Price watch stores`), different words do.
Dates are 2026-11-05 unless given; times are entries in the old decision log,
which git history keeps. "Names pass" is his pass through the open name
questions on 2026-11-07.

## Skills

All approved. The Yes column says where his yes was given; notes a to f are
under the table.

| Skill                        | What it is                                      | Yes        |
| ---------------------------- | ----------------------------------------------- | ---------- |
| `afternoon-reminder`         | The afternoon reminder                          | 15:33      |
| `configure`                  | Setup wizard; each part to its configure skill  | 16:52      |
| `configure-notifications`    | Channel, Pushover keys, one test push           | names list |
| `configure-schedule`         | The user's jobs: kinds, days, times, titles     | 15:25      |
| `configure-style`            | Builds or revises `ntm-user:style`              | audit      |
| `configure-todo-list`        | Where the list lives, the agreements on it      | note a     |
| `conventions`                | Rules for the todo list; the backend guides     | 14:50      |
| `evening-reminder`           | The evening reminder                            | 15:33      |
| `fix-todo-list`              | Closes done parents; clears stale dates         | 15:49      |
| `help`                       | Answers from the installed README               | note b     |
| `morning-reminder`           | The morning reminder                            | 15:33      |
| `notify`                     | Sends a notification on the user's channel      | 15:25      |
| `pause`                      | Days nothing gets planned automatically         | 16:01      |
| `plan`                       | Sets planned dates, by `--auto` or in chat      | 15:25      |
| `price-watch`                | Which watched items are a good deal today       | audit      |
| `ready-check`                | Proves a session can run a job                  | 14:53      |
| `review-todo-list`           | Reviews the list with the user, chat only       | note c     |
| `self-test`                  | The whole loop on a throwaway task and database | note d     |
| `settings`                   | Shows, changes settings; builds the `.plugin`   | names list |
| `show-completed`             | What got done over a span                       | 16:01      |
| `sync-price-watch-to-amazon` | Amazon alerts for watched items, by browser     | note e     |
| `today`                      | What's planned (default: today and earlier)     | answers    |
| `weekly-planning`            | Closes out the week, tidies, plans the next     | note f     |

Short sources: "names list" is his names list (11-05), "audit" the names audit
(11-06), "answers" Justin's answers (11-06 08:00). `settings` is the one builder
of `ntm-user.plugin`.

- a: Justin's answers, 11-06 08:00; the rename table was then posted on PR #1,
  which he merged.
- b: his names list, 11-05; kept in the names audit, 11-06.
- c: 15:49; restored in the names audit, 11-06.
- d: the old 0.4 design page: "Both keep the name `self-test` (Justin,
  2026-11-06)"; 20:12 had it pending.
- e: his yes in chat, 11-07; the old log has only "with" (16:43).
- f: approved tentatively in the names audit, 11-06. Decided, not yet on main:
  removed (names pass); `configure-schedule` builds that job with each user.

## Agents

| Agent       | What it is                                    | Status               |
| ----------- | --------------------------------------------- | -------------------- |
| `messenger` | Writes reminders, sends them through `notify` | approved, 15:25      |
| `shopper`   | Checks one watched task for a good deal       | approved, 15:25      |
| `estimator` | Estimates, time guesses, review support       | approved, names pass |

## Plugins

| Plugin              | What it is                  | Status          |
| ------------------- | --------------------------- | --------------- |
| `ntm`               | The base plugin             | approved, 16:55 |
| `ntm-user`          | The user's generated plugin | approved, 17:57 |
| `ntm-user:settings` | The user's settings         | approved, 17:57 |
| `ntm-user:style`    | The user's style            | approved, 17:57 |
| `ntm-user.plugin`   | The file the user installs  | approved, 17:57 |

The displayName is `Neurodivergent Task Manager (ntm)` on main. Decided, not yet
on main: `Neurodivergent Task Manager`, without "(ntm)", in plugin.json and the
README's title (16:55, and the names pass).

## Settings

The headings (`About you`, `Todo list`, `Labels`, `Planning`, `Shopping`,
`Notifications`, `Deviations`) are internal and fine as they are (names pass).

Keys approved: `Channel` (17:55, 18:13), its values `pushover` (18:13) and
`claude-push` (names pass), and, in the names pass, `Pushover user key`,
`Pushover app token`, `Timezone`, `Country and currency`, `Backend`,
`List name`, `List id`, `Amazon interface`.

Decided, not yet on main (names pass):

- renamed: `Never picks` to `Excluded labels from automatic scheduling`
- merged: `Task labels` and `Project labels` into one `Labels` list
- merged: `Estimate scale` and `Estimate mapping` into `Estimate pattern`
- moved to job prompts: `Rhythm`, `Planning days`, `Plans ahead`,
  `A day's worth`, `Weekly message`
- moved to each watched task: `Condition`, `Delivery`, `A deal`
- dropped: `Name`, `Task prefix`, `Your tasks`, `Statuses` and its class names,
  `Price watch project`, `Notes` and its per-database titles, `Parents`,
  `Estimate help`

## Database titles (on the todo list)

The plugin fixes these titles; a user's rename goes in Deviations.

| Name                 | Status                            | Source             |
| -------------------- | --------------------------------- | ------------------ |
| `Pauses`             | approved                          | 16:01              |
| `Message history`    | approved                          | names audit, 11-06 |
| `Task review log`    | approved                          | names audit, 11-06 |
| `Price watch stores` | approved                          | 17:57              |
| `Amazon alert steps` | decided, not yet on main: removed | names pass         |

`Amazon alert steps` goes as a 0.3 bug fix: `sync-price-watch-to-amazon` carries
the steps itself.

## Default labels

Default names, all approved. In plugin text, `$` in front marks a label the user
configures; it isn't part of the name.

| Name                | What it is             | Source                    |
| ------------------- | ---------------------- | ------------------------- |
| $no-autoschedule    | Task and project label | 17:55; terminology, 11-06 |
| $pending-shipment   | Task label             | 17:55; terminology, 11-06 |
| $amazon-unavailable | Task label             | 17:55; terminology, 11-06 |
| $has-amazon-alert   | Task label             | names audit, 11-06        |
| $price-watch        | Project label          | 17:55; terminology, 11-06 |

## Job titles

Titles are the user's, chosen live in `configure-schedule`, and nothing matches
on them (names pass). Main still fixes default titles (`Morning reminder` to
`Completed this month`) and a job kind `Completed` as match keys. Decided, not
yet on main: no fixed titles or kinds; matching keys off skill names.

## Skill arguments

Approved: `plan --auto day` and `plan --auto week` (15:25), `pause --check`
(16:01), `configure-todo-list [linear|<name>]` (18:04, given for
`configure-integration`, with backends linear, claude-docs, other), and
`fix-todo-list --dry-run` (names pass).

Decided, not yet on main (names pass):

- `plan --auto <range>`, the range in words (`week mon-fri`,
  `all weekdays this month`)
- the `configure` part `todo list` becomes `todo-list`

The rest stand as on main; the names pass changed only these. Users type
`pause --until`, `show-completed <span in words> [--notify]` and the other
`configure` parts (`about-you`, `notifications`, `style`, `schedule`). Jobs and
skills pass `ready-check --notify-failure`, the `notify` flags and the
`ntm-user:style` flags (`--stay-fresh`, from his own persona skill at 21:52, and
`--for`); those are internal.

## The style profile

His list (18:13) was register, the hook, escalation (+ climb rule), signature
moves (+ repeat limit), what stays untouched, examples. In the names pass,
main's names stand: `Register`, `What gets you to read`, `The reminders`,
`When something keeps slipping`, `Motifs` with its `Repeat limit:` line,
`Examples`, the `Profanity:` line, and `## For ntm` above a persona's body.

Decided, not yet on main: `Off limits` is removed from the profile, and the
builder never asks about it.

## 0.4 only (decided for 0.4, not on main)

- Base plugin `neurodivergent-task-manager`, user plugin `ntm`, and an optional
  alias plugin named with the user's own word (11-06).
- `setup` and `update` as more ways into `configure`; the base drops its
  `settings` skill (11-06).
- Contracts in the user plugin: `todo-list` stays the backend guide's contract,
  `ready-check` is in the user plugin only, both plugins keep `self-test`
  (11-06); `notify` carries the user's Pushover-or-chat choice (11-07, from
  #18's notes).
- From the old 0.4 design page, not attributed to Justin: `settings` and `style`
  as contracts, the `Version:` line in the user's settings,
  `configure/references/generator.md`,
  `configure/references/versions/<version>.md`.
