# ntm: where things are (updated 2026-11-07)

Current state and what's next, for the orchestrating session. The working rules
are in `CLAUDE.md`, what's decided in `DECISIONS.md`, and names in `NAMES.md`.

## Main

0.3.2 plus #3 to #16, all squash merges: bug fixes, review-todo-list, task and
review wording, lint (Prettier, markdownlint, CI), estimates on the user's
scale, author, Linear estimate type, job prompts as one pattern, backend guides
that own their setup (no Claude Docs guide), conventions fixes, tables as
sections, the ntm-user template replaced by a guide, and #15: the estimator
agent (estimates, time guesses, review and the task review log), the planner
merged into `ntm:plan`, estimate wording (`Estimate scale`).

## Branches and PRs

- Open PRs: `gh pr list`. #2, the single-branch 0.4 attempt, is closed unmerged;
  its branch `v0.4` stays as raw material for 0.4.
- `plugin-history-2026-11-06`: history from before the 0.3 squash.
- History was rewritten on 2026-11-07 to take a leaked address out of commit
  metadata. A clone from before then is stale; re-clone. GitHub Support has a
  ticket to purge the old pull request refs; nothing to do unless they ask.

## Justin's installed copy

ntm 0.3.0 and its ntm-user, five jobs on Opus. Its settings use old names
(Ticket prefix, Week ahead, grooming log), so the next release needs a fresh
setup.

## Next

The Deferred and open section of `DECISIONS.md`.
