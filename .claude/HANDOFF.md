# ntm: where things are (updated 2026-11-07)

Current state and what's next, for the orchestrating session. The working rules
are in `CLAUDE.md`, what's decided in `DECISIONS.md`, and names in `NAMES.md`.

## Main

Version 0.3.2 in plugin.json; no PR since #1 has changed it. #3 to #17 are all
squash-merged: bug fixes, the review-todo-list skill, wording, lint and CI,
estimates on the user's own scale, the job prompts, the backend guides, the
conventions, the `ntm-user` guide, the estimator agent (#15, which also merged
the planner agent into `ntm:plan`), and Linear connected from the Connectors tab
(#17). `DECISIONS.md` has what each settled.

## Branches and PRs

- Open PRs: `gh pr list`. On 2026-11-07: #18 (notify owns the channel caps; the
  messenger is handed its settings), #19 (small fixes), #20 (devbox, direnv,
  make), #21 (line length in fenced blocks).
- #2, the single-branch 0.4 attempt, is closed unmerged; its branch `v0.4` stays
  as raw material for 0.4.
- `plugin-history-2026-11-06`: history from before the 0.3 squash.
- History was rewritten on 2026-11-07 to take a leaked address out of commit
  metadata. A clone from before then is stale; re-clone. GitHub Support has a
  ticket to purge the old pull request refs; nothing to do unless they ask.

## Justin's installed copy

ntm 0.3.0 and its ntm-user, five jobs on Opus. Its settings use old names
(Ticket prefix, Week ahead, grooming log), so the next release needs a fresh
setup.

## Next

1. The questions in `NAMES.md`, one at a time.
2. The open PRs, as he reviews them.
3. Then the rest of Deferred and open in `DECISIONS.md`, as he picks.
