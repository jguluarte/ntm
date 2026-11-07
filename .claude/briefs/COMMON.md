# Common brief for the 0.3.x follow-up branches

## The repo

github.com/jguluarte/ntm is a Claude plugin: markdown skills and agents, and a
few JSON files. On main the base plugin is `ntm` and the user's generated plugin
is `ntm-user`; the templates for `ntm-user` are under
`skills/settings/references/user-plugin/`. Main already says "task" (never
ticket), "review" (never groom), and `$` marks only the configured label names.
Use main's names, paths and words. A later 0.4 renames the plugins; that is not
your branch's work.

The owner, Justin, owns this plugin. Keep your change small and exactly in
scope: no redesign, no improvements outside it. If something needs a decision,
stop and report it; don't decide it. Don't change versions.

## Your worktree

Work only in `/home/claude/ntm-<branch>`, on branch `<branch>`, which starts at
main. Never touch another worktree. Several branches run in parallel off main;
don't do another branch's work. Conflicts between them are resolved at merge.

## Lint

The repo has Prettier and markdownlint. Before each commit, in your worktree:
`npm --prefix /home/claude/ntm-<branch> ci` (once), then
`npm --prefix /home/claude/ntm-<branch> run fix`, then
`npm --prefix /home/claude/ntm-<branch> run lint`, which must pass. Lines are 80
columns, frontmatter included; tables and unbreakable text (a URL, a code span)
are exempt. A long `description:` is a `>-` folded block.

## Shell and git

Bash is for search (grep, find), git in your worktree, and npm as above. One
command per call. Absolute paths or `git -C <worktree>`; never `cd`, never
heredocs, never compound commands with `rm` (use `git -C <worktree> rm` to
delete tracked files).

Commit one concern per commit:

`git -C /home/claude/ntm-<branch> -c user.name=Justin -c user.email=950947+jguluarte@users.noreply.github.com commit -F <message file>`

Write message files with the Write tool under
`a scratch folder outside the repo `. A message is a subject in plain words
saying what changed (no design shorthand), a short body wrapped at 72, then
these two lines:

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com> Claude-Session:
<https://claude.ai/code/session_01QiwttzEY6czMx2y8EeEaxX>

## Helpers

You may spawn Opus subagents when splitting your branch's work in parallel is
more effective than doing it yourself. One layer only: tell every subagent you
spawn that it must not spawn its own. Brief each with exactly what it needs,
including this file's path.

## Text rules

- Never the word "voice", in any form.
- Nothing that ties the plugin to a particular person: no names, no board name,
  no Drag Race words, no ADHD.
- Keys are never printed. 24-hour time.
- Terse, plain, imperative. No AI filler phrasing.
- Write for the typical flow, not edge cases. State the trust basis and give the
  agent an escape hatch where a step depends on something it can't verify.
- Readers include people who don't do tech work: plain words over jargon.

## Size

None of these branches should add significant lines. If yours is growing, stop
and report why.

## When done

Open a pull request as `.claude/briefs/PR.md` says, send the main session the
URL and your report, and stop.

## Report

Your commits (hash and subject), one or two sentences per commit on what
changed, anything you weren't sure about, and anything you saw outside your
scope (report it; don't fix it). Don't restate files.
