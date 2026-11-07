---
name: self-test
description: >-
    Exercises the whole ntm loop on a throwaway task and a throwaway database,
    one line per step, and ends with Self-test OK or the first step that failed.
    The first thing to run after installing ntm and ntm-user ("test ntm", "run
    the self test", "is everything wired up?"), and the smoke test for a backend
    the user described themselves.
---

# ntm:self-test

Runs every skill a job uses, and every backend operation they need, once, on a
task and a database made for the purpose and canceled and emptied at the end.
Run it in chat, in a new chat after installing `ntm-user`: it's the first thing
to run after install, and the thing to run again after changing Todo list in
your settings.

## Usage

```
/ntm:self-test
```

## What it uses

- Load `ntm:conventions` and compute `TODAY` as its Dates section says.
- One throwaway task, titled `ntm self-test`, labeled with the $no-autoschedule
  label by its real name from Labels in your settings, in no project. Keep its
  id once created; `ABC-12` below stands for it.
- One throwaway database, titled `ntm self-test`, at list level. It's not one of
  the databases in `ntm:conventions`; only this skill knows it.
- If an earlier run left either behind (`fetch open` shows a task with that
  title; `read database` finds the database), remove them first, as Cleanup
  says, so this run starts clean.

## Steps

Run in order. Each ends with one line, `<n>. <step>: pass` or
`<n>. <step>: FAIL: <why>`. Stop at the first failure and go to Cleanup. A call
that fails for a backend reason (a timeout, a server error) gets one retry, as
the conventions say; a second failure is the step's failure.

1. **ready-check:** `/ntm:ready-check`. Pass on `Ready-check OK` or
   `Ready-check OK (no style)`; the text after `Ready-check FAILED:` is the why.
2. **create task:** the guide's `create task` with the title, a one-line
   description (`ntm self-test, <TODAY>; safe to remove`), the label, and
   nothing else. Create it new; a canceled one from an earlier run is not a
   match. Pass when it comes back with an id. If the backend rejects the label,
   the why is `no-autoschedule label missing; run /ntm:configure-todo-list`.
3. **plan:** `/ntm:plan put ABC-12 on today and move nothing else`. The user
   asked for this test, so that is their approval. Take the plan it proposes as
   approved when it dates only that task, paused day or not; otherwise answer
   that only ABC-12 moves, and approve that. The $no-autoschedule label doesn't
   stop it; in chat the user has the final say. Pass when `read task` shows the
   planned date as `TODAY`.
4. **today:** `/ntm:today`. Pass when a line starts with `ABC-12`.
5. **style:**
   `/ntm-user:style --for morning "Morning reminder; self-test, ABC-12 planned for today" ABC-12 is planned for today`.
   Pass when the output contains `ABC-12` and ends with a `Title:` line. When
   `ntm-user:style` won't load, the line is `5. style: skipped (no style)` and
   the next step uses the message as given with the title `Morning reminder`.
   Keep the message and the title for the next step.
6. **notify:** read Channel in Notifications in your settings first. On
   `pushover`, `/ntm:notify --title "<the title>" --message "<the message>"`.
   Pass on `Sent:`, as `6. notify: pass (push sent; check your phone)`. Nobody
   waits for the phone: the user asked for this test, so one push is expected,
   and whether it arrived is theirs to confirm. On the `claude-push` channel,
   run `ntm:notify` anyway; it returns its delivery block instead of sending.
   Show the block and pass as `6. notify: pass (claude-push; shown, not sent)`.
   `Notify FAILED` is the why.
7. **close:** `set status` to the done status from Todo list. Pass when
   `read task` shows it closed.
8. **completed:** `/ntm:show-completed today`. Pass when `ABC-12` is listed
   under `Done`.
9. **fix-todo-list:** `/ntm:fix-todo-list --dry-run`. Pass on `Dry run <TODAY>:`
   with any lines, or `Dry run <TODAY>: nothing to fix.`; `Fix-todo-list FAILED`
   is the why.
10. **pause --check:** `/ntm:pause --check`. Pass on one `<TODAY>: true` or
    `<TODAY>: false` line.
11. **database:** `write database` on the throwaway database with the content
    `self-test <TODAY>`, then `read database` returns the same content. Pass
    when it does.

## Cleanup

Always, whether the steps passed or stopped, and in this order; one line each,
`cleanup: <what>` or `cleanup: couldn't <what>: <why>`.

- **The task:** if it was created, `set status` to the canceled status from Todo
  list, so it never counts as work done (leave it done when Todo list's canceled
  line is blank). Where the backend keeps databases in tasks, cancel the
  database's task the same way.
- **The database:** if it was written, `write database` it empty.

Nothing else on the todo list is touched: the test dates, closes and cancels its
own task and empties its own database only, plus the one history entry the style
writes in step 5, which ages out.

## Result

After the cleanup lines, one line:

- `Self-test OK`
- `Self-test FAILED at <step>: <why>`, the step being the number and name from
  Steps.

On a failure, add one line with the fix when it's plain: a `ready-check` failure
carries its own fix; a missing label is `/ntm:configure-todo-list`; a notify
failure is `/ntm:configure-notifications`; a backend operation that errored on a
backend of your own means the operation's description under Todo list needs
correcting, with `/ntm:configure-todo-list`.
