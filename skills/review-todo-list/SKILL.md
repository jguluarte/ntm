---
name: review-todo-list
description: >-
    Reviews the user's todo list with them in chat: closes obsolete or duplicate
    tasks, then estimates and splits unreviewed ones with their approval. Run by
    the user in chat, never by a job ("let's review my list", "review the
    kitchen project", "estimate the garage work").
---

# ntm:review-todo-list

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

Name a project, part of one, a few tasks, or something already reviewed to look
at again; the estimator's "What to review" says more. If you name nothing, the
review proposes a project.

## Running the review

The review procedure lives in the estimator agent's file. An agent can't talk
with the user, so this skill runs the procedure here in the chat instead.

1. Load `ntm:conventions`.
2. Read the estimator's file, `agents/estimator.md`, found as the conventions'
   "Chat, jobs and agents" says.
3. Follow the section headed Review with the user, starting at its Setup
   subsection. Pass on what to review, if the user named it.
