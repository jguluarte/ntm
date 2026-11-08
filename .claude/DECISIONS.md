# ntm decisions in force

What's decided and in force on main, by topic. A line marked "decided, to build"
is decided but main doesn't match it yet; the work is listed under Deferred and
open. After the topics: what's decided for 0.4, test-drive findings the plugin
doesn't handle yet, and what's deferred or still open. Names are in `NAMES.md`;
the working rules are in `CLAUDE.md`. When something changes, edit its line
here; don't add a dated entry.

## Plugin shape

- The plugin targets Cowork and chat, not Claude Code. No Code-only paths.
- No `userConfig`: its prompts work only in Claude Code, and chat and Cowork
  have no plugin settings layer. Settings live in the plugin's own files.
- `ntm-user` is a plugin with two skills, `ntm-user:settings` and
  `ntm-user:style`. Secrets live in it, so it stays private.
- `ntm-user` is built from a guide the user's agent follows, not from templates.
  Its version is `1.<YYYYMMDD>.<HHMM>`.
- Only `settings` builds `ntm-user.plugin`. `configure` and the `configure-*`
  skills return their section text to it.
- `configure` is setup; `settings` is seeing or changing values after setup.
- A skill that hands work to an agent does the work itself when the agent isn't
  loaded, by reading `agents/<name>.md` from the installed plugin. Chat ignores
  agents, and whether they load in scheduled runs is unconfirmed.
- No hidden skills (`user-invocable: false`): as far as the docs say, they work
  only in Claude Code.
- Skill descriptions never contain angle brackets; the uploader rejects them.
- Backend guides are plain reference files, never skills. No skill per service,
  no plugin per backend.
- Renaming ntm to the user's own word: one sentence in the README and `help`,
  "fork and rename with your agent". `configure` doesn't ask.
- `help` reads the installed README. The README is the one text, with the origin
  story and price watch as the bridge for the impulse to buy.
- Decided, to build: the displayName and the README's title are
  `Neurodivergent Task Manager`, without "(ntm)".
- Publishing to the directory waits for the test-drives. Keep `ntm` ready: a
  README of 40+ words, LICENSE, icon, author, homepage, repository, no
  credentials, no brand names. The name similarity check happens only at
  submission.

## Settings and databases

- What the user writes goes in `ntm-user`. What jobs write at run time goes in
  databases on the todo list.
- Rules live in `conventions`, values in settings, tool calls in the backend
  guides.
- Settings are free text under fixed headings, read by heading. A missing
  section means its defaults. Deviations hold anything the user does
  differently; read last, they override. The headings are internal.
- Notifications holds the channel, the keys, and free-text policy that `notify`
  follows.
- Whether the style exists is the switch for styled messages; there is no on/off
  setting.
- `conventions` has no `Version:` or `Template source:` line; nothing read them.
- On main, whose tasks count is a setting (`Your tasks`). Decided, to build:
  every task on the list is the user's; a shared list goes in Deviations.
- Decided, to build: About you drops `Name`. Setup fills `Timezone` and
  `Country and currency` from the current timezone and asks the user to confirm.
- Decided, to build: one `Labels` list for tasks and projects. Linear passes a
  project's label to its tasks by name, so the guide says a project label needs
  the same name.
- A database is a document in the backend; where the backend has no documents, a
  task's description. Titles carry no prefix. The pause schedule is the pauses
  database. The shopper's comment on a task isn't a database. Main's plugin text
  calls databases "notes"; decided, to build: "database" everywhere (read
  database, write database).
- On main, each database's title is a setting (`Notes`) and how much message
  history to keep is that database's `Keep:` line. Decided, to build: the plugin
  fixes the titles and a rename goes in Deviations; `Keep:` moves into the
  message history database's frontmatter.

## Agents

- Agents own their procedures. The reminder skills gather facts and hand them
  off.
- An agent can't start another agent, so the planner is merged into `plan`.
- The estimator owns estimates, time guesses, explaining the ways to estimate,
  and review with the task review log. It never plans. Planning and other
  callers engage it; several callers is right.
- Decided, to build: the estimator's `Estimate a task` and `Time tasks` become
  one `Estimate` request, for one or many tasks, size or time.
- With no estimate field, the estimate goes in the task description.
- The messenger never reads settings; the skill that asks hands it the reminder,
  the job, the facts and any setting it needs. Its inputs are a contract
  (required and optional), and a missing required one comes back as
  `Messenger NEEDS`. Wording Deviations reach it only when a caller hands them
  in. It reads only the task-wording section of `conventions`, loads
  `ntm-user:style`, and sends through `notify`. When the style returns no title,
  it asks the style once more.
- The shopper owns its brief. It gets a task id and today's date only.

## Notifications

- No skill but `notify` sends anything; the messenger sends through it.
- `configure-notifications`: the channel, the keys, one test push with explicit
  keys, then an open question about notification policy. A re-run shows and
  asks.
- On the Claude channel, jobs are created with push on, and the run's summary is
  the reminder. Reminders run from chat get no special case. The channel value
  stays `claude-push`.
- Channel caps live in `notify`, and the messenger carries no channel rules. On
  Pushover, a message or title over the cap isn't trimmed or sent: `notify`
  returns `Notify TOO LONG` with the cap and why, and the caller shortens once.
  The Claude channel has no cap.
- `Pushover user key` lives in settings. Decided, to build: `Pushover app token`
  in settings is the default, for one generic app; a job can carry its own app
  token in its prompt, which overrides it and is handed to `notify`.

## Backends

- Shipped backend guides live in `conventions/references/<backend>.md`. Any
  other backend is described by the user under Todo list and smoke-tested
  against the contract; it can be built on anything, a Claude Doc for example.
- ntm bundles no Linear server. Setup has the user add Linear from the
  Connectors tab in Claude's settings.
- Backend guides leave how to call a tool to the connector's own instructions; a
  guide says which tool does each operation and which values go where.
- Backend guides own their setup.
- Setup asks the Linear team's estimate type; the connector can't read it.
- `configure-todo-list` picks the backend, collects what it needs, and checks or
  creates statuses, labels and databases. No `--test`: checks belong to
  `ready-check` and `self-test`.
- Todo list keeps `Backend`, `List name` and `List id`. On main it also has
  `Task prefix` and `Statuses`. Decided, to build: both go. Style examples use a
  generic `ABC-12`. Status classes are read from the backend's status types;
  blocked is a status named Blocked by default, and anything else goes in
  Deviations.
- Decided, to build: parent auto-close lives in `configure-todo-list`'s backend
  reference. The Linear guide suggests turning on Linear's Parent auto-close; a
  backend built on the contract asks the user.

## Planning and reports

- Planning in chat asks only when the request is ambiguous.
- Pausing a day that already holds planned work clears those dates and replans
  the rest of the week with the user.
- A report span is a number of days ending today. "Last month" is as many days
  as the previous calendar month had.
- Decided, to build: `Rhythm`, `Planning days`, `Plans ahead` and
  `A day's worth` leave settings for the job prompts, which `configure-schedule`
  writes with the user. `plan` keeps defaults for chat.
- Decided, to build: `plan --auto` takes the range in words (`week mon-fri`,
  `all weekdays this month`) and works out the days; it needn't be perfect.
- Decided, to build: `Never picks` becomes
  `Excluded labels from automatic scheduling`, labels only. Never planning a
  blocked task is a fixed rule in `conventions`.
- Decided, to build: nothing about parents or deadlines. No `Parents` key, no
  "plan the sub-tasks, never the parent", no "a parent's own date means
  nothing". `fix-todo-list` stops closing finished parents and only clears stale
  planned dates, or with `--dry-run` reports what it would clear.
- Decided, to build: the long "today" and timezone definitions across skills are
  cut, the Linear queries do no timezone math, and job prompts state the
  timezone.

## Jobs and scheduling

- A job is a three-line prompt that only loads a skill, written once in
  `configure-schedule`. Decided, to build: the prompt also carries the job's own
  settings (its planning, the weekly message, the timezone, and optionally a
  Pushover app token).
- On main, `configure-schedule` walks fixed job kinds (want it? days? time?
  title?) with defaults: morning weekdays 09:00, afternoon 14:30, evening 19:30,
  weekly planning Sunday 22:00, price watch daily 07:00 only if it's on,
  completed off. Main matches notifications and tokens on the default titles.
- Decided, to build: no fixed job kinds and no `Completed` kind.
  `configure-schedule` works out with each user what schedule they want and
  builds jobs from the skills. Before creating anything it shows a short table
  (job, days, time, title) for the user to approve or change. Titles are chosen
  live; internal matching keys off skill names, never titles.
- Decided, to build: no `weekly-planning` skill. The suggested weekly pattern is
  `show-completed <range>`, then `fix-todo-list`, then `plan --auto <range>`.
- Jobs are turned off and on, never "paused".
- A new job takes the creating chat's model, which can be the heaviest one, so
  `configure-schedule` asks once which model the jobs run on, suggests a lighter
  one such as Opus or Sonnet, and sets the user's choice with `update_trigger`.
- `configure` order: About you, todo list, notifications, style, schedule.
  `configure` writes nothing itself and ends by suggesting `/ntm:self-test` in a
  new chat. Decided, to build: the part name `todo list` becomes `todo-list`.
- `self-test`: `ready-check`, then a throwaway task and database, one line per
  step, ending `Self-test OK` or `Self-test FAILED at <step>`. Once the user
  starts it, it runs without asking; never run it unasked, since it sends a push
  and writes a task.
- The price watch job runs daily; pause days (from `pause`) don't skip it.

## The style

- No shipped personas. `configure-style` is a builder; "just remind me" means
  plain.
- A user's own persona goes in word for word under a `## For ntm` shim.
- The plugin defines no tone ladder; the user's style sets its own levels, and
  the harder-each-day rule climbs whatever levels the style has.
- Motifs rest for 20 messages by default.
- A day of reminders follows an episode arc: setup, middle, resolution, recap,
  credits.
- A title is part of the message's theme, never the reminder's name.
- Justin's own persona skill never ships.
- The profile's headings stay as on main. Decided, to build: `Off limits` is
  removed from the profile and the builder never asks about it, in Justin's
  style too.

## Price watch

- On main, price watch is on exactly when Todo list names a project, and the
  watch uses the project label only. Decided, to build: `Price watch project`
  goes; watched items are found by the $price-watch label, which tasks inherit
  from the project. Price watch is off when nothing carries it or the job isn't
  scheduled.
- Deal details go in the run's final reply, not in a separate post.
- Decided, to build: `Condition`, `Delivery` and `A deal` leave Shopping; they
  belong to each item, on its task. `Amazon interface` stays, and is left out
  entirely when the user doesn't want Amazon.
- Decided, to build, as a 0.3 bug fix: no Amazon alert steps database.
  `sync-price-watch-to-amazon` carries the steps itself, and is updated when
  Amazon changes. The steps already learned, in that database on Justin's
  Linear, are copied into the skill.

## Estimates and review

- Setup asks how the user estimates tasks and offers to explain. On Linear,
  their scale maps onto the team's points.
- Decided, to build: one key, `Estimate pattern`, says how the user sizes things
  and what to do with it, any mapping included. It replaces `Estimate scale` and
  `Estimate mapping`. `Estimate help` goes: what the user has been told belongs
  in the agent's memory, not in settings.
- "Estimate" is the plain word; no "sizing", no "groomed size".
- Review runs in chat only, never in a job.

## Words

The text rules in `CLAUDE.md` apply; these add to them.

- "Todo list", never "board".
- The product is "ntm" in prose. A file that abbreviates defines it at first
  use, "Neurodivergent Task Manager (ntm)", then ntm. No undefined abbreviations
  in docs.
- "Job" is defined in the vocabulary, and its definition avoids "task".
- Never say "trigger", "routine" or "cron job" to the user.
- In plugin text, `$` in front of a label (`$no-autoschedule`) marks a name the
  user configures: use its real name from Labels, and never show the `$` to the
  user. Such names are written bare, not in backticks. Plugin and skill names
  never take a `$`.
- Internal lines (status, delivery, result) never reach the user as they are;
  anything a user reads is plain words. Their names don't need Justin's yes.

## The repo

- devbox provides Node, and direnv turns it on in the repo. The Makefile is the
  way in: `make lint` and `make fix` run the npm scripts, and install the
  linters only when `package-lock.json` changes. `make test` runs bats on
  `tests/`: the user-facing name tests, against `tests/expected/`. bats and jq
  come from devbox, not node. CI runs lint through npm directly, and `make test`
  through `devbox run test` in `test.yml`.
- Line length: Prettier wraps prose, markdownlint holds fenced code blocks to 80
  columns, and tables are exempt (the rule is in `CLAUDE.md`'s Lint). Justin
  declined `stern` and any change to the prose limit.
- Lock files are generated: `.gitattributes` marks `*.lock` and
  `package-lock.json` `linguist-generated=true`, so GitHub collapses them in
  diffs. Justin's rule for all his repos: a new kind of lock file gets a line
  there.
- History was rewritten on 2026-11-07 to take a leaked address out of commit
  metadata. A clone from before then is stale; re-clone. GitHub Support has a
  ticket to purge the old pull request refs; nothing to do unless they ask.
- The branch `plugin-history-2026-11-06` keeps the history from before the 0.3
  squash.

## Justin's installed copy

ntm 0.3.0 and its ntm-user, five jobs on Opus. Its settings use old names
(Ticket prefix, Week ahead, grooming log), so the next release needs a fresh
setup.

His jobs, for that setup: the weekly planning plans weekdays; the morning plans
today if it's empty and not paused. Both aim for an hour or less where they can,
without ruling out bigger tasks; a bigger task is the signal to break it up.

## 0.4: decided

The v0.4 branch and git history keep the raw material, including the old 0.4
design page. Here "the base" is the published plugin and "the user plugin" the
generated one, which 0.4 names `ntm`.

- The base is `neurodivergent-task-manager` (published; commands autofill, so
  the length costs nothing). The user plugin is `ntm`, a fixed name so the base
  can always reach the contracts. An optional alias plugin's name is the user's
  word; there is no setting for it.
- Every job and every command the user types starts in the user plugin, setup
  included, so a user with an alias never types the base's name.
- `setup` and `update` are ways into `configure`, which absorbs showing and
  changing settings, and upgrades. The base has no `settings` skill.
- Contracts in the user plugin: `todo-list` (the backend guide), `ready-check`
  (only in the user plugin) and `self-test`. Both self-tests keep the name
  `self-test`. The old design page also lists `settings` and `style` as
  contracts; that isn't credited to Justin.
- The base is a guide the user's agent follows. Only contract names and call
  shapes are fixed.
- The user plugin's `notify` carries the user's Pushover-or-chat choice.
- The generated user plugin bundles the connector for the user's backend. Which
  Linear wins at first run is open (see Deferred and open).
- Plugin and file renames stay separate from content renames.
- No migration from 0.3; installs start fresh. The base and the user plugin
  update together.
- Publishing adds: the base self-test passes with no user plugin installed;
  `configure` never sends or creates without being asked; a privacy page; the
  name check for `neurodivergent-task-manager`; the published release is
  identifiable. The old wording, "`Template source:` points at a release", named
  a line #19 removed from `conventions`, so how the release is identified is
  open.

## Test-drive findings

Not handled by the plugin yet.

- Whether agents load in scheduled runs is unconfirmed. The read-the-file
  fallback covers it until then.
- An imported persona may carry its own history instructions and double-write
  the message history database. Watch real runs.
- The accept card for `ntm-user.plugin` in chat is untested.
- Installing through Chrome: `file_upload` rejects `/mnt/user-data/outputs/`; a
  path under the working directory works.

## Deferred and open

### To build, from the names pass

Each is decided (see its topic above). Justin places each in 0.3 or 0.4; only
the first is placed.

- 0.3, a bug fix: remove the Amazon alert steps database and copy the learned
  steps into `sync-price-watch-to-amazon`.
- Release: blank. The displayName and README title without "(ntm)", and every
  abbreviation defined at first use.
- Release: blank. Settings: drop `Name`, `Task prefix`, `Your tasks`,
  `Statuses`, `Price watch project`, `Notes`, `Parents` and `Estimate help`; one
  `Labels` list; `Estimate pattern`;
  `Excluded labels from automatic scheduling`; setup fills `Timezone` and
  `Country and currency` and confirms.
- Release: blank. Status classes from the backend's status types; blocked as a
  fixed rule in `conventions`.
- Release: blank. Job prompts carry the planning, the weekly message, the
  timezone and an optional app token; `notify` takes a job's app token.
- Release: blank. `configure-schedule` builds jobs from the skills with each
  user: no fixed kinds or titles, a table to approve first, matching on skill
  names.
- Release: blank. Remove `weekly-planning`; the weekly job chains
  `show-completed`, `fix-todo-list` and `plan --auto`.
- Release: blank. `plan --auto` takes a range in words.
- Release: blank. Purge parents and deadlines; `fix-todo-list` only clears stale
  planned dates; parent auto-close moves to `configure-todo-list`'s backend
  reference.
- Release: blank. Cut the long "today" and timezone definitions; no timezone
  math in the Linear queries.
- Release: blank. Price watch finds items by the $price-watch label alone;
  `Condition`, `Delivery` and `A deal` move to each task; `Amazon interface`
  left out when the user doesn't want Amazon.
- Release: blank. Call the notes databases everywhere; fixed titles; `Keep:`
  into the message history database's frontmatter.
- Release: blank. One `Estimate` request to the estimator.
- Release: blank. Remove `Off limits` from the style profile and the builder.
- Release: blank. The `configure` part `todo list` becomes `todo-list`.

### Open

- An option, not decided: settings can live in a file in the user's backend (a
  Linear doc, for example), and the `settings` skill then only says where to
  find them. Some databases' own settings could live there too.
- A price watch talk, later: its default pattern makes too much busywork, the
  per-item details belong on the task, and setup needs better guidelines.
- Tasks that keep slipping never get a harder reminder: the style's history
  doesn't record task ids (review finding #3). Justin decides where this goes.
  Idea, big enough to wait for 0.4: planning owns a mention history database
  where each reminder records the date for every task it names; the caller
  passes each task's count through the messenger to the style, which only maps a
  count to a level; the weekly `fix-todo-list` keeps only ids still open, so any
  closed state drops out. JSON in a database is fine; a sqlite file would be the
  same thing, so revisit storage only if needed.
- Date-math edges in report spans ("last month" on the 1st): not worth fixing,
  since reports are for the typical flow. Someday, maybe: phrase spans as "since
  the last scheduled run".
- A reading-comprehension pass: writers simplify, human comprehension first ("if
  a human can comprehend, so can a model"). Includes the estimator's "Good
  enough reminders complete." and `weekly-planning`'s parenthetical about
  `fix-todo-list`'s result. Justin decides where this goes.
- Waiting for Justin, from the 2026-11-07 review:
    - Should the shopper price Amazon when Amazon alerts are off?
    - `self-test` claims every backend operation but skips comments, labels and
      agents: add the steps or narrow the claim?
    - Does showing a key's last four characters count as printing it? Are keys
      OK in the curl command in run transcripts?
- Not discussed yet: `fix-todo-list` fetches the whole closed history every
  week, a cost that grows. Proposed: only recent completions.
- 0.4 inputs, held for the 0.4 talks:
    - one home for the style's call contract (now inside settings' Regenerating)
    - each database's format created by the skill that owns it, not by setup
    - the plugin-locator globs in `help` and `conventions` break under the
      rename
    - the job-run block (ready check, FINAL REPLY, error handling, agent
      fallback) repeats across about 8 skills
    - the estimator's Review procedure could move into `review-todo-list`
    - `configure-todo-list` re-walks setup when reconfiguring
    - the `ntm-user` package layout isn't spelled out
- 0.4, open: the generated user plugin bundles the connector (decided above),
  but first-run setup needs Linear before the user plugin exists, so the user
  connects through the Connectors tab first, and a bundled server would be a
  second Linear. Decide which wins.
- Before 0.4: install main on Justin's account with a fresh setup and use it for
  a few days (see Justin's installed copy). His call, and only with his
  go-ahead.
- Revising the `/domain-first-design` skill and Justin's design agents, his
  tooling outside ntm: parked, tracked on his own list as GULU-314.
