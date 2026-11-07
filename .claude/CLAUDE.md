# ntm: working rules

Read `.claude/HANDOFF.md` first for where things are and what's next, then
`.claude/DECISIONS.md` for history. `.claude/DESIGN-0.4.md` is raw material and
out of date; don't author from it.

## The repo

A Claude plugin: markdown skills and agents, and a few JSON files. On main the
base plugin is `ntm` and the user's generated plugin is `ntm-user`; 0.4 renames
them (base `neurodivergent-task-manager`, user `ntm`). Use main's names, paths
and words.

## Justin owns the plugin

- Nothing lands unless he asked for it or approved it. Don't run ahead.
- Decisions go to him one at a time. User-facing names are his. A rename lands
  only after his explicit yes; silence is not approval.
- Never touch his installed copy, his scheduled tasks or his live skills
  unasked.

## How work runs

- Small PRs against main, one concern each, one Opus agent per PR, briefed with
  `.claude/briefs/COMMON.md` and `.claude/briefs/PR.md`. Subagents can't start
  agents; the orchestrator does any fan-out.
- The orchestrator runs in Claude Code on his laptop. The remote is `jguluarte`;
  worktrees are siblings under `~/code/.claude-worktrees/ntm/`.
- Reviewer and dry-run agents get Read, Glob, Grep and Write only, never Bash.
- Fable runs only when he says so.
- His PR comments go to the PR's author agent, which replies on the thread and
  pushes a new commit. Agents post under his account, and every reply ends with
  `<!-- ntm-agent -->`. The orchestrator resolves finished threads; author
  agents don't.
- Merges are squash merges, on his say-so. Merged branches auto-delete.
- Once he's reviewing a PR: no amend, rebase or force-push. Bring main in with a
  merge commit.
- Versions are set at merge. He doesn't want patch version bumps.

## Commits

- Identity comes from git config: his GitHub noreply address. Never set
  `user.email`, and never use an address at his personal domain, anywhere.
- One concern per commit. The subject says in plain words what changed, with no
  design shorthand; a short body wrapped at 72; then the session's
  `Co-Authored-By` line.
- Stage files by name, never `git add -A` or `git add .`.

## Lint

80 columns everywhere: prose, frontmatter, fenced blocks. Tables and unbreakable
text (a URL, a code span) are exempt. A long `description:` is a `>-` folded
block. Run `npm run fix`, then `npm run lint`, which must pass; CI runs the same
lint on every PR. The lint doesn't check line length inside fenced blocks yet
(markdownlint's Prettier preset turns MD013 off), so check those by eye.

In agent files, pseudo-markup like `<example>` is indented like nested markup.

## Text rules for the plugin

- The plugin's word for an item is "task", never "ticket". The process is
  "review", never "groom". `$` marks only the label names the user configures.
- Never the word "voice", in any form.
- Nothing that ties the plugin to a particular person: no names, no board name,
  no Drag Race words, no ADHD.
- Keys are never printed. 24-hour time.
- Terse, plain, imperative. No AI filler phrasing.
- Write for the typical flow, not edge cases. State the trust basis and give the
  agent an escape hatch where a step depends on something it can't verify.
- Readers include people who don't do tech work: plain words over jargon.
