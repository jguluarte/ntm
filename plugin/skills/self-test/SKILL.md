---
name: self-test
user-invocable: false
description: >-
    Tries out everything setup built, and cleans up after itself. Run by you in
    a new chat once setup asks, after you install the plugin it built ("run the
    ntm self-test", "test ntm", "run the self test", "is everything wired up?").
    It is also the smoke test for a backend you described yourself.
---

# ntm:self-test

A test that this user's setup is complete, and that their task list can do the
core interactions every backend must support. It deletes what it makes for the
test, and puts back what it changes, so it leaves nothing behind, pass or fail.
Run it in a new chat after installing `ntm-user`, and again after `ntm-user` is
rebuilt. Never run it unasked: a run writes to the task list, and sends a push.
Once the user starts it, run it without asking, apart from step 3's one question
when there's no task to test on.

## Usage

```
/ntm:self-test
```

## Test execution steps

Do each step on the task list as `ntm-user:backend` teaches. Step 1 loads it,
ntm's core rules and `%Settings`, which holds the user's label names.
`<timestamp>` is the date and time the run starts, to the second, in the user's
timezone, like `2026-11-09 14:03:27`.

A step that makes something for the test runs only when `ntm-user:backend` says
the task list can delete it. When it doesn't run, its line says why: the task
list can't delete it, or `ntm-user:backend` doesn't say whether it can. For
example, "10. Store data: not run, the task list can't delete a database."

Run the steps in order. As each one finishes, tell the user in one line what it
tested and whether it passed, like "3. Create a task: the task list takes a new
task. Pass." A call that fails for a backend reason gets one retry. At the first
failure, say why and skip to step 13.

### 1. Connectivity

Follow `/ntm:ready-check`. The step passes when you reach `Ready-check OK`.

### 2. What setup made

Every database under Databases in `%Settings` opens, as do this week's `%Theme`
and `%Message-history`, and every label under Labels in `%Settings` is on the
task list, by its name there. Name each one that's missing.

Then look for their jobs among their scheduled tasks, knowing each by the `ntm:`
skills it runs. With Planning in `%Settings`, expect the weekly setup and the
morning, afternoon and evening reminders; with Shopping, the price watch. A job
you don't find doesn't fail the step. When you can't see their scheduled tasks,
say you couldn't check the jobs, and go on.

### 3. Create a task

When the task list can delete a task, create the below throwaway task. It should
get an id, and it is the test task.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test, <timestamp>               |
| Description | This is a test, it can safely be removed |
| Project     | none                                     |

Otherwise, the test task is one of the user's open tasks with no planned date:
note its title, description, labels and comments, to check and put back later.
The step's line names it, and says its history on the task list will show the
test's changes.

When they have none, ask:

> To test your task list, I'll add one real task to it. What's one thing you
> need to do? A few words is enough.

Create their answer as their task, titled in their words. It is the test task,
and it stays: the step's line names it and says it's theirs to keep. With no one
to answer, such as in a job, or when they'd rather not, steps 4 to 9 don't run,
and the step's line says there was no task to test on.

### 4. Read it back

The task shows the title and description from step 3.

### 5. Find it

It is among the open tasks.

### 6. Plan it

Plan it for today, and it is among the open tasks planned for today. Then clear
its planned date, and it has none.

### 7. Label it

Add one of the labels under Labels in `%Settings` that it doesn't have, and the
task shows it. Then remove it, and the task has the labels it had.

### 8. Comment on it

Comment on it, then change the comment's text, and the task's comments show the
new text. Then delete the comment, and it's gone.

### 9. Change it

Runs on the throwaway task from step 3.

Change its description to `This is a changed test, it can safely be removed`,
and the task shows it.

### 10. Store data

Write the below database, then find it by its title, and it holds the contents.

| Field    | Value                      |
| -------- | -------------------------- |
| Title    | ntm self-test database     |
| Contents | ntm self-test, <timestamp> |

### 11. Close it

Runs on the throwaway task from step 3.

Cancel the test task, or mark it done when the task list has no canceled status,
and it is among the tasks closed today, canceled included.

### 12. The backend's cleanup

Runs on the throwaway task from step 3.

Do the cleanup `ntm-user:backend` lists, on the test task alone. When the
cleanup only acts on certain tasks, make the test task one of them first. Use
what the user already has for this, such as one of their projects, and make only
what step 13 can delete. The task then shows what the cleanup says it leaves.
With no cleanup listed, the step passes, and its line says there is none.

### 13. Clean up

Runs after a failure too. Delete everything the run made for the test. When the
test task is the user's, it stays: clear its planned date, and put its labels
and comments back as they were in step 3. Touch nothing else on the task list.

It fails when anything can't be cleaned up, and its line names what's left and
on which task.

### 14. Send the success message

Only when no step before it has failed. Send it as the core rules' Sending a
message in the user's style says. Its one fact is
`ntm is ready; the self-test passed`. It passes when `ntm-user:notify` returns
`Sent:`, or its `NOTIFY VIA FINAL REPLY` block, which you show the user. Any
other return fails the step.

When `ntm:style` keeps a failure line from `ntm:refresh-picks`, send nothing:
the step fails, with that line as its why.

## Result

`Self-test OK`, or `Self-test FAILED at <n>. <step>: <why>`. On a failure, add
the fix when it's plain: for a ready-check failure, the fix in its failure line,
which is `/ntm:setup` when `ntm-user` isn't installed; for anything missing from
the user's setup, or a call that errored on a backend the user described
themselves, telling ntm in chat what to fix.

When steps didn't run, add one line naming them, and why.

When step 2 didn't find some jobs, add one line naming them, and how to schedule
them if they want them. For example:

> No weekly setup or reminders are scheduled. If you want them, run `/ntm:setup`
> again, or tell ntm to set them up.
