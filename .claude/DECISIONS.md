# ntm decisions in force

What's decided and in force on main, by topic. A line marked "decided, to build"
is decided but main doesn't match it yet; the work is listed under Deferred and
open. After the topics: what's decided for 0.4, test-drive findings the plugin
doesn't handle yet, and what's deferred or still open. User-facing names are
held by `tests/expected/` (see `tests/README.md`); the working rules are in
`CLAUDE.md`. When something changes, edit its line here; don't add a dated
entry.

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
  agents. Scheduled runs load them and can start them.
- No hidden skills (`user-invocable: false`): as far as the docs say, they work
  only in Claude Code.
- Skill descriptions never contain angle brackets; the uploader rejects them.
- Backend guides are plain reference files, never skills. No skill per service,
  no plugin per backend.
- Renaming ntm to the user's own word: one sentence in the README and `help`,
  "fork and rename with your agent". `configure` doesn't ask.
- `help` reads the installed README. The README is the one text, with the origin
  story and price watch as the bridge for the impulse to buy.
- The displayName is `Neurodivergent Task Manager`, without "(ntm)". The
  README's title keeps "(ntm)", which defines it.
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
- Whether the style exists is the switch for styled messages.
- Every task on the list is the user's; a shared list goes in Deviations.
- About you holds `Timezone` and `Country and currency`. Setup fills them from
  the current timezone and asks the user to confirm.
- One `Labels` list for tasks and projects. Linear passes a project's label to
  its tasks by name, so the guide says a project label needs the same name.
- A database is a document in the backend; where the backend has no documents, a
  task's description. The pause schedule is the pauses database. The shopper's
  comment on a task isn't a database. "Database" everywhere: read database,
  write database.
- The plugin fixes each database's title, and a rename goes in Deviations. How
  much message history to keep is the `Keep:` line in the message history
  database's frontmatter.

## Agents

- Agents own the procedures that run without the user; a procedure that needs
  the user's answers lives in the chat skill that runs it (review). The reminder
  skills gather facts and hand them off.
- An agent can't start another agent, so the planner is merged into `plan`.
- The estimator owns estimates, time guesses and explaining the ways to
  estimate. It never plans. Planning and other callers engage it; several
  callers is right.
- Review and the task review log belong to `ntm:review-todo-list`; the estimator
  answers its Estimate requests.
- The estimator has one `Estimate` request, for one or many tasks, size or time.
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
- `Pushover user key` lives in settings. `Pushover app token` in settings is the
  default, for one generic app; a job can carry its own app token in its prompt,
  which overrides it and is handed to `notify`. `configure-notifications` offers
  a job's own app; `configure-schedule` writes the token into the job's prompt.

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
  creates statuses, labels and databases. Checks belong to `ready-check` and
  `self-test`.
- Todo list has `Backend`, `List name` and `List id`. Style examples use a
  generic `ABC-12`. Status classes are read from the backend's status types;
  blocked is a status named Blocked by default, and anything else goes in
  Deviations.
- Parent auto-close lives in the backend guide's setup. The Linear guide
  suggests turning on Linear's Parent auto-close; a backend built on the
  contract asks the user.

## Planning and reports

- Planning in chat asks only when the request is ambiguous.
- Pausing a day that already holds planned work clears those dates and replans
  the rest of the week with the user.
- A report span is a number of days ending today. "Last month" is as many days
  as the previous calendar month had.
- The job prompts carry the planning rhythm, the planning days, how far ahead to
  plan and a day's worth; `configure-schedule` writes those with the user.
  `plan` keeps defaults for chat.
- `plan --auto` takes the range in words (`week mon-fri`,
  `all weekdays this month`) and works out the days; it needn't be perfect.
- `Excluded labels from automatic scheduling` is labels only. Never planning a
  blocked task is a fixed rule in `conventions`.
- Planning has no rules for parents or deadlines: it treats every open task the
  same, and closing finished parents is the backend's job (Parent auto-close,
  above). `fix-todo-list` only clears stale planned dates, or with `--dry-run`
  reports what it would clear.
- Job prompts state the timezone. Skills carry no long "today" or timezone
  definitions, and the Linear queries no timezone math.

## Jobs and scheduling

- A job is a short prompt that only loads skills, written once in
  `configure-schedule`. The prompt also carries the job's own settings (its
  planning, the weekly message, the timezone, and optionally a Pushover app
  token).
- `configure-schedule` works out with each user what schedule they want and
  builds jobs from the skills. Before creating anything it shows a short table
  (job, days, time, title) for the user to approve or change. Titles are chosen
  live; internal matching keys off skill names, never titles.
- The suggested weekly pattern is `show-completed <range>`, then
  `fix-todo-list`, then `plan --auto <range>`.
- Jobs are turned off and on, never "paused".
- A new job takes the creating chat's model, which can be the heaviest one, so
  `configure-schedule` asks once which model the jobs run on, suggests a lighter
  one such as Opus or Sonnet, and sets the user's choice with `update_trigger`.
- `configure` order: About you, todo list, notifications, style, schedule.
  `configure` writes nothing itself and ends by suggesting `/ntm:self-test` in a
  new chat. The part names are one word each: `todo-list`, not `todo list`.
- `self-test`: `ready-check`, then a throwaway task and database, one line per
  step, ending `Self-test OK` or `Self-test FAILED at <step>`. Once the user
  starts it, it runs without asking; never run it unasked, since it sends a push
  and writes a task.
- `self-test` also writes and updates a comment, adds and removes a label, and
  asks the estimator for a time guess, which only reads. With no agent loaded it
  follows `agents/estimator.md` itself and says so.
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
- The profile's headings stay as on main. The profile has no `Off limits`, and
  the builder never asks about it, in Justin's style too.
- The style records, in the message history, the task ids each message names; a
  carried-over task's level comes from counting the earlier days that name it.

## Price watch

- Watched items are found by the $price-watch label, which tasks inherit from
  the project. Price watch is off when nothing carries it or the job isn't
  scheduled.
- Deal details go in the run's final reply, not in a separate post.
- Each watched task's description says its condition, how it reaches the user
  and what counts as a deal, in the user's words. The shopper's defaults fill
  what it doesn't say: new; ordered online and delivered to the user's country;
  at or near the target, or well below the usual price. The $price-watch label
  in `conventions` says how to write one.
- Shopping holds `Amazon interface` and anything else about how the user shops.
  The line is left out when the user doesn't want Amazon alerts, and the section
  when nothing is left in it.
- Amazon alerts are on when `Amazon interface` names a browser or is blank;
  they're off when the line is missing or says off, or there's no Shopping
  section.
- With Amazon alerts on, the shopper leaves Amazon to them. With them off, it
  tries Amazon like any other store, reading the setting itself. When it can't
  read Amazon's page, it drops Amazon silently: never a problem, a failure or a
  mention to the user.
- No Amazon alert steps database. `sync-price-watch-to-amazon` carries the steps
  itself, and is updated when Amazon changes.

## Estimates and review

- Setup asks how the user estimates tasks; it explains the ways to estimate only
  when the user asks for more. On Linear, their scale maps onto the team's
  points.
- One key, `Estimate pattern`, says how the user sizes things and what to do
  with it, any mapping included. What the user has been told about estimating
  belongs in the agent's memory, not in settings.
- The plain words are "estimate" and "breaking up a task".
- Review runs in chat only, never in a job.

## Words

The text rules in `CLAUDE.md` apply; these add to them.

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

- devbox provides prettier, markdownlint-cli2, direnv, bats and jq. `make lint`,
  `make lint-fix` and `make test` are the way in, locally and in CI.
- `make test` runs the bats tests in `tests/`: the user-facing name tests,
  against `tests/expected/`, which only Justin edits.
- `make lint` also enforces the hard line cap, ABSOLUTE_MAXIMUM_LINE_LENGTH
  (145, exported in `.envrc`), on every tracked file except those
  `.gitattributes` marks `skip-absolute-line-length`, and prints the files that
  break it.
- Line length: Prettier wraps prose, markdownlint holds fenced code blocks to 80
  columns, and tables are exempt (the rule is in `CLAUDE.md`'s Lint). Justin
  declined `stern` and any change to the prose limit.
- Lock files are generated: `.gitattributes` marks `*.lock` and
  `package-lock.json` `linguist-generated=true`, so GitHub collapses them in
  diffs. Justin's rule for all his repos: a new kind of lock file gets a line
  there.
- The branch `plugin-history-2026-11-06` keeps the history from before the 0.3
  squash.

## Justin's installed copy

- **Current Installed Version**: ntm 0.3.2
- **Last rebuilt on**: 2026-11-08 (bcf91a9)
- **Jobs**: five, on Opus, re-synced 2026-11-08
- **Next install**: once it includes #51, rerun `/ntm:configure-style` for his
  persona style

His jobs, for the next fresh setup: the weekly planning plans weekdays; the
morning plans today if it's empty and not paused. Both aim for an hour or less
where they can, without ruling out bigger tasks; a bigger task is the signal to
break it up.

## 0.4: decided

The build plan is `.claude/plans/0.4-build-plan.md`; the v0.4 branch and git
history keep the raw material. Here "the base" is the published plugin and "the
user plugin" the generated one. Justin reshaped 0.4 on 2026-11-08.

- No rename. The base stays `ntm` and the user plugin stays `ntm-user`, the one
  setup generates, holding only what's tailored to this user. An alias plugin
  isn't planned: with no entry skills it has nothing to alias (the plan
  recommends dropping it; his call).
- Day-to-day commands are base skills, called directly: `/ntm:today`,
  `/ntm:plan`, `/ntm:pause`, and so on. There are no entry skills anywhere.
  Users rarely type commands; their jobs do most of the calling, and a job's
  prompt loads `ntm:<skill>`. Base skills keep their full descriptions.
- `ntm-user:backend` is the one place that teaches how to work with this user's
  list: their backend's calls, their labels and statuses, what counts as open,
  their databases. It is the list rules and the backend guide, tailored to this
  user only. It takes a request in plain words ("today's open items",
  "everything done last week", "watched items") and gives the call to make; the
  agent makes it.
- Base skills say WHAT to do and ask `ntm-user:backend` for the data:
  `ntm:today` is "get today's open items from `ntm-user:backend`, then present
  them". Planning, the reminders and the price watch all go through it. Future
  recurring items show up in "today's open items" the same way.
- There is no base conventions skill. The generic text (the list rules, every
  backend guide, each feature's rules) stays in the base only as setup reference
  files that the build reads to write `ntm-user:backend`. A rule fix reaches
  users through `update` and a rebuild, not a base patch. Tokens matter most.
- The hard rule: no day-to-day run loads text about a path the user isn't set up
  for (another backend, a feature they didn't pick). Text a base skill needs for
  one feature lives in a reference that only that feature's runs load.
- The user plugin holds `backend`, `notify` (only their channel), `ready-check`
  (names no backend; a sign-in failure comes from `backend`'s ping) and
  `settings`, plus the Linear connector for Linear users. It has no `style` and
  no `self-test`: the base's `style` and `self-test` serve everyone.
- The base's entry points are `setup`, a wizard that walks the whole flow (see
  0.4: setup), and a tiny `update` whose body loads `setup`, there so someone
  already set up finds it; run before any setup, it asks "It doesn't look like
  you've run setup before, do you want to?" The `configure` skills go away, and
  so do the base's `conventions`, `settings`, `notify` and `ready-check`, their
  text moved under setup as the build's source.
- `update` reads per-version reference files of what changed, picked by the user
  plugin's `major.minor`, and offers what's new, new features included.
- The user plugin's `major.minor` mirrors the base's; its patch is its own, a
  count of the user's rebuilds. Its generation time is a field in its
  `plugin.json`, and `ntm-user:backend` opens with a Built line naming the
  versions, backend, channel and features.
- Values setup collects live in the backend, in the `Settings` document. About
  you, Planning, Shopping and Notifications are read live; Labels and Deviations
  are built into `ntm-user:backend`, so changing one means `update` rebuilds.
- `ntm-user:settings` shows the user their settings on request and points the
  agent to the right place for a change: the Settings document, a scheduled task
  through `ntm:schedules`, the Style document through `ntm:style`, or a built-in
  value through `update`. It never rebuilds.
- The persona's Profile lives in the `Style` document on the backend. The style
  procedure is the base skill `ntm:style`, which reads it (tentative: one extra
  document read per message; the fallback is copying the persona into the user
  plugin at build). The base reference `style/references/persona-contract.md`
  gives the Style document's required and optional sections, settled from
  `.claude/drafts/persona-breakdown.md`; Justin reviews it on its PR.
- No skill for any job, under any name. Jobs are composed from skills however
  the user wants. The suggested weekly job: `show-completed` for the span just
  past, `fix-todo-list`, `plan --auto` for the next span, then one message. Each
  step is a base skill, so fixes reach everyone.
- `schedules` manages the jobs, a base skill called as `/ntm:schedules`. It
  checks which scheduled tasks exist and belong to ntm. With none, it walks the
  user through setting them up. With `--setup "<their schedules>"`, it creates
  the jobs from that text. Each job's prompt carries the job run block (ready
  check, final reply, error handling). The scheduled tasks are the source of
  truth, and a change to a job edits its scheduled task directly.
- The Settings document holds no schedules. The schedules and the jobs' model go
  in setup's handoff prompt (0.4: setup, step 9). Nothing in Settings marks a
  job off, and nothing compares the jobs against Settings.
- Each database is created by the skill that owns it, the first time it writes.
  Setup creates only Settings and Style, and confirms the names of the rest. The
  pauses database is its own document, titled `Paused dates`, with a line
  explaining what it holds.
- Pushover keys: working default, the user key and default app token in the
  Settings document, and a job's own app token in that job's prompt. Not
  strongly held.
- The base is a guide the user's agent follows. Only contract names and call
  shapes are fixed.
- The generated user plugin bundles the connector when the user is on Linear.
  Setup has already connected it and tested it at the todo list step, before the
  plugin is built. A duplicate Linear connection isn't designed for; the agent
  that hits one handles it.
- Parents and sub-tasks are the backend's task hierarchy, and their words stay.
- Plugin and file renames stay separate from content changes.
- No migration from 0.3; installs start fresh. The base and the user plugin
  update together.
- 0.4 is built on the integration branch `release-0.4`, which has main's
  required checks. 0.4 PRs target it; main stays installable as 0.3.
- Every 0.4 PR is intentional, targeted, human-knowable and maintainable, with
  one concern a person would name as a change, never a technical slice: mostly
  under about 100 changed lines, in 1 to 5 files.
- Publishing adds: the base self-test passes with no user plugin installed;
  `setup` never sends or creates without being asked; a privacy page; the
  published release is identifiable. How the published release is identified is
  open.

## 0.4: setup

Walked through with Justin on 2026-11-08. A new user ends with the same shape
and function as his setup, built from their own choices: a connected todo list,
a persona, the features they picked running as jobs, reminders on their phone,
and a passing self-test.

Setup asks one question at a time, conversationally, never a list to answer. It
front-loads the back-and-forth so the build runs without stopping. It saves at
the end of each area (the todo list, the persona, task management, price watch,
notifications), values and assets together, without asking, unless the user
would rather save each piece. In order:

1. **Intro.** One short text: what ntm is and where it came from, what it does,
   why the persona matters, and that setup takes 20 to 60 minutes and then
   mostly runs itself. Draft: `.claude/drafts/setup-intro.md`; ntm says "I", and
   Justin is "my creator". It ends by confirming the timezone.
2. **The todo list.** Suggest a free Linear account, and help create it and
   connect it; the connector is checked right then. Someone who doesn't want
   Linear hears it'll take longer to find something, and that you're happy to:
   the agent reads the backend contract and searches with them until they're
   content, always offering to build the list inside Claude (an artifact or a
   Claude Doc that holds the data) or to find an existing tool. Saving this area
   creates the Settings document.
3. **The persona.** Right after the list. Someone who doesn't want one gets
   pushed a little: without it, ntm is no different from Apple or Google
   reminders. Setup helps build one from generic parts, with no show or IP
   named, and with repetition guarded against. A good opener: "think about the
   formula of a show you enjoy, where they can snap back at you when you need
   it, or celebrate you when you've earned it". The parts, from Justin's own
   persona: `.claude/drafts/persona-breakdown.md` (not yet reviewed by him).
   Saving this area writes the Style document, in the sections the persona
   contract requires.
4. **Features.** A numbered list to pick from, everything or a subset: day to
   day task management (things you want or need to do), and price watch (things
   you want to buy, without buying on impulse). New functionality joins this
   list, and `update` offers it to existing users.
5. **Each picked feature, in turn.**
    - Task management: the schedule, suggesting Monday to Friday for doing
      things and Sunday for cleanup and planning the week ahead; then its
      labels, $pending-shipment included even without price watch (a task that
      can't happen until something arrives isn't scheduled automatically).
    - Price watch: country and currency; the schedule, Justin's as the default;
      its labels; then whether to set up Amazon sync, explaining that cloud
      agents can't reach Amazon, so this works around it. A no skips the Amazon
      labels too.
    - Saving each feature's area saves its labels and other values to the
      Settings document. Its schedules go in the handoff prompt (step 9).
6. **The jobs' model.** Suggest a lighter model than the one running setup,
   worded so any AI provider works; never only Claude models. It goes in the
   handoff prompt with the schedules.
7. **Notifications.** For a separate app on their phone or computer, strongly
   suggest Pushover, which their phone's focus settings can treat differently;
   otherwise the AI app's own push. A job's own Pushover app (its own sound)
   isn't asked; it goes in the Pushover reference.
8. **Databases.** Confirm the names of the ones their features need. On Linear,
   say they live at Linear's base location and which document holds which
   database. Elsewhere, the agent works it out. Setup creates only Settings and
   Style; each other database is created by its owner skill on its first write.
9. **The build.** Say what's about to happen and wait for a green light, leaving
   room for anything else they want to say. Then narrate each step: create their
   plugin, install it, hand off. Setup ends with one handoff prompt, the same
   text whether a subagent gets it or the user pastes it into a new chat: "I
   just set up ntm and need you to run tests and finish the setup. Run
   `/ntm:self-test`. If it passes, set up the schedules:
   `/ntm:schedules --setup "<schedules and model>"`". Setup gives it to a
   subagent first, since a new plugin may only load in a fresh session. If that
   fails, the user pastes it into a new chat, or setup drives their browser, but
   only when it has browser access.
10. **The end.** A passing self-test sends a success message in their persona,
    said in chat and sent as a push. Then `schedules --setup` creates the jobs.
    The self-test's own push can be fun too. Making people smile is good.

Estimating isn't part of setup: it's asked the first time they review.

## Test-drive findings

Not handled by the plugin yet.

- An imported persona may carry its own history instructions and double-write
  the message history database. Watch real runs.
- The accept card for `ntm-user.plugin` in chat is untested.
- Installing through Chrome: `file_upload` rejects `/mnt/user-data/outputs/`; a
  path under the working directory works.

## Deferred and open

### Start here (2026-11-08)

The 0.4 build plan: `.claude/plans/0.4-build-plan.md`, reshaped on 2026-11-08:
no rename, no entry skills, no base conventions skill, and `ntm-user:backend` as
the one place that knows the user's list (0.4: decided). Next: Justin reads the
plan's "For the owner" choices, then its PR sequence on `release-0.4`, wave 1
first.

### Future work

After the planned 0.4 work, as 0.4 patch releases:

- Evening reminder: if everything was done by the afternoon reminder and nothing
  changed since (the same tasks done, nothing new, nothing open), skip the push.
- Weekend reminders that work differently: no automatic planning, only tasks
  planned for that day. With nothing planned, the day counts as paused and
  nothing is sent. A task added for that day still gets reminders: the afternoon
  reminds, the evening reports.

Likely 1.1:

- Recurring reminders at an interval (pet care, medicine, anything). Not planned
  automatically; the next date follows from when it was last done, so a missed
  day shifts the interval. Needs the weekend reminders.

Release: when 0.4 is complete on `release-0.4`, it merges into main and the
version is tagged on main.

### Open

- A price watch talk, later: its default pattern makes too much busywork, and
  setup needs better guidelines.
- Slipping tasks, a 0.4 idea: move the counting out of the style. Planning owns
  a mention history database where each reminder records the date for every task
  it names; the caller passes each task's count through the messenger to the
  style, which only maps a count to a level; the weekly `fix-todo-list` keeps
  only ids still open, so any closed state drops out. JSON in a database is
  fine; a sqlite file would be the same thing, so revisit storage only if
  needed.
- Date-math edges in report spans ("last month" on the 1st): not worth fixing,
  since reports are for the typical flow. Someday, maybe: phrase spans as "since
  the last scheduled run".
- A reading-comprehension pass: writers simplify, human comprehension first ("if
  a human can comprehend, so can a model"). Includes the estimator's "Good
  enough reminders complete." Justin decides where this goes.
- An idea, later: the estimator takes the task review log over from
  `ntm:review-todo-list` as its own database and keeps its `## How you work`
  tidy (folds and rewrites entries); `fix-todo-list` asks the estimator to do
  that and never edits the log itself.
- Not discussed yet: `fix-todo-list` fetches the whole closed history every
  week, a cost that grows. Proposed: only recent completions.
- 0.4 inputs; the build plan places each:
    - one home for the style's call contract (now inside settings' Regenerating)
    - `help` finds the newest installed copy when several sit side by side
    - the job-run block (ready check, FINAL REPLY, error handling, agent
      fallback) repeats across about 8 skills
    - the `ntm-user` package layout isn't spelled out
- Before 0.4: install main on Justin's account with a fresh setup and use it for
  a few days (see Justin's installed copy). His call, and only with his
  go-ahead.
