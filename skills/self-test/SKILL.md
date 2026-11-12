---
name: self-test
description: >-
    A test that the user's setup is complete and their task list can do what
    every backend must: check that setup made their databases and labels, then
    create, read, find, plan, label, comment on, estimate, change and close a
    throwaway task, and write and read a throwaway database, then clean up and
    have the messenger agent send a success message. Each step's result is shown
    as it passes or fails. The first thing to run after installing ntm and
    ntm-user ("test ntm", "run the self test", "is everything wired up?"), and
    the smoke test for a backend the user described themselves.
---

# ntm:self-test

A test that this user's setup is complete, and that their task list can do the
core interactions every backend must support, on a task and a database made for
the purpose. Run it in a new chat after installing `ntm-user`, and again after
`ntm-user` is rebuilt. Never run it unasked: a run writes to the task list, and
the messenger agent sends a push. Once the user starts it, run it without
asking.

## Usage

```
/ntm:self-test
```

## Test execution steps

Do each step on the task list as `ntm-user:backend` teaches. Step 1 loads it and
`%Settings`, which holds the user's label names. `<timestamp>` is the date and
time the run starts, to the second, in the user's timezone, like
`2026-11-09 14:03:27`.

Run the steps in order. As each one finishes, tell the user in one line what it
tested and whether it passed, like "3. Create a task: the task list takes a new
task. Pass." A call that fails for a backend reason gets one retry. At the first
failure, say why and skip to step 12.

### 1. Connectivity

Follow `/ntm:ready-check`. The step passes when you reach `Ready-check OK`.

### 2. What setup made

The step passes when setup made everything it was supposed to: every database
`ntm-user:backend` lists opens, and every label under Labels in `%Settings` is
on the task list, by its name there. Name each one that's missing.

### 3. Create a task

Create the below task. It should get an id.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test, <timestamp>               |
| Description | This is a test, it can safely be removed |
| Label       | `$no-autoschedule`, by its real name     |
| Project     | none                                     |

The label keeps anything from planning it.

### 4. Read it back

The task shows the title, description and label from step 3.

### 5. Find it

It is among the open tasks.

### 6. Plan it

Plan it for today, and it is among the open tasks planned for today. Then clear
its planned date, and it has none.

### 7. Label it

Add another of the user's labels, and the task shows both. Then remove it, and
only `$no-autoschedule` is left.

### 8. Comment on it

Comment on it, then change the comment's text, and the task's comments show the
new text.

### 9. Change it

Change its description to `This is a changed test, it can safely be removed`,
with the estimate line `Estimate: 2 hours` at its end, and the task shows both.

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

Runs after a failure too. Cancel the task if it's still open, remove the added
label if it's still on, and delete the test database, or empty it when the task
list can't delete one. Do the same for any test task or database an earlier
self-test left behind. Touch nothing else on the task list.

It fails when anything can't be cleaned up: a run that leaves its test data
behind didn't pass.

### 13. Send the success message

Only when every step before it passed. Ask the messenger agent for a `freeform`
message: `ntm is ready; the self-test passed`. It passes when the messenger
returns `Sent:`, or a delivery block, which you show the user. Any other return
fails the step.

## Result

One line: `Self-test OK`, or `Self-test FAILED at <n>. <step>: <why>`. On a
failure, add the fix when it's plain: for a ready-check failure, the fix in its
failure line, which is `/ntm:setup` when `ntm-user` isn't installed; for
anything missing from the user's setup, or a call that errored on a backend the
user described themselves, `/ntm:update`.
