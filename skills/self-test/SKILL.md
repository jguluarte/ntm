---
name: self-test
description: >-
    A test that the user's task list can do what every backend must: create,
    read, find, plan, label, comment on, estimate, change and close a throwaway
    task, give it a sub-task and mark that a duplicate, and write and read a
    throwaway database, then clean up and have the messenger agent send a
    success message. Each step's result is shown as it passes or fails. The
    first thing to run after installing ntm and ntm-user ("test ntm", "run the
    self test", "is everything wired up?"), and the smoke test for a backend the
    user described themselves.
---

# ntm:self-test

A test that this user's task list can do the core interactions every backend
must support, on a task and a database made for the purpose. Run it in a new
chat after installing `ntm-user`, and again after `ntm-user` is rebuilt. Never
run it unasked: a run writes to the task list, and the messenger agent sends a
push. Once the user starts it, run it without asking.

## Usage

```
/ntm:self-test
```

## Test execution steps

Load `ntm-user:backend`, and do each step with the operations described in it.
`<timestamp>` is the date and time the run starts, to the second, in the user's
timezone, like `2026-11-09 14:03:27`.

Run the steps in order. As each one finishes, tell the user in one line what it
tested and whether it passed, like
`2. Create a task: the task list takes a new task. Pass.` A call that fails for
a backend reason gets one retry, as described in `ntm-user:backend`. At the
first failure, say why and skip to step 13.

### 1. Connectivity

Follow `/ntm:ready-check`. The step passes when you reach `Ready-check OK`.

### 2. Create a task

Use `create task` to make the below task. It should return an id.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test, <timestamp>               |
| Description | This is a test, it can safely be removed |
| Label       | $no-autoschedule, by its real name       |
| Project     | none                                     |

The label keeps anything from planning it.

### 3. Read it back

`read task` shows the title, description and label from step 2.

### 4. Find it

`fetch open` lists it among the open tasks.

### 5. Plan it

`set planned date` to today, and `fetch open` shows it planned for today. Then
`clear planned date`, and `read task` shows no date.

### 6. Label it

`add labels` with another of the user's labels, and `read task` shows both. Then
`remove labels` with it, and only $no-autoschedule is left.

### 7. Comment on it

`write comment`, then `update comment` with new text, and `read comments` shows
the new text.

### 8. Change it

`update task` with an estimate on the user's scale and the description
`This is a changed test, it can safely be removed`, and `read task` shows both.

### 9. Add a sub-task

Use `create task` to make the below task. It should return an id, and
`read task` shows the test task as its parent.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test sub-task, <timestamp>      |
| Description | This is a test, it can safely be removed |
| Label       | $no-autoschedule, by its real name       |
| Parent      | the test task from step 2                |

### 10. Mark it a duplicate

`mark duplicate of` the sub-task as a duplicate of the test task, and
`fetch closed` for today, duplicate included, lists it.

### 11. Store data

Use `write database` to make the below database, and `read database` returns its
contents.

| Field    | Value                      |
| -------- | -------------------------- |
| Title    | ntm self-test database     |
| Level    | list                       |
| Contents | ntm self-test, <timestamp> |

### 12. Close it

`set status` to canceled, or done when the task list has no canceled status, and
`fetch closed` for today, canceled included, lists it.

### 13. Clean up

Runs after a failure too. Cancel the task and the sub-task if they're still
open, remove the added label if it's still on, and write the database empty;
when the database lives in a task, cancel that task too. Cancel any open task an
earlier self-test left behind. Touch nothing else on the task list.

It fails when anything can't be cleaned up: a run that leaves its test data
behind didn't pass.

### 14. Send the success message

Only when every step before it passed. Ask the messenger agent with
`kind: self-test`, `job: self-test` and
`message: ntm is ready; the self-test passed`. It passes when the messenger
returns `Sent:`, or a delivery block, which you show the user. A
`Messenger NEEDS` answer fails the step.

## Result

One line: `Self-test OK`, or `Self-test FAILED at <n>. <step>: <why>`. On a
failure, add the fix when it's plain: for a ready-check failure, the fix in its
failure line; for a missing label, or an operation that errored on a backend the
user described themselves, `/ntm:setup`.
