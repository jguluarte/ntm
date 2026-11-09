---
name: self-test
description: >-
    Checks that the user's todo list can do what every backend must: create,
    read, find, plan, label, comment on, change and close a throwaway task, and
    write and read a throwaway database. One line per check, ending with
    Self-test OK or the first check that failed. The first thing to run after
    installing ntm and ntm-user ("test ntm", "run the self test", "is everything
    wired up?"), and the smoke test for a backend the user described themselves.
---

# ntm:self-test

Proves this user's todo list can do the core interactions every backend must
support, on a task and a database made for the purpose, then cleans up. Run it
in a new chat after installing `ntm-user`, and again after `ntm-user` is
rebuilt. Never run it unasked: it writes to the todo list and sends a push. Once
the user starts it, it runs without asking.

## Usage

```
/ntm:self-test
```

## Setup

Load `ntm-user:backend` to read the user's conventions, and do each check below
with the operations it describes.

The throwaway task is titled `ntm self-test`, has no project, and carries the
$no-autoschedule label, by its real name, so nothing plans it. The throwaway
database is titled `ntm self-test database`, at list level. If an earlier run
left either behind, clean it up first, as Cleanup says.

## Checks

Run them in order. Each ends with one line, `<n>. <check>: pass` or
`<n>. <check>: FAIL: <why>`. Stop at the first failure and go to Cleanup. A call
that fails for a backend reason gets one retry, as `ntm-user:backend` says.

1. **Reach the list:** `/ntm:ready-check` returns `Ready-check OK`.
2. **Create a task:** `create task` with the title, the label and the
   description `ntm self-test, <today>; safe to remove`. It returns an id.
3. **Read it back:** `read task` shows that title, description and label.
4. **Find it:** `fetch open` lists it among the open tasks.
5. **Plan it:** `set planned date` to today, and `fetch open` shows it planned
   for today. Then `clear planned date`, and `read task` shows no date.
6. **Label it:** `add labels` with another of the user's labels, and `read task`
   shows both. Then `remove labels` with it, and only the $no-autoschedule label
   is left.
7. **Comment on it:** `write comment`, then `update comment` with new text, and
   `read comments` shows the new text.
8. **Change it:** `update task` with a new description, and `read task` shows
   it.
9. **Store data:** `write database` with `ntm self-test, <today>`, and
   `read database` returns it.
10. **Close it:** `set status` to canceled, or done when the list has no
    canceled status, and `fetch closed` for today lists it.

## Cleanup

Always, whether the checks passed or stopped. Cancel the task if it's still
open, remove the added label if it's still on, and write the database empty
(when `ntm-user:backend` keeps databases in tasks, cancel that task too). One
line each, `cleanup: <what>` or `cleanup: couldn't <what>: <why>`. Nothing else
on the todo list is touched.

## Result

After the cleanup lines, one line: `Self-test OK`, or
`Self-test FAILED at <n>. <check>: <why>`.

On a failure, add the fix when it's plain: a ready-check failure carries its
own; a missing label, or an operation that errored on a backend the user
described themselves, is `/ntm:setup`.

On `Self-test OK`, load `ntm-user:style` and write a short success message with
it: ntm is ready. Make them smile. Say it in chat, and send it with
`ntm-user:notify`; when that returns a delivery block instead, show the block.
When there's no style yet, say it plainly.
