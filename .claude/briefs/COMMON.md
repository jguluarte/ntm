# Common brief for a PR branch

The working rules, commit rules, lint and text rules in `.claude/CLAUDE.md`
apply to you. Read it in your worktree first.

## Your branch

Keep your change small and exactly in scope: no redesign, no improvements
outside it. If something needs a decision, stop and report it; don't decide it.
Don't change versions. Several branches may run in parallel off main; don't do
another branch's work. Conflicts between them are resolved at merge.

## Your worktree

The orchestrator names your branch. Make your worktree a sibling of the repo,
starting at main:

`git -C /Users/jguluarte/code/ntm worktree add /Users/jguluarte/code/.claude-worktrees/ntm/<branch> -b <branch> jguluarte/main`

Work only there. Never touch another worktree or the main checkout.

## Lint

In your worktree, run `direnv allow` once. Before each commit, run `make fix`,
then `make lint`, which must pass.

## Shell and git

One command per call. Absolute paths or `git -C <worktree>`; never `cd`. Delete
tracked files with `git -C <worktree> rm`.

Commit with `git -C <worktree> commit -F <message file>`. Write message files
with the Write tool, outside the repo, in the session's scratchpad directory.

## Size

No branch should add significant lines. If yours is growing, stop and report
why.

## When done

Open a pull request as `.claude/briefs/PR.md` says, then end with its URL and
your report as your final message.

## Report

Your commits (hash and subject), one or two sentences per commit on what
changed, anything you weren't sure about, and anything you saw outside your
scope (report it; don't fix it). Don't restate files.
