---
name: self-test
description: >-
    Tests that the user's task list can do what ntm needs, step by step on a
    throwaway task and database, ending with cleanup and a success message. The
    first thing to run after setup and after each rebuild ("test ntm", "run the
    self test", "is everything wired up?"), and the smoke test for a backend the
    user described themselves.
---

# ntm:self-test

A test that the user's task list can do the core interactions every backend must
support, on a task and a database made for the purpose.

A run writes to the task list and sends a push, so run it only when the user
asks. Once they do, run it to the end without asking.

## Usage

```
/ntm:self-test
```

## Setup

Load `ntm-user:backend` to read the user's conventions. When it won't load,
nothing is set up to test yet: run no steps, and return the base-only result.

## Test steps

As each step finishes, tell the user in one line what it tested and whether it
passed, like "2. Create a task: the task list takes a new task. Pass." At the
first failure, say why and go to step 13.

`<timestamp>` is when the run started, to the second, in the user's timezone,
like `2026-11-09 14:03:27`.

### 1. Connectivity

Load `ntm:ready-check` and follow it. The step passes on `Ready-check OK`.

### 2. Create a task

Create the task below. It comes back with an id.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test, <timestamp>               |
| Description | This is a test, it can safely be removed |
| Label       | $no-autoschedule                         |
| Project     | none                                     |

The label keeps planners from picking it.

### 3. Read it back

Reading it shows the title, description and label from step 2.

### 4. Find it

It's among the open tasks.

### 5. Plan it

Plan it for today: it's among the open tasks planned for today. Then clear its
planned date: reading it shows none.

### 6. Label it

Add another of the user's labels: reading it shows both. Then remove that label:
only $no-autoschedule is left.

### 7. Comment on it

Comment on it, then change the comment's text: its comments show the new text.

### 8. Change it

Replace its description with `This is a changed test, it can safely be removed`
and the estimate line `Estimate: 1 hour` under it: reading it shows both.

### 9. Add a sub-task

Create the task below. It comes back with an id, and reading it shows the test
task as its parent.

| Field       | Value                                    |
| ----------- | ---------------------------------------- |
| Title       | ntm self-test sub-task, <timestamp>      |
| Description | This is a test, it can safely be removed |
| Label       | $no-autoschedule                         |
| Parent      | the test task                            |

### 10. Mark it a duplicate

Mark the sub-task a duplicate of the test task: it's among the tasks closed
today, duplicates included.

### 11. Store data

Write the database below: reading it back returns its contents.

| Field    | Value                      |
| -------- | -------------------------- |
| Title    | ntm self-test database     |
| Project  | none                       |
| Contents | ntm self-test, <timestamp> |

### 12. Close it

Cancel the test task: it's among the tasks closed today, canceled ones included.

### 13. Clean up

Runs after a failure too. Cancel the test task and sub-task if they're still
open, and any open task an earlier self-test left behind. Take the added label
off if it's still on. Empty the test database, and cancel its task too when
databases live in tasks. Touch nothing else on the task list.

The step fails when anything can't be cleaned up: a run that leaves its test
data behind didn't pass.

### 14. Send the success message

Only when every step before it passed. Ask the messenger agent:

```
type: freeform
job: self-test
message: ntm is ready; the self-test passed
```

The step passes when the messenger returns `Sent:`, or a delivery block, which
you show the user. Anything else fails it.

## Result

One line:

| Result                                                            | When                       |
| ----------------------------------------------------------------- | -------------------------- |
| `Self-test OK`                                                    | every step passed          |
| `Self-test OK (base only): nothing is set up yet; run /ntm:setup` | `ntm-user` isn't installed |
| `Self-test FAILED at <n>. <step>: <why>`                          | step `<n>` failed first    |

On a failure, add the fix when it's plain: ready-check's own fix, or
`/ntm:setup` for a missing label or for a step that fails on a backend the user
described themselves.
