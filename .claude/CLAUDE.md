# ntm: working rules

Read `.claude/DECISIONS.md` for what's decided and what's next.

## The repo

A Claude plugin: markdown skills and agents, and a few JSON files. The base
plugin is `ntm` and the user's generated plugin is `ntm-user`, on main and in
0.4 alike. 0.4 is built on `release-0.4`, an integration branch: branch from it
and open every PR against it. It may hold mismatches between files while each
file is rebuilt in its own PR; it only has to be right before release. Don't
author from the `v0.4` branch, the old 0.4 design page, or his installed 0.3.0
copy.

## Justin owns the plugin

- Nothing lands unless he asked for it or approved it. Don't run ahead.
- Decisions go to him one at a time. User-facing names are his. A rename lands
  only after his explicit yes; silence is not approval. Plugin-internal names
  (status, delivery and result lines) don't need it.
- `make test` holds the skill and agent names and plugin.json's name and
  displayName to `tests/expected/`, and fails on any difference. A PR that
  changes a name updates `tests/expected/` in the same PR and says so in its
  description; that diff is how Justin sees the rename and pushes back. A name
  test failing for a change nobody meant means: put the name back.
- Never touch his installed copy, his scheduled tasks or his live skills
  unasked.

## How work runs

- Each PR is a chunk of work a person can review and know in one sitting. Each
  thing in it lands with the work that first needs it.
- Small PRs against `release-0.4`, one Opus agent per PR, briefed with
  `.claude/briefs/COMMON.md` and `.claude/briefs/PR.md`. Subagents can't start
  agents; the orchestrator does any fan-out.
- The orchestrator runs in Claude Code on his laptop. The remote is `jguluarte`;
  worktrees are siblings under `~/code/.claude-worktrees/ntm/`.
- Reviewer and dry-run agents get Read, Glob, Grep and Write only, never Bash.
- Fable, the costliest model, on a weekly budget, runs only when he says so.
- His PR comments go to the PR's author agent, which replies on the thread and
  pushes a new commit. Agents post under his account, and every reply ends with
  `<!-- ntm-agent -->`. The orchestrator resolves finished threads; author
  agents don't.
- Merges are squash merges, on his say-so. Merged branches auto-delete.
- A squash merge gets a written message: one short paragraph on the net change,
  not GitHub's default list of every commit.
- Once he's reviewing a PR: no amend, rebase or force-push. Bring `release-0.4`
  in with a merge commit.
- Versions are set at merge; PR branches don't change them. He doesn't want
  patch version bumps.

## Commits

- Identity comes from git config: his GitHub noreply address. Never set
  `user.email`, and never use an address at his personal domain, anywhere.
- Each commit is a step a person can review and know on its own. The subject
  says in plain words what changed, with no design shorthand; a short body
  wrapped at 72; then the session's `Co-Authored-By` line.
- Stage files by name, never `git add -A` or `git add .`.

## Lint

80 columns everywhere: prose, frontmatter, fenced blocks. Indents are 4 spaces.
`tools/reflow.py` stays outside the repo. Tables and unbreakable text (a URL, a
code span) are exempt. Every line has a hard cap of 120 columns, tables and
unbreakable text included, checked by `make lint`. A long `description:` is a
`>-` folded block. Run `make lint-fix`, then `make lint`, which must pass
(devbox provides the linters through direnv); CI runs the same lint on every PR.
Prettier wraps prose; markdownlint holds fenced code blocks to 80 columns, and
tables are exempt.

In agent files, pseudo-markup like `<example>` is indented like nested markup.

## Text rules for the plugin

- The plugin's word for an item is "task", never "ticket". The process is
  "review", never "groom". The list is the "task list" in prose, never "board".
  `$` marks only the label names the user configures. `%` marks a user database
  by its default title. These plugin variables always sit in backticks,
  `$price-watch` and `%Settings`, and so does a configured label's name written
  without the `$`.
- Never the word "voice", in any form.
- Nothing that ties the plugin to a particular person: no names, no board name,
  no Drag Race words, no ADHD. The exception is the setup intro's origin story,
  which names its creator as an autistic ADHD person, never by name.
- A key is never shown in full in anything the user reads. Its last four
  characters are fine, and so is the curl command in `notify`.
- 24-hour time.
- Terse, plain, imperative. No AI filler phrasing.
- Write for the typical flow, not edge cases. State the trust basis and give the
  agent an escape hatch where a step depends on something it can't verify.
- Readers include people who don't do tech work: plain words over jargon.
