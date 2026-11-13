---
name: self-test
description: >-
    A test that the user's setup is complete and their task list can do what
    every backend must: check setup made their databases, labels and jobs, then
    create, read, find, plan, label, comment on, change and close a throwaway
    task, and write and read a throwaway database, then clean up and send a
    success message in the user's style. Each step's result is shown as it
    passes or fails. The first thing to run after installing ntm and ntm-user
    ("test ntm", "run the self test", "is everything wired up?"), and the smoke
    test for a backend the user described themselves.
---

# ntm:self-test

A test that this user's setup is complete, and that their task list can do the
core interactions every backend must support, on a task and a database made for
the purpose. Run it in a new chat after installing `ntm-user`, and again after
`ntm-user` is rebuilt. Never run it unasked: a run writes to the task list, and
sends a push. Once the user starts it, run it without asking.

## Usage

```
/ntm:self-test
```

## Test execution steps

Do each step on the task list as `ntm-user:backend` teaches. Step 1 loads it,
ntm's core rules and `%Settings`, which holds the user's label names.
`<timestamp>` is the date and time the run starts, to the second, in the user's
timezone, like `2026-11-09 14:03:27`.

Run the steps in order. As each one finishes, tell the user in one line what it
tested and whether it passed, like "3. Create a task: the task list takes a new
task. Pass." A call that fails for a backend reason gets one retry. At the first
failure, say why and skip to step 12.

### 1. Connectivity

Follow `/ntm:ready-check`. The step passes when you reach `Ready-check OK`.

### 2. What setup made

The step passes when setup made everything it was supposed to: every database
`ntm-user:backend` says where it lives opens, and every label under Labels in
`%Settings` is on the task list, by its name there. Name each one that's
missing.

Then look for their jobs among their scheduled tasks, knowing each by the `ntm:`
skills it runs. With Planning in `%Settings`, expect the weekly setup and the
morning, afternoon and evening reminders; with Shopping, the price watch. A job
you don't find doesn't fail the step. When you can't see their scheduled tasks,
say you couldn't check the jobs, and go on.

### 3. Create a task

Create the below task. It should get an id.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test, <timestamp>               |
| Description | This is a test, it can safely be removed |
| Project     | none                                     |

### 4. Read it back

The task shows the title and description from step 3.

### 5. Find it

It is among the open tasks.

### 6. Plan it

Plan it for today, and it is among the open tasks planned for today. Then clear
its planned date, and it has none.

### 7. Label it

Add the label `ntm-self-test`, creating it when the task list doesn't have it
yet, and the task shows it. Then remove it, and the task has no labels.

### 8. Comment on it

Comment on it, then change the comment's text, and the task's comments show the
new text.

### 9. Change it

Change its description to `This is a changed test, it can safely be removed`,
and the task shows it.

### 10. Store data

Write the below database, into the one an earlier self-test left behind or a new
one when there isn't one, then find it by its title, and it holds the contents.

| Field    | Value                      |
| -------- | -------------------------- |
| Title    | ntm self-test database     |
| Contents | ntm self-test, <timestamp> |

### 11. Close it

Cancel the test task, or mark it done when the task list has no canceled status,
and it is among the tasks closed today, canceled included.

### 12. Clean up

Runs after a failure too. Cancel the task if it's still open, and delete the
test label and the test database. When the task list can't delete them, take the
label off the task and empty the database, for a rerun to reuse. Do the same for
any test task an earlier self-test left behind. Touch nothing else on the task
list.

It fails when anything can't be cleaned up: a run that leaves its test data
behind didn't pass.

### 13. Send the success message

Only when every step before it passed. Send it as the core rules' Sending a
message in the user's style says. Its one fact is
`ntm is ready; the self-test passed`. It passes when `ntm-user:notify` returns
`Sent:`, or its `NOTIFY VIA FINAL REPLY` block, which you show the user. Any
other return fails the step.

## Result

`Self-test OK`, or `Self-test FAILED at <n>. <step>: <why>`. On a failure, add
the fix when it's plain: for a ready-check failure, the fix in its failure line,
which is `/ntm:setup` when `ntm-user` isn't installed; for anything missing from
the user's setup, or a call that errored on a backend the user described
themselves, telling ntm in chat what to fix.

When step 2 didn't find some jobs, add one line naming them, and how to schedule
them if they want them. For example:

> No weekly setup or reminders are scheduled. If you want them, run `/ntm:setup`
> again, or tell ntm to set them up.
