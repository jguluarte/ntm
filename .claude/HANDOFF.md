# ntm: handoff for the next session (updated 2026-11-07 09:10 PT)

Notes for the orchestrating session, not for Justin. Read this first, then
`DECISIONS.md` for history. `DESIGN-0.4.md` is out of date (see its banner);
don't author from it.

## Before touching the repo

The repo's history is being rewritten out from under this project. Justin has
another agent replacing the commit email his private Claude address (leaked
through public commit metadata and harvested by spammers) with his GitHub
noreply address across every branch, by force-push. After that every commit id
changes:

- Re-clone `github.com/jguluarte/ntm` before any work; never push from a clone
  made before the rewrite (`/home/claude/ntm` in an old container is stale).
- Commit as `Justin <950947+jguluarte@users.noreply.github.com>`. Never use his
  private Claude address anywhere in git.
- `jguluarte/dos2-skills` had the same leak; his other agent handles it.

## How Justin wants this run

- He owns the plugin. Don't run ahead: nothing lands unless he asked for it or
  approved it. Decisions come to him one at a time; user-facing names are his.
- Work is split the way a human team would split it: small PRs against main, one
  concern each, one Opus agent per PR. Agents can't start agents (no Agent tool
  in subagents), so the orchestrator does any fan-out.
- Route each of his PR comments to the PR's author agent, which replies on the
  thread and pushes a new commit. Resolve finished threads.
- Merges are squash merges, on his say-so. Merged branches auto-delete.
- Once he's reviewing a PR, no rebase or force-push; bring main in with a merge
  commit.
- 80 columns everywhere, including frontmatter and fenced blocks; `npm run fix`
  then `npm run lint`. The lint doesn't check line length inside fenced blocks
  yet (markdownlint's Prettier preset turns MD013 off).
- In agent files, pseudo-markup like `<example>` is indented like nested markup.
- He doesn't care about patch version bumps; main says 0.3.2.

## Where things are

- Main has 0.3.2 plus #3 to #16 (all squash merges): bug fixes,
  review-todo-list, task and review wording, lint (Prettier, markdownlint, CI),
  estimates on the user's scale, author, Linear estimate type, job prompts as
  one pattern, backend guides that own their setup (no Claude Docs guide),
  conventions fixes, tables as sections, the ntm-user template replaced by a
  guide, and #15: the estimator agent (estimates, time guesses, review and the
  task review log), the planner merged into `ntm:plan`, estimate wording
  (`Estimate scale`).
- Open: only PR #2 (draft, branch `v0.4`), the abandoned 0.4 attempt; raw
  material only. Also on GitHub: `plugin-history-2026-11-06` (old history).
- GraphQL is blocked: open PRs, comment and merge with `gh api` REST calls.
- Agents post under Justin's account; their replies end with
  `<!-- ntm-agent -->`.
- Installed on his account: ntm 0.3.0 and its ntm-user, five jobs on Opus. Its
  settings use old names (Ticket prefix, Week ahead, grooming log), so the next
  release needs a fresh setup. Never touch his scheduled tasks or live skills
  unasked.

## Next

- A small PR: turn on line-length checking for fenced blocks in the lint.
- 0.4, talked through with Justin before any authoring: the user plugin as the
  way in (contracts, entry points, configure absorbing settings and upgrades),
  plugin renames (base `neurodivergent-task-manager`, user `ntm`), and the base
  as a guide the user's agent follows rather than a prescriptive generator (main
  already does this for ntm-user, #16).
- `/domain-first-design` revision and his design agents: parked (GULU-314).
