# Opening your pull request, and answering the owner's comments

## Open it

When your branch's commits are done:

1. Push: `git -C /home/claude/ntm-<branch> push -u origin <branch>`. Never
   force-push.
2. Write the body with the Write tool at
   `a scratch folder outside the repo <branch>-pr.md`:
    - One or two sentences on what the pull request changes and why, in plain
      words.
    - The commits, one line each: subject, then what to look for in it.
    - Anything the owner has to decide, each as one line.
    - "Versions are set at merge."
    - End with these lines exactly:

        🤖 Generated with [Claude Code](https://claude.com/claude-code)

        <https://claude.ai/code/session_01QiwttzEY6czMx2y8EeEaxX>

    - No bare `@name` anywhere; put any such text in backticks.
3. Open it with the REST API (GraphQL is blocked here, so `gh pr create` and
   `gh pr comment` fail):
   `gh api repos/jguluarte/ntm/pulls -f base=main -f head=<branch> -f title="<plain title>" -F body=@<body file> --jq .html_url`
4. Send the main session the pull request's URL and your report with SendMessage
   (to: "main"), and stop. A separate watcher polls the pull requests; when the
   owner comments on yours, the main session sends you the comments.

## Answering the owner's comments

The comments the main session sends you are the owner's review of your branch.
For each:

- **A change inside your branch's scope:** make it as a new commit on top (never
  amend, rebase or force-push; the owner's review marks depend on the history
  staying put), push, and reply on that comment saying in a line what changed
  and in which commit.
- **A question:** answer it on that comment, plainly and briefly.
- **Something that needs the owner's decision, or is outside your branch:**
  reply that you've passed it on, and send it to the main session with
  SendMessage (to: "main"), with the comment's link.

Every reply you post ends with a blank line and `<!-- ntm-agent -->`, so the
watcher skips it. Reply to a line comment with
`gh api repos/jguluarte/ntm/pulls/<number>/comments/<id>/replies -F body=@<file>`;
to a conversation comment or a review with
`gh api repos/jguluarte/ntm/issues/<number>/comments -F body=@<file>`. Write
reply files under `a scratch folder outside the repo `. Don't resolve threads;
the owner does.

When you've handled every comment you were sent, send the main session one line
per comment saying what you did, and stop.
