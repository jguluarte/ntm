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

Name a project, part of one, or a few tasks. With nothing, the review proposes
one.

## Running the review

The estimator agent owns the review procedure. The review needs the user's
answers, and an agent can't talk with them, so it runs here in the chat.

1. Load `ntm:conventions`.
2. Read the estimator's file, `agents/estimator.md`, found as the conventions'
   "Chat, jobs and agents" says.
3. Follow its Review section with the user, starting at Setup. Pass on what to
   review, if the user named it.
