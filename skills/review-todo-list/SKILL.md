---
name: review-todo-list
description: >-
    Reviews the user's todo list with them in chat: closes obsolete or duplicate
    tasks, then sizes and splits unreviewed ones with their approval. Run by the
    user in chat, never by a job ("let's review my list", "review the kitchen
    project", "size the garage work").
---

# ntm:review-todo-list

## Usage

```
/ntm:review-todo-list [<what to review, in words>]
```

What to review is a project, part of one, or a few tasks; see What to review in
the planner's Review. Without it, the review proposes one.

## Running the review

The planner agent owns reviewing: the procedure is the Review section of its
file, and the task review log is what it learns. Reviewing needs the user's
answers, and an agent can't hold a conversation with them, so this skill brings
the review into the chat.

Read the planner's file (`agents/planner.md`, found as the conventions' "Chat,
jobs and agents" says) and follow its Review section with the user, here in the
chat, starting at its Setup. Pass on what to review, if the user named it.
