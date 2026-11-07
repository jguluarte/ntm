# ntm decisions in force

What's decided and in force on main, by topic. Names are in `NAMES.md`; the
working rules are in `CLAUDE.md`. When something changes, edit its line here;
don't add a dated entry.

## Plugin shape

- The plugin targets Cowork and chat, not Claude Code. No Code-only paths.
- No `userConfig`. Settings live in the plugin's own files.
- `ntm-user` is a plugin with two skills, `ntm-user:settings` and
  `ntm-user:style`. Secrets live in it, so it stays private.
- `ntm-user` is built from a guide the user's agent follows, not from templates.
  Its version is `1.<YYYYMMDD>.<HHMM>`.
- Only `settings` builds `ntm-user.plugin`. `configure` and the `configure-*`
  skills return their section text to it.
- `configure` is setup; `settings` is seeing or changing values after setup.
- A skill that hands work to an agent does the work itself when the agent isn't
  loaded, by reading `agents/<name>.md` from the installed plugin.
- No hidden skills (`user-invocable: false`).
- Skill descriptions never contain angle brackets; the uploader rejects them.
- Backend guides are plain reference files, never skills. No skill per service,
  no plugin per backend.
- Trigger word: one sentence in the README and `help`, "fork and rename with
  your agent". `configure` doesn't ask.
- `help` reads the installed README. The README is the one text, with the origin
  story and price watch as the bridge for the impulse to buy.
- Publishing to the directory waits for the test-drives. Keep `ntm` ready: a
  README of 40+ words, LICENSE, icon, author, homepage, repository, no
  credentials. The name similarity check happens only at submission.

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
- Note titles carry no prefix. The pause schedule is a document in the backend;
  with no documents, a task description.
- Whether the style exists is the switch for styled messages; there is no on/off
  setting.

## Agents

- Agents own their procedures. The reminder skills gather facts and hand them
  off.
- An agent can't start another agent.
- The estimator owns estimates, time guesses, explaining the ways to estimate,
  and review with the task review log. It never plans.
- With no estimate field, the estimate goes in the task description.
- The shopper owns its brief. It gets a task id and today's date only.

## Notifications

- No skill but `notify` sends anything.
- `configure-notifications`: the channel, the keys, one test push with explicit
  keys, then an open question about notification policy. A re-run shows and
  asks.
- On the Claude channel, jobs are created with push on, and the run's summary is
  the reminder. Reminders run from chat get no special case.
- When a push is too long, the list is summarized, not trimmed.

## Backends

- Shipped backend guides live in `conventions/references/<backend>.md`. Any
  other backend is described by the user under Todo list and smoke-tested
  against the contract; it can be built on anything, a Claude Doc for example.
- Backend guides own their setup, and describe parent auto-close.
- Setup asks the Linear team's estimate type; the connector can't read it.
- `configure-todo-list` picks the backend, collects what it needs, and checks or
  creates statuses, labels and notes. No `--test`: checks belong to
  `ready-check` and `self-test`.

## Jobs and scheduling

- A job is a three-line prompt that only loads a skill, written once in
  `configure-schedule`.
- `configure-schedule` walks each job kind (want it? days? time? title?) with
  defaults: morning weekdays 09:00, afternoon 14:30, evening 19:30, weekly
  planning Sunday 22:00, price watch daily 07:00 only if it's on, completed off.
  Titles and prompts belong to the user.
- Jobs are turned off and on, never "paused".
- A new job takes the creating chat's model, so `configure-schedule` asks once
  which model the jobs run on, proposes Opus, and sets it with `update_trigger`.
- `configure` order: About you, todo list, notifications, style, schedule.
  `configure` writes nothing itself and ends by suggesting `/ntm:self-test` in a
  new chat.
- `self-test`: `ready-check`, then a throwaway task and note, one line per step,
  ending `Self-test OK` or `Self-test FAILED at <step>`. It runs unattended.
- The price watch job runs daily, paused days included.

## The style

- No shipped personas. `configure-style` is a builder; "just remind me" means
  plain.
- A user's own persona goes in word for word under a `## For ntm` shim.
- The plugin defines no tone ladder; the user's style sets its own levels.
- Motifs rest for 20 messages by default.
- A day of reminders follows an episode arc: setup, middle, resolution, recap,
  credits.
- A title is part of the message's theme, never the reminder's name. The
  messenger asks again when the title is missing.
- Justin's own persona skill never ships.

## Price watch

- Price watch is on exactly when Todo list names a project. The watch uses the
  project label only.
- Deal details go in the run's final reply, not a thread post.

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
- `$` names are bare and never shown to the user. Plugin and skill names never
  take a `$`.

## 0.4: decided

The v0.4 branch and git history keep the raw material, including the old 0.4
design page.

- Base plugin `neurodivergent-task-manager` (published; commands autofill, so
  the length costs nothing). User plugin `ntm`, a fixed name so the base can
  always reach the contracts. An optional alias plugin whose name is the user's
  word; there is no setting for it.
- Every job and every command the user types starts in `ntm`, setup included, so
  a user with an alias never types the base's name.
- `setup` and `update` are ways into `configure`, which absorbs settings and
  upgrades. The base has no `settings`.
- Contracts in `ntm`: `settings`, `style`, `notify`, `todo-list`, `ready-check`
  (only in `ntm`) and `self-test`. Both self-tests keep the name `self-test`.
- The base is a guide the user's agent follows. Only contract names and call
  shapes are fixed.
- `ntm`'s `notify` carries the Pushover-or-chat choice for that user.
- The generated `ntm` bundles the connector for the user's backend.
- Plugin and file renames stay separate from content renames.
- No migration from 0.3; installs start fresh. The base and `ntm` update
  together.
- displayName "Neurodivergent Task Manager", without "(ntm)".
- Publishing adds: the base self-test passes with no `ntm` installed;
  `configure` never sends or creates without being asked; a privacy page; the
  name check for `neurodivergent-task-manager`; `Template source:` points at a
  release.

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

- "Keeps slipping" never climbs: the style history doesn't record task ids.
  Justin places it. Idea, 0.4-sized: planning owns a mention history note where
  each reminder records the date for every task it names; the caller passes each
  task's count through the messenger to the style, which only maps a count to a
  level; the weekly `fix-todo-list` keeps only ids still open. JSON in a note is
  fine.
- Per-reminder Pushover tokens don't work: `configure-notifications` writes free
  text, and `notify` reads a fixed line format. Specific to Justin's own
  `ntm-user`. His idea: a dictionary in settings mapping each reminder to its
  token.
- Date-math edges in report spans ("last month" on the 1st): not worth fixing.
  Someday, maybe: phrase spans as "since the last scheduled run".
- A reading-comprehension pass: writers simplify, human comprehension first ("if
  a human can comprehend, so can a model"). Includes the estimator's "Good
  enough reminders complete." and `weekly-planning`'s parenthetical about
  `fix-todo-list`'s result. Justin places it.
- Waiting for Justin:
    - About you's Name and Planning's Parents are collected, but nothing reads
      them: wire them in or drop them?
    - Should the shopper price Amazon when Amazon alerts are off?
    - `self-test` claims every backend operation but skips comments, labels and
      agents: add the steps or narrow the claim?
    - Does showing a key's last four characters count as printing it? Are keys
      OK in the curl command in run transcripts?
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
- 0.4, open: first-run setup needs Linear before `ntm` exists, so the user
  connects through the Connectors tab first, and a bundled server would be a
  second Linear. Decide which wins.
- Before 0.4: install main on Justin's account with a fresh setup and use it for
  a few days. His installed copy is 0.3.0 with old setting names.
- Small PR: line-length checking inside fenced blocks in the lint, and
  devbox.json plus a Makefile (lint, fix), as in his other repos.
- `/domain-first-design` revision and Justin's design agents: parked (GULU-314).
