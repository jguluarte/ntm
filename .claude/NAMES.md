# ntm names

Names change only with Justin's explicit yes, and this file is the authority.

Every name here is as it is on main; the last section is not on main. "Approved"
means the notes record his yes, and a time or a source says where. A yes counts
when his words name the thing: case and hyphens in his prose lists don't matter
("price-watch stores" is `Price watch stores`), different words do. Anything
else is a question for him, and the questions come first. Dates are 2026-11-05
unless given; times are entries in the old decision log, which git history
keeps.

## Questions for Justin

Drifted from his yes:

1. displayName: he settled `Neurodivergent Task Manager` for the plugin (16:55)
   and said again on 11-06 (19:37): without "(ntm)". Main has
   `Neurodivergent Task Manager (ntm)` in plugin.json, and the same "(ntm)" in
   the README's first heading and `help`'s description. Drop it in all three?
2. Channel value: main has `claude-push`; he said `claude` (18:13).
3. Note title: main has `Amazon alert steps`. His list of notes (17:57) names it
   "Amazon alert flow", its title in 0.1.0; no yes for "steps" is recorded.
4. Style profile headings (see The style profile):
   `When something keeps slipping` (his "escalation"), `Motifs` ("signature
   moves"), `Off limits` ("what stays untouched"), and `The reminders`, which
   has no counterpart in his list. And `What gets you to read` was kept earlier
   on 11-05, but his later list (18:13) calls that section "the hook". Which
   stands?
5. Default job titles: he decided titles belong to each user, with nothing
   locked by the plugin (19:47). Main fixes the default titles
   (`Morning reminder` ... `Completed this month`) as the names notifications
   and tokens are matched by (`configure-schedule`), and `notify --from`, the
   messenger's `job:` line and `show-completed`'s job names all key off them.
   Keep them as fixed names, or stop matching on titles?
6. The overview job: his kind is "overview"; main names the kind `Completed`
   (`### Completed` in `configure-schedule`), with the titles
   `Completed this week` and `Completed this month`, and `show-completed` uses
   `Completed` as the job name for any other span. Approve these names?

Never approved:

7. Agent `estimator` (came in #15, which he merged).
8. Settings headings `About you`, `Planning`, `Shopping`.
9. Settings keys:
    - About you: `Name`, `Timezone`, `Country and currency`
    - Todo list: `Backend`, `List name`, `List id`, `Task prefix`, `Your tasks`,
      `Statuses` and its class names, `Price watch project`, and `Notes` with
      its sub-keys
    - Labels: `Task labels`, `Project labels`
    - Planning: `Rhythm`, `Planning days`, `Plans ahead`, `A day's worth`,
      `Never picks`, `Parents`, `Weekly message`
    - Shopping: `Condition`, `Delivery`, `A deal`, `Amazon interface`
    - Notifications: `Pushover app token`, `Pushover user key`
10. Came in only with merged PRs (#8, #15): `Estimate scale`,
    `Estimate mapping`, `Estimate help`. Confirm?
11. Skill arguments: `--notify`, `--notify-failure`, `--dry-run`, `--until`,
    `--stay-fresh`, `--for` and its values; every `notify` flag; the `configure`
    part names (`about-you` has a hyphen, `todo list` a space).
12. Internal names nobody ruled on (see Agent requests, Note and comment
    headings, Internal markers, The style profile): one yes for the lot, or one
    by one?
13. Optional: `weekly-planning` for good (his yes was tentative).

## Skills

All approved; `weekly-planning` only tentatively (Q13). The Yes column says
where his yes was given; notes a to e are under the table.

| Skill                        | What it is                                     | Yes        |
| ---------------------------- | ---------------------------------------------- | ---------- |
| `afternoon-reminder`         | The afternoon reminder                         | 15:33      |
| `configure`                  | Setup wizard; each part to its configure skill | 16:52      |
| `configure-notifications`    | Channel, Pushover keys, one test push          | names list |
| `configure-schedule`         | The user's jobs: kinds, days, times, titles    | 15:25      |
| `configure-style`            | Builds or revises `ntm-user:style`             | audit      |
| `configure-todo-list`        | Where the list lives, the agreements on it     | note a     |
| `conventions`                | Rules for the todo list; the backend guides    | 14:50      |
| `evening-reminder`           | The evening reminder                           | 15:33      |
| `fix-todo-list`              | Closes done parents; clears stale dates        | 15:49      |
| `help`                       | Answers from the installed README              | note b     |
| `morning-reminder`           | The morning reminder                           | 15:33      |
| `notify`                     | Sends a notification on the user's channel     | 15:25      |
| `pause`                      | Days nothing gets planned automatically        | 16:01      |
| `plan`                       | Sets planned dates, by `--auto` or in chat     | 15:25      |
| `price-watch`                | Which watched items are a good deal today      | audit      |
| `ready-check`                | Proves a session can run a job                 | 14:53      |
| `review-todo-list`           | Reviews the list with the user, chat only      | note c     |
| `self-test`                  | The whole loop on a throwaway task and note    | note d     |
| `settings`                   | Shows, changes settings; builds the `.plugin`  | names list |
| `show-completed`             | What got done over a span                      | 16:01      |
| `sync-price-watch-to-amazon` | Amazon alerts for watched items, by browser    | note e     |
| `today`                      | What's planned (default: today and earlier)    | answers    |
| `weekly-planning`            | Closes out the week, tidies, plans the next    | audit      |

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

## Agents

| Agent       | What it is                                    | Status              |
| ----------- | --------------------------------------------- | ------------------- |
| `messenger` | Writes reminders, sends them through `notify` | approved, 15:25     |
| `shopper`   | Checks one watched task for a good deal       | approved, 15:25     |
| `estimator` | Estimates, time guesses, review support       | NEVER APPROVED (Q7) |

`estimator` came in with #15; its name was never approved.

## Agent requests

Skills ask agents for these by name. All came in with #15, and none is approved
(Q12):

- `estimator`: `Estimate a task`, `Time tasks`, `Explain estimating`, `Review`
- `messenger`: the request lines `reminder:`, `job:`, `today:` and the other
  facts

## Plugins

| Plugin              | What it is                  | Status          |
| ------------------- | --------------------------- | --------------- |
| `ntm`               | The base plugin             | approved, 16:55 |
| `ntm-user`          | The user's generated plugin | approved, 17:57 |
| `ntm-user:settings` | The user's settings         | approved, 17:57 |
| `ntm-user:style`    | The user's style            | approved, 17:57 |
| `ntm-user.plugin`   | The file the user installs  | approved, 17:57 |

The displayName `Neurodivergent Task Manager (ntm)`, in plugin.json and also the
README's first heading and `help`'s description, DRIFTED from his 16:55 yes
(Q1).

## Settings headings (`ntm-user:settings`)

| Heading         | Status              | Source                           |
| --------------- | ------------------- | -------------------------------- |
| `Todo list`     | approved            | answers ("board" to "todo list") |
| `Labels`        | approved            | 17:55                            |
| `Notifications` | approved            | 17:55                            |
| `Deviations`    | approved            | 17:55                            |
| `About you`     | NEVER APPROVED (Q8) |                                  |
| `Planning`      | NEVER APPROVED (Q8) |                                  |
| `Shopping`      | NEVER APPROVED (Q8) |                                  |

## Settings keys

| Under         | Name                        | Status                            |
| ------------- | --------------------------- | --------------------------------- |
| Notifications | `Channel`                   | approved, 17:55 and 18:13         |
| Notifications | channel value `pushover`    | approved, 18:13                   |
| Notifications | channel value `claude-push` | DRIFTED (Q2): 18:13 said `claude` |

Only by merged PRs #8 and #15 (Q10): under Planning, `Estimate scale`,
`Estimate mapping`, `Estimate help`.

NEVER APPROVED (Q9):

- Notifications: `Pushover app token`, `Pushover user key`
- About you: `Name`, `Timezone`, `Country and currency`
- Todo list: `Backend`, `List name`, `List id`, `Task prefix`, `Your tasks`,
  `Price watch project`. 17:55 says only "tracker, board/team, ids, status
  names".
- Todo list: `Statuses`, and its classes `plannable`, `started`, `blocked`,
  `done`, `canceled`, `duplicate`
- Todo list: `Notes`, one key, with one lowercase sub-key per note (`pauses`,
  `message history`, `task review log`, `price watch stores`,
  `Amazon alert steps`)
- Labels: `Task labels`, `Project labels`
- Planning: `Rhythm`, `Planning days`, `Plans ahead`, `A day's worth`,
  `Never picks`, `Parents`, `Weekly message`
- Shopping: `Condition`, `Delivery`, `A deal`, `Amazon interface`

## Note titles (on the todo list)

| Name                 | Status       | Source                         |
| -------------------- | ------------ | ------------------------------ |
| `Pauses`             | approved     | 16:01                          |
| `Message history`    | approved     | names audit, 11-06             |
| `Task review log`    | approved     | names audit, 11-06             |
| `Price watch stores` | approved     | 17:57                          |
| `Amazon alert steps` | DRIFTED (Q3) | 17:57 said "Amazon alert flow" |

## Note and comment headings

All NEVER APPROVED (Q12):

- message history note: the `Keep:` line
- pauses note: `## Pauses`, and `None.` when empty
- task review log note: `## How you work`, `## Estimates`
- price watch stores note: `## Seed`, `## Vouched`, `## Blocked`
- the shopper's comment on a task: `Stores:`, with its `Not used` and `Problems`
  parts

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

## Default job titles

- `Morning reminder`, `Afternoon reminder`, `Evening reminder`,
  `Weekly planning`, `Price watch`: match his job kinds (19:47); main fixes them
  as match keys (Q5).
- `Completed this week`, `Completed this month`: NEVER APPROVED; his kind is
  "overview" (Q6).
- The job kind `Completed`: NEVER APPROVED (Q6).

`Completed` on its own is not a job title: it's the job name `show-completed`
passes with `--notify` for a span that is neither a week nor a month (Q6).

## Skill arguments

Approved:

- `plan --auto day`, `plan --auto week` (15:25)
- `pause --check` (16:01)
- `configure-todo-list [linear|<name>]` (18:04, given for
  `configure-integration`, with backends linear, claude-docs, other)

NEVER APPROVED (Q11):

- `pause --until`
- `fix-todo-list --dry-run`
- `show-completed <span in words> [--notify]`
- `ready-check --notify-failure "<job name>"`
- `notify --title --message --url --priority --from --app-token --user-key`
- `ntm-user:style --stay-fresh` (from his own persona skill, 21:52), `--for`
  (morning, afternoon, evening, week, completed), a tone
- `configure <part>`: `about-you`, `todo list`, `notifications`, `style`,
  `schedule`

## Internal markers

Lines skills and agents return to each other.

Approved (11-05 first table, "internal, decided"): `Messenger FAILED:`,
`Title:`.

NEVER APPROVED (Q12):

- `<Skill> FAILED:` (Notify, Ready-check, Plan, Pause, Today, Show-completed,
  Fix-todo-list, Price-watch, Sync-price-watch-to-amazon, Configure-todo-list,
  Shopper)
- `Ready-check OK`, `Ready-check OK (no style)`
- `Self-test OK`, `Self-test FAILED at <step>:` (proposed at 20:12, "name
  pending Justin")
- `Sent:`, `List:`, `NOTIFY VIA FINAL REPLY`, `Price-watch:`
- `Notify TOO LONG:`, `Messenger NEEDS:` (#18)
- the shopper's result lines `RESULT`, `DEAL`, `COMPARE`, `OTHER VERIFIED`,
  `CHECKED`, `NOTES`, and results `DEAL`, `NO DEAL`, `NO VERIFIED PRICE`,
  `NOT ACTIONABLE`

## The style profile

His list (18:13) was register, the hook, escalation (+ climb rule), signature
moves (+ repeat limit), what stays untouched, examples.

- `Register`: approved (18:13)
- `What gets you to read`: kept (11-05 first table); his 18:13 list says "the
  hook" (Q4)
- `The reminders`: NEVER APPROVED; nothing in his list matches (Q4)
- `When something keeps slipping`: DRIFTED from "escalation" (Q4)
- `Motifs`: DRIFTED from "signature moves" (Q4)
- the `Repeat limit:` line, under Motifs: approved (18:13)
- `Off limits`: DRIFTED from "what stays untouched" (Q4)
- `Examples`: approved (18:13)
- the `Profanity:` line: NEVER APPROVED (Q12)
- `## For ntm`, written above a persona's body: NEVER APPROVED as a name (Q12)

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
