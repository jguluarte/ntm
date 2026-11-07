# ntm decisions in force

What's decided and in force on main, by topic. After the topics: what's decided
for 0.4, test-drive findings the plugin doesn't handle yet, and what's deferred
or still open. Names are in `NAMES.md`; the working rules are in `CLAUDE.md`.
When something changes, edit its line here; don't add a dated entry.

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
- Publishing to the directory waits for the test-drives. Keep `ntm` ready: a
  README of 40+ words, LICENSE, icon, author, homepage, repository, no
  credentials, no brand names. The name similarity check happens only at
  submission.

## Settings and notes

- What the user writes goes in `ntm-user`. What jobs write at run time goes in
  notes on the todo list.
- Rules live in `conventions`, values in settings, tool calls in the backend
  guides.
- Settings are free text under fixed headings, read by heading. A missing
  section means its defaults. Deviations hold anything the user does
  differently; read last, they override.
- Notifications holds the channel, the keys, and free-text policy that `notify`
  follows.
- Whose tasks count is a setting.
- How much message history to keep is the note's own `Keep:` line, not a
  setting.
- Note titles carry no prefix. A note is a document in the backend; where the
  backend has no documents, a task's description. The pause schedule is the
  pauses note.
- Whether the style exists is the switch for styled messages; there is no on/off
  setting.
- `conventions` has no `Version:` or `Template source:` line; nothing read them.

## Agents

- Agents own their procedures. The reminder skills gather facts and hand them
  off.
- An agent can't start another agent, so the planner is merged into `plan`.
- The estimator owns estimates, time guesses, explaining the ways to estimate,
  and review with the task review log. It never plans.
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
  the reminder. Reminders run from chat get no special case.
- Channel caps live in `notify`, and the messenger carries no channel rules. On
  Pushover, a message or title over the cap isn't trimmed or sent: `notify`
  returns `Notify TOO LONG` with the cap and why, and the caller shortens once.
  The Claude channel has no cap.

## Backends

- Shipped backend guides live in `conventions/references/<backend>.md`. Any
  other backend is described by the user under Todo list and smoke-tested
  against the contract; it can be built on anything, a Claude Doc for example.
- ntm bundles no Linear server. Setup has the user add Linear from the
  Connectors tab in Claude's settings.
- Backend guides leave how to call a tool to the connector's own instructions; a
  guide says which tool does each operation and which values go where.
- Backend guides own their setup, and describe parent auto-close.
- Setup asks the Linear team's estimate type; the connector can't read it.
- `configure-todo-list` picks the backend, collects what it needs, and checks or
  creates statuses, labels and notes. No `--test`: checks belong to
  `ready-check` and `self-test`.

## Planning and reports

- Planning in chat asks only when the request is ambiguous.
- Pausing a day that already holds planned work clears those dates and replans
  the rest of the week with the user.
- A report span is a number of days ending today. "Last month" is as many days
  as the previous calendar month had.

## Jobs and scheduling

- A job is a three-line prompt that only loads a skill, written once in
  `configure-schedule`.
- `configure-schedule` walks each job kind (want it? days? time? title?) with
  defaults: morning weekdays 09:00, afternoon 14:30, evening 19:30, weekly
  planning Sunday 22:00, price watch daily 07:00 only if it's on, completed off.
  Titles and prompts belong to the user; main still matches on the default
  titles (`NAMES.md`, Q5).
- Jobs are turned off and on, never "paused".
- A new job takes the creating chat's model, which can be the heaviest one, so
  `configure-schedule` asks once which model the jobs run on, suggests a lighter
  one such as Opus or Sonnet, and sets the user's choice with `update_trigger`.
- `configure` order: About you, todo list, notifications, style, schedule.
  `configure` writes nothing itself and ends by suggesting `/ntm:self-test` in a
  new chat.
- `self-test`: `ready-check`, then a throwaway task and note, one line per step,
  ending `Self-test OK` or `Self-test FAILED at <step>`. Once the user starts
  it, it runs without asking; never run it unasked, since it sends a push and
  writes a task.
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

## Price watch

- Price watch is on exactly when Todo list names a project. The watch uses the
  project label only.
- Deal details go in the run's final reply, not in a separate post.

## Estimates and review

- Setup asks how the user estimates tasks and offers to explain. On Linear,
  their scale maps onto the team's points.
- "Estimate" is the plain word; no "sizing", no "groomed size".
- Review runs in chat only, never in a job.

## Words

The text rules in `CLAUDE.md` apply; these add to them.

- "Todo list", never "board".
- The product is "ntm" in prose.
- "Job" is defined in the vocabulary, and its definition avoids "task".
- Never say "trigger", "routine" or "cron job" to the user.
- In plugin text, `$` in front of a label (`$no-autoschedule`) marks a name the
  user configures: use its real name from Labels, and never show the `$` to the
  user. Such names are written bare, not in backticks. Plugin and skill names
  never take a `$`.

## The repo

- devbox provides Node, and direnv turns it on in the repo. The Makefile is the
  way in: `make lint` and `make fix` run the npm scripts, and install the
  linters only when `package-lock.json` changes. CI runs npm directly.
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
- displayName "Neurodivergent Task Manager", without "(ntm)".
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
  the message history note. Watch real runs.
- The accept card for `ntm-user.plugin` in chat is untested.
- Installing through Chrome: `file_upload` rejects `/mnt/user-data/outputs/`; a
  path under the working directory works.

## Deferred and open

- Next: the questions in `NAMES.md`, one at a time; then the rest of this
  section, as Justin picks.
- Tasks that keep slipping never get a harder reminder: the style's history
  doesn't record task ids (review finding #3). Justin decides where this goes.
  Idea, big enough to wait for 0.4: planning owns a mention history note where
  each reminder records the date for every task it names; the caller passes each
  task's count through the messenger to the style, which only maps a count to a
  level; the weekly `fix-todo-list` keeps only ids still open, so any closed
  state drops out. JSON in a note is fine; a sqlite file would be the same
  thing, so revisit storage only if needed.
- Per-reminder Pushover tokens don't work, and aren't built out yet:
  `configure-notifications` writes free text, and `notify` reads a fixed line
  format. Specific to Justin's own `ntm-user`. His idea: a dictionary in
  settings mapping each reminder to its token.
- Date-math edges in report spans ("last month" on the 1st): not worth fixing,
  since reports are for the typical flow. Someday, maybe: phrase spans as "since
  the last scheduled run".
- A reading-comprehension pass: writers simplify, human comprehension first ("if
  a human can comprehend, so can a model"). Includes the estimator's "Good
  enough reminders complete." and `weekly-planning`'s parenthetical about
  `fix-todo-list`'s result. Justin decides where this goes.
- Waiting for Justin, from the 2026-11-07 review:
    - About you's Name and Planning's Parents are collected, but nothing reads
      them: wire them in or drop them?
    - Should the shopper price Amazon when Amazon alerts are off?
    - `self-test` claims every backend operation but skips comments, labels and
      agents: add the steps or narrow the claim?
    - Does showing a key's last four characters count as printing it? Are keys
      OK in the curl command in run transcripts?
    - #15 said only `plan` asks the estimator, and nothing everyday does. On
      main, `plan --auto day` asks it (Time tasks) on mornings with nothing
      planned, and `configure-todo-list` and `review-todo-list` ask it too. Does
      the rule still stand, and what does it cover?
- Not discussed yet: `fix-todo-list` fetches the whole closed history every
  week, a cost that grows. Proposed: only recent completions.
- 0.4 inputs, held for the 0.4 talks:
    - one home for the style's call contract (now inside settings' Regenerating)
    - each note's format created by the skill that owns the note, not by setup
    - the plugin-locator globs in `help` and `conventions` break under the
      rename
    - the job-run block (ready check, FINAL REPLY, error handling, agent
      fallback) repeats across about 8 skills
    - `plan --auto week` does three jobs: report, tidy, plan
    - the estimator's Review procedure could move into `review-todo-list`
    - `configure-todo-list` re-walks setup when reconfiguring
    - the `ntm-user` package layout isn't spelled out
    - `configure`'s part names are spelled inconsistently (`about-you`,
      `todo list`)
- 0.4, open: the generated user plugin bundles the connector (decided above),
  but first-run setup needs Linear before the user plugin exists, so the user
  connects through the Connectors tab first, and a bundled server would be a
  second Linear. Decide which wins.
- Before 0.4: install main on Justin's account with a fresh setup and use it for
  a few days (see Justin's installed copy). His call, and only with his
  go-ahead.
- Revising the `/domain-first-design` skill and Justin's design agents, his
  tooling outside ntm: parked, tracked on his own list as GULU-314.
