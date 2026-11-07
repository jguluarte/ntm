# Naming decisions (owner, 2026-11-05) — apply in one rename pass before packaging

| Built as                                   | Final                                                                     | Status            |
| ------------------------------------------ | ------------------------------------------------------------------------- | ----------------- |
| `nudge:board`                              | `nudge:conventions`                                                       | settled 14:50     |
| `nudge:due`                                | `nudge:todo-list` (no args = today; words = scope)                        | settled 14:50     |
| `nudge:voice`                              | `nudge:style-message`                                                     | settled 14:50     |
| `nudge:messenger` (profile skill)          | `nudge:communication-style`; note "…: communication style"                | settled 13:59     |
| config `voice on`, `messenger name`        | removed; the note's existence is the switch, its `Name:` line is the name | settled 13:59     |
| `Send FAILED:`                             | `Messenger FAILED:`                                                       | internal, decided |
| `Subject:` line from the voice             | `Title:`                                                                  | internal, decided |
| profile heading `## What gets you to read` | keep                                                                      | decided           |
| `nudge:ping`                               | `nudge:ready-check`                                                       | settled 14:53     |
| plugin name `nudge`                        | open                                                                      |                   |
| other skill names, job titles, tones       | open (owner drives next round)                                            |                   |

## 15:25 batch

| Built as                                              | Final                                                                                                                                                                                        | Status                         |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `nudge:notify`                                        | `nudge:notify`                                                                                                                                                                               | settled                        |
| `nudge:recap`                                         | proposed `nudge:history`                                                                                                                                                                     | open (owner leaning `history`) |
| `nudge:plan --weekly/--daily/--replan`                | `nudge:plan --auto day` / `--auto week` (unattended; jobs use these); `nudge:plan <context>` plans with the user in chat, asks only if ambiguous                                             | settled                        |
| `nudge:setup`                                         | `nudge:configure`                                                                                                                                                                            | settled                        |
| `nudge:jobs`                                          | `nudge:configure-schedule`                                                                                                                                                                   | settled                        |
| agent `price-checker`                                 | `shopper`                                                                                                                                                                                    | settled                        |
| agents `planner`, `messenger`                         | keep                                                                                                                                                                                         | settled                        |
| job skills morning/afternoon/evening/week/price-watch | if kept: `run-` prefix; owner questions whether they should be skills at all (prefers the sequence to live in the scheduled task's prompt, defaults from configure-schedule, user-refinable) | open — discuss in chat         |

## 15:33

| Built as                                  | Final                                                                                                                     | Status  |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------- |
| `nudge:price-watch`                       | `nudge:run-price-watch`                                                                                                   | settled |
| `nudge:amazon-alerts`                     | `nudge:run-price-watch-amazon`                                                                                            | settled |
| `nudge:morning` / `afternoon` / `evening` | `nudge:morning-reminder` / `afternoon-reminder` / `evening-reminder`                                                      | settled |
| `nudge:week`                              | no skill; default sequence becomes the scheduled task's prompt, owned by `configure-schedule` as a user-refinable default | settled |

## 15:49 batch

| Built as                                      | Final                                                                                                                                                                                     | Status             |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `nudge:groom`                                 | `nudge:review-todo-list`                                                                                                                                                                  | settled            |
| `nudge:cleanup`                               | `nudge:fix-todo-list`                                                                                                                                                                     | settled            |
| `nudge:recap`                                 | proposed `nudge:show-completed` (owner's idea; prefers "completed")                                                                                                                       | open, yes to close |
| `nudge:days-off`                              | proposed `nudge:time-off` (bare = show; dates = take off; `--check` for jobs)                                                                                                             | open, yes to close |
| tone ladder light/escalated/harsh/affirmation | not plugin-defined: the communication-style note defines its own levels; the "harder each day" policy climbs whatever levels the note has; the four names survive only as an illustration | settled            |
| scheduled-task titles                         | fine for now; revisit while working on configure-schedule                                                                                                                                 | parked             |

## 16:01

| Built as         | Final                                                                                                                                                                                                                                              | Status  |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `nudge:recap`    | `nudge:show-completed`                                                                                                                                                                                                                             | settled |
| `nudge:days-off` | `nudge:pause` — bare: ask whether to see or change the pause schedule; with words: follow them; `--check` for jobs. `configure-schedule` says enable/disable for jobs, never pause. The note stays "…: days off"? → use "…: pauses" (owner's word) | settled |

## 2026-11-05 — configuration skills (no settings layer on chat/Cowork)

Research: chat/Cowork have no plugin settings layer. `userConfig` prompts are
Claude Code only (chat ignores `${user_config.*}` MCP refs; Cowork doesn't
prompt; cloud Code sessions can't supply it either). Agents and hooks are
ignored in chat, load in Cowork/Code. `${CLAUDE_PLUGIN_DATA}` is Code-only.
Scheduled tasks run remotely as Cowork sessions with skills + plugins; agent
loading there = test-drive item 1.

Consequences:

- Config stays in the plugin's own files (template → personalized copy). Do NOT
  add `userConfig`.
- Secrets (Pushover keys) stay in the personalized copy's config note.
- New SPEC rule: every skill that delegates to an agent must do the work inline
  when the agent isn't loaded.

Names (Justin, 2026-11-05):

- `configure` → `settings`
- new `configure-notifications` (channel choice, credentials, test push)
- `adapter` → `configure-integration` (SETTLED 2026-11-05). One skill;
  per-service guides are plain files under
  `skills/configure-integration/references/` (`linear.md`, `claude-docs.md`,
  `CONTRACT.md`) — never skills, so contributors add a file without adding a `/`
  entry. Per-service skills (`configure-linear`) rejected; hidden skills not
  used; plugin-per-backend rejected.
- new `help` — renders README
- `communication-style`, `configure-schedule` unchanged
- Hidden skills (`user-invocable: false`) are Code-only as far as docs say; not
  used.
- `run-price-watch-amazon` → `sync-price-watch-with-amazon` (Justin, in the
  names doc, 16:43)
- Later: decide what belongs under `settings` vs the `configure-*` skills
  (parked).
- `settings` = see/change user-facing settings after setup. New `setup` = first
  run only: prefix, then the configure-* skills in order; produces the
  personalized copy (Justin, doc comment 16:41).
- `communication-style` → `configure-communication-style` (Justin, doc comment
  16:41). Note title unchanged.
- Plugin name: proposed `name: ntm`,
  `displayName: "Neurodivergent Task Manager"`. `setup` must offer changing the
  prefix (rewrites `name` in plugin.json and the note-title prefix in
  conventions config). Pending Justin's yes.
- `setup` → `configure` (Justin 16:52): bare = first-run walkthrough (prefix,
  then each configure-_in order) or pick one part to redo; parent of the
  configure-_ family. `settings` unchanged.
- Plugin name SETTLED (Justin 16:55): `name: ntm`,
  `displayName: "Neurodivergent Task Manager"`. Expected to possibly fail the
  directory similarity check — revisit only at submission time. All names now
  settled; rename pass unblocked.

## 2026-11-05 17:43 — settings store (Justin)

- Target surfaces: Cowork and chat. Claude Code is NOT a target; drop Code-only
  paths from SPEC/README.
- Settings store = an account skill named `ntm-settings` (one SKILL.md,
  key/value table; description says it's loaded by `ntm:conventions` and changed
  with `/ntm:settings`). `conventions` loads it by name. `settings` writes it
  via the skill save card (propose_skills; user taps save). Scheduled runs read
  only.
- Test-drive item: confirm the save card fires from a plugin skill on mobile
  chat and in Cowork.
- Banned word: "voice" — nowhere in the plugin. `voice history` →
  `message history`; history length lives in the message-history note itself,
  not in settings.
- Not yet decided: what goes in `ntm-settings` vs plugin files (item 3); whether
  the template gets personalized at all and the prefix question are the
  user's/their agent's call — the plugin must work either way (same settings
  skill, or values baked in by customization).
- Settings store skill name: `ntm-user-settings` (Justin 17:48;
  underscores/leading markers aren't legal in skill names). Bare invocation:
  show the values and say they belong to ntm, change via `/ntm:settings`. The
  template refers to it by literal name; a prefix customization renames both.

## 2026-11-05 17:55 — what goes in `ntm-user-settings` (Justin)

Freeform under fixed headings; defaults pre-filled by `configure`; `conventions`
reads by heading.

- Labels — issue labels (live, corrected): `no-autoschedule`,
  `pending-shipment`, `deadline`, `has-amazon-price-watch`,
  `amazon-unavailable`. Project labels: `price-watch`, `no-autoschedule`
  (inherited). `price-watch` issue label is RETIRED (2026-10-17). Plugin's
  `amazon-alert` is wrong → `has-amazon-price-watch`.
- Deviations — anything the user does differently from the plugin's default
  conventions.
- Board — everything specific to their ticket backend (tracker, board/team, ids,
  status names).
- Notifications — channel + credentials + freeform policy (e.g. a different
  Pushover app token per reminder); `notify` reads this section and follows it.

## 2026-11-05 17:57 — `ntm-user` is a plugin, not a skill (Justin)

Rule: user-authored → `ntm-user`; runtime-written by jobs → notes on the board.

- `ntm-user:settings` — as defined above (replaces `ntm-user-settings` skill
  name).
- `ntm-user:style` — the communication-style profile;
  `configure-communication-style` writes it; `style-message` loads it by name.
  Import path: Justin's existing persona skill becomes `ntm-user:style` as-is.
  `messenger note` key removed.
- Board notes stay: message history, pauses, grooming log, price-watch stores,
  Amazon alert flow.
- Delivery: `configure` packages `ntm-user.plugin` for the user to accept
  (Cowork accept card); `settings` regenerates it.
- Pause schedule = a document in the backend (Linear doc / Claude doc / whatever
  the backend offers). (Justin 18:00)
- Shipped backend guides live in `conventions/references/<backend>.md` (linear,
  claude-docs), not under `configure-integration`. Any other backend is
  described by the user under Board in `ntm-user:settings`;
  `configure-integration` helps write that section and smoke-tests it against
  the contract `conventions` states.

## 2026-11-05 18:04 — configure-integration (Justin)

- Bare: pick backend (linear / claude-docs / other), collect what that backend
  needs, check statuses/labels/notes (offer to create missing), write Board +
  Labels of `ntm-user:settings`. With a backend named: skip the first question.
- Already configured: show current Board + Labels and ask whether to change
  anything. No `--test`; checks are `ready-check`'s job.

## 2026-11-05 18:13 — configure-notifications / configure-communication-style (Justin)

- configure-notifications: channel (pushover | claude); pushover → tokens + one
  test push; open question for any policy in the user's words (e.g. per-reminder
  app tokens). Writes Notifications of `ntm-user:settings`. Re-run: show + ask.
  With the claude channel, configure-schedule creates tasks with "notify when
  finished" + push on; the reminder is the run's summary. No special-casing of
  chat-triggered reminders.
- configure-communication-style: NO shipped personas. A persona BUILDER:
  sections = register, the hook, escalation (user-named levels + climb rule),
  signature moves (+ repeat limit → message history), what stays untouched
  (task/date/ticket), examples (one per level). User supplies any theme; builder
  derives sections with them. "Just remind me" → plain answers for every
  section. Import path: an existing profile/skill handed in → written as
  `ntm-user:style` unchanged. Re-run: show + ask. His persona skill never ships
  in the template.

## 2026-11-05 19:47 — configure-schedule (Justin)

Walks through the kinds of jobs; for each: want it? which days? what time?
Creates/updates the scheduled tasks (push notification on). Re-run: list
existing, ask what to change. Enable/disable, never pause. Kinds + offered
defaults: morning reminder (weekdays 09:00), afternoon reminder (weekdays
14:30), evening reminder (weekdays 19:30), weekly planning (Sun 22:00: plan
--auto week, fix-todo-list), price watch (daily 07:00, only if on), overview
(show-completed weekly/monthly, off by default). Titles and prompt text are per
user, asked during setup, created in their schedule — nothing locked by the
plugin.

## 2026-11-05 19:50 — configure (wizard) + trigger-word rename (Justin)

- configure bare, nothing set: two-line intro, then configure-integration →
  notifications → communication-style → schedule, skipping done ones; packages
  `ntm-user.plugin` for the accept card; runs ready-check once installed.
  Already configured: one line of state per part, ask which to change, hand off.
  `configure <part>` → straight there. configure writes nothing itself.
- Trigger-word rename: offered in `configure` AND `settings`; mentioned in
  `help` as customizable. The renamed copy differs from the template only by
  `name` in plugin.json + literal `ntm-user` references (keep it that way). If
  renamed: ask whether the weekly job should watch upstream for changes; if yes,
  weekly job compares versions and offers to regenerate (re-fetch template,
  re-apply the substitution, hand back a .plugin). Tell them to uninstall the
  original after installing the renamed copy.

## 2026-11-05 20:12 — self-test + publishing (Justin)

- The plugin must be able to test itself. Proposed `ntm:self-test` (name pending
  Justin): ready-check, then on a throwaway ticket + note: create → plan →
  todo-list → style-message (no send) → notify test push (ask first) → close →
  show-completed → fix-todo-list dry run → pause --check → remove throwaway. One
  line per step; `Self-test OK` / `Self-test FAILED at <step>: <why>`.
  configure-integration's smoke test = self-test. help lists it.
- Justin intends to publish to the directory after his friend's test-drive: keep
  `ntm` submission-clean (README 40+ words, LICENSE, icon,
  author/homepage/repository, no credentials, no brand names).

## 2026-11-05 21:35 — v0.2.0 packaged

Built to SPEC v2.2 (+ amendments logged in reviews/). Review rounds: SPEC ×3 +
verify; keystone; groups B–F2; integration (6 run traces); dry runs on
Opus/Sonnet/Haiku + confirmation on Haiku/Sonnet; prose tightening + diff check.
Validator passes; leak grep 0. Delivered ntm.plugin + HANDOFF.md. Live skills
and tasks untouched. Open for the test-drive: agents in scheduled runs; accept
card on chat; Claude Docs guide untested; directory name check; Template source
none yet.

- 21:40 Upload fixes: (1) ntm-user template files renamed `plugin.json.template`
  / `SKILL.md.template` (uploader saw a second plugin.json); (2) two skill
  descriptions had `<name>`/`<part>` placeholders — uploader rejects angle
  brackets in descriptions. Installed on Justin's account via the browser: 23
  skills, 3 agents, Linear connector.

## 21:52 Migration run (Justin's own account)

- Schedule swap done: five `<Kind> (ntm)` tasks on (suffix per Justin, not
  prefix), five original tasks off. Weekly recap was already off.
- `the message history note` wiped to `Keep: 60 entries or 8 weeks` + empty
  jsonl block; title kept, settings point at it.
- `ntm-user` 1.20261106.550 generated through ntm:settings' Regenerating steps
  and installed via Chrome `file_upload`.
- Finding: `file_upload` rejects `/mnt/user-data/outputs/` ("only files this
  session is allowed to read"); a path under the working directory works.
  Regenerating step 7's outputs copy is for the card, not the upload.
- Finding: Handed in keeps a body verbatim, so the persona skill's theme list
  (under its own `--stay-fresh` section) isn't under `## Motifs`; style-message
  sees no motifs. Decision pending with Justin: leave verbatim, or give Handed
  in a rule to carry a themes list into Motifs.
- Open: the imported body still carries the persona skill's own Linear history
  instructions and its own command usage; style-message's own history handling
  is more specific and should win. Watch the first scheduled runs for
  double-writes to the history note.
- Finding: create_trigger inherits the creating chat's model; Justin's five jobs
  came out on Fable and were switched to claude-opus-5-5 by hand.
  configure-schedule should set the model (Opus) with update_trigger right after
  each create, and say which model the jobs run on.
- Finding: self-test step 6 (notify) is interactive ("send one test push now?" /
  "got it"), so a fresh-agent run skips it. Make it unattended: send the push
  and report "sent; confirm it arrived", or take a flag.

## 2026-11-06 00:00–01:00 — 0.3 restructure (Justin asleep; PR review of 38 comments)

Justin's review of PR #1 (github.com/jguluarte/ntm) turned the cleanup into a
restructure. His comments, read as principles and applied everywhere they fit:

- Agents own their procedures (messenger composes+styles+sends; planner answers
  four named requests; shopper owns the brief). Reminder skills gather facts and
  hand off; fallback when an agent isn't loaded: read `agents/<name>.md` from
  the installed plugin (verified readable at
  ~/.claude/plugins/synced/<id>/ntm/agents/).
- Rules in conventions, values in ntm-user:settings (new Planning and Shopping
  sections), tool calls in guides. Labels, note titles (no NTM: prefix),
  exclusions, parent rule, estimate scale, rhythm are agreed defaults in
  configure-board.
- deadline label removed everywhere.
- ntm:style-message → ntm-user:style (one skill: Usage + Profile + procedure; a
  handed-in persona goes in verbatim under a `## For ntm` shim). ntm-user has
  two skills: settings, style.
- Jobs are three-line wrappers; weekly-planning and completed --notify are
  skills. Job files named after titles, header boilerplate gone.
- Names: price-watch, amazon-alerts, completed, configure-board, configure-style
  (table posted on the PR; applied in its own commit "Names judged at the call
  site" so it can be dropped).
- Trigger word: one sentence in README/help ("fork and rename with your agent");
  the settings procedure removed; configure no longer asks.
- help reads the installed README; README is the one text, with the origin story
  and price watch as the impulse bridge.
- builder: beats modeled on an episode arc, abstracted (setup / middle /
  resolution / recap / credits).
- Review loops per Justin's 00:06 instruction: Fable reviewers only (architect,
  naming critic, comprehension dry run), then Haiku/Sonnet/Opus comprehension at
  the end.
- DESIGN-0.3.md is the brief every author and reviewer worked from. validate.sh
  is the packaging gate.
- Justin's ntm-user for 0.3 built as nudge-work/ntm-user-0.3.plugin (his persona
  skill verbatim as ntm-user:style). NOT installed; his live 0.2.0 + jobs
  untouched overnight.

## 2026-11-06 08:00–08:45 — 0.3.0 shipped to Justin's account

- Overnight stall: three reviewer subagents sat on unanswered Bash approval
  prompts (a `cd` into /tmp counts). Rule from now: reviewer and dry-run agents
  get Read/Glob/Grep/Write only, never Bash.
- Haiku 18 / Sonnet 17 / Opus 6 points → 23 clarity edits, plus Justin's
  answers: motif window 20 (default and his his persona skill copy); spans are
  days ending today, last month = previous calendar month's length; plan in chat
  asks; pausing a day with planned work replans the week; deal details in the
  run's final reply (no thread post), push overflow summarized not trimmed;
  "board" → "todo list"; todo-list → today; configure-board + review-todo-list →
  configure-todo-list.
- Rename table (all renames since the first) posted on PR #1 for sign-off.
- Installed on Justin's account 08:39: ntm 0.3.0 and ntm-user 1.20261106.1634.
  Weekly planning (ntm) prompt re-synced to the wrapper. Self-test launched
  08:41.
- validate.sh is the gate; DESIGN-0.3.md the brief; reviews in reviews/0.3/.
- 08:56 Justin: history squashed per his ask (renames first, then content
  commits); old history on plugin-history-2026-11-06.
- QUEUED (after this review pass): lint — wrap prose at <= 80 columns, never
  mid-word; tables and code blocks exempt; add the check to validate.sh; one
  reflow commit.

## 2026-11-06 afternoon and evening (Opus orchestrating)

- PR #1 merged as ntm 0.3.2 (#1): one commit per version (nudge 0.1.0, ntm
  0.2.0, 0.2.1, 0.3.0), the review commits, 0.3.1, the reflow, 0.3.2. A markdown
  linter comes in its own PR; tools/reflow.py stays outside the repo.
- Rule: a rename lands only after Justin's explicit yes; silence is not approval
  (the 11-06 "unanswered rows stay" table is how names drifted).
- Names audit (doc "ntm names: what drifted"), Justin's answers: keep
  `price-watch`, `configure-style`, `weekly-planning` (tentatively; weekly is a
  sane default cadence), `has-amazon-alert`, `Message history`, `help`; restore
  `review-todo-list` as its own skill; the grooming log note is
  `Task review log`.
- 0.4 names: base `neurodivergent-task-manager` (published), user plugin `ntm`
  (fixed), optional alias plugin with the user's word; `setup` and `update` are
  entry points to `configure`; base has no `settings`; `ready-check` is an `ntm`
  contract; contract for the backend guide stays `todo-list`; both self-tests
  keep `self-test`.
- Terminology: the plugin's word is "task" (not "ticket"); Vocabulary defines it
  once with how each tracker represents it. `$` marks only values the user
  configures, by their default name: the labels ($no-autoschedule,
  $pending-shipment, $price-watch, $has-amazon-alert, $amazon-unavailable). No
  `$` on Vocabulary words. "Groom"/"grooming" go: the process is review
  (`review-todo-list`). Estimate is a plain word, not "groomed size". Job stays
  defined; its definition avoids "task".
- Titles: written with the message as part of its theme, never the reminder's
  name; in v0.4 (style template, configure-style's For ntm rule, messenger
  re-asks).
- Fable runs only when Justin says so (weekly budget).
- Product in prose stays "ntm" (it's also the user's plugin, what they type);
  the base's displayName is "Neurodivergent Task Manager", without "(ntm)"
  (Justin, 19:37).

## 2026-11-06 night (Opus orchestrating)

- The single 0.4 branch was the wrong shape: too much at once, out of Justin's
  control. Work is now split as a human team would: small PRs to main, one
  concern each, an agent per PR. The v0.4 branch is raw material.
- Most of the 0.4 branch was 0.3 patch work. Merged to main as squash merges: #3
  bug fixes (titles, completed, three slips), #4 review-todo-list (grooming was
  meant to be one skill; a bug), #5 wording (task, review, $ on configured
  labels only, vocabulary), #6 lint (Prettier and markdownlint, 80 columns,
  4-space indent, frontmatter included, CI on PRs; .nvmrc dropped for engines),
  #8 estimates (setup asks how the user sizes tasks and offers to explain;
  Linear maps their scale onto the team's points; settings keep Estimate mapping
  and Estimate help).
- No patch version bumps for these.
- Follow-ups agreed: readable tool calls; conventions (scope into settings,
  automations into backend guides, no parent planned date); job prompts as one
  pattern; tables that should be sections; a writer pass before 0.4.
- 0.4 rethink (open): the generator is too prescriptive; the base should be a
  guide for the user's agent, with only contract names and call shapes fixed.
  Plugin and file renames belong to 0.4, separate from content renames.

## 2026-11-06 late night and 2026-11-07 morning

- Follow-ups before 0.4, all merged: author in plugin.json (#9); setup asks the
  Linear team's estimate type, since the connector can't read it (#10); job
  prompts written once in configure-schedule (#11); backend guides lay out calls
  for reading, own their own setup, and the Claude Docs guide is dropped: the
  contract says a backend can be built on anything, a Claude Doc for example
  (#12); whose tasks count is a setting, parent auto-close lives in the backend
  guides, a parent's own date means nothing is gone (#13); tables kept only
  where they read well (notify, ready-check, setup skills), the rest as
  contract-style sections (#14); the ntm-user template replaced by a guide the
  user's agent follows (#16).
- #15: estimating stated once, in estimate wording ("sizing" is jargon; the key
  is Estimate scale). A new estimator agent owns what an estimate is, estimating
  a task, time guesses, explaining ways to estimate, and reviewing the todo list
  with the user, keeping the task review log. The planner agent is merged into
  ntm:plan, because an agent can't start another agent; only plan asks the
  estimator, and nothing everyday does. With no estimate field, the estimate
  goes in the task's description.
- Watcher runs whenever PRs are open; pseudo-markup in agent files is indented.
- Commit email leak: commits carried his private Claude address and spammers
  harvested it. Commits now use the GitHub noreply address; Justin's other agent
  rewrites this repo's history after #15.

## 2026-11-07 midday (Claude Code on Justin's laptop)

- History rewrite done: every branch force-pushed with commit identities on his
  GitHub noreply address. Actions runs that showed the old address are deleted,
  so Actions history starts fresh. GitHub Support is asked to purge the old pull
  request refs (#1 to #16).
- New commits take their identity from git config (the noreply address); no
  `-c user.email` in commands.
- PR #2 closed unmerged; `v0.4` stays as raw material. Updating it meant
  resolving 40 conflicting files against a design already left behind.
- The PR watcher script is dropped.
- Orchestration moves from the Cowork container to Claude Code on Justin's
  laptop: GraphQL works there (`gh pr create`), the remote is `jguluarte`, and
  worktrees are siblings under `~/code/.claude-worktrees/ntm/`. Lasting rules
  move into `.claude/CLAUDE.md`; HANDOFF keeps only state and next steps.
