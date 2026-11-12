# Opening your pull request, and answering the owner's comments

## The README

A branch that adds, changes, renames or removes a skill or agent updates that
one's entry in `README.md` in the same PR. `/ntm:help` answers from the README.

## Open it

When your branch's commits are done:

1. Push: `git -C <worktree> push jguluarte <branch>`. Never `-u`, never
   force-push.
2. Write the body with the Write tool, in the session's scratchpad directory:
    - One or two sentences on what the pull request changes and why, in plain
      words.
    - The commits, one line each: subject, then what to look for in it.
    - Anything the owner has to decide, each as one line.
    - "Versions are set at merge."
    - End with this line exactly:

        🤖 Generated with [Claude Code](https://claude.com/claude-code)

    - No bare `@name` anywhere; put any such text in backticks.
3. Open it:

    ```sh
    gh pr create -R jguluarte/ntm \
        --base release-0.4 --head <branch> \
        --title "<plain title>" --body-file <body file>
    ```

    The base is `release-0.4`, the integration branch for 0.4.

4. End with the pull request's URL and your report as your final message. When
   the owner comments, the orchestrator sends you the comments.

## Answering the owner's comments

The comments the orchestrator sends you are the owner's review of your branch.
For each:

- **A change inside your branch's scope:** make it as a new commit on top (never
  amend, rebase or force-push; the owner's review marks depend on the history
  staying put), push, and reply on that comment saying in a line what changed
  and in which commit.
- **A question:** answer it on that comment, plainly and briefly.
- **Something that needs the owner's decision, or is outside your branch:**
  reply that you've passed it on, and include it, with the comment's link, in
  your final message.

Every reply you post ends with a blank line and `<!-- ntm-agent -->`, so your
replies can be told from the owner's. Reply to a line comment with
`gh api repos/jguluarte/ntm/pulls/<number>/comments/<id>/replies -F body=@<file>`;
to a conversation comment or a review with
`gh pr comment <number> -R jguluarte/ntm --body-file <file>`. Write reply files
in the session's scratchpad directory. Don't resolve threads.

When you've handled every comment you were sent, end with one line per comment
saying what you did.
