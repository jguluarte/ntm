---
name: self-test
description: >-
    Exercises the whole ntm loop on a throwaway task and a throwaway database,
    comments, labels and one agent included, one line per step, and ends with
    Self-test OK or the first step that failed. The first thing to run after
    installing ntm and ntm-user ("test ntm", "run the self test", "is everything
    wired up?"), and the smoke test for a backend the user described themselves.
---

# ntm:self-test

Runs every skill a job uses, the requests to `ntm-user:backend` they need on
tasks, comments, labels and databases, and one of the plugin's agents, once, on
a task and a database made for the purpose and canceled and emptied at the end.
Run it in chat, in a new chat after installing `ntm-user`: it's the first thing
to run after install, and the thing to run again after `ntm-user` is rebuilt.

## Usage

```
/ntm:self-test
```

## What it uses

- `ntm-user:backend`, asked in plain words for what each step needs.
- One throwaway task, titled `ntm self-test`, labeled with the $no-autoschedule
  label by the name `ntm-user:backend` gives it, in no project. Keep its id once
  created; `ABC-12` below stands for it.
- One throwaway database, titled `ntm self-test`, at list level. It's not one of
  the user's databases; only this skill knows it, and its first write creates
  it.
- If an earlier run left either behind (every open item includes a task with
  that title; reading the database finds it), remove them first, as Cleanup
  says, so this run starts clean.

## Steps

Run in order. Each ends with one line, `<n>. <step>: pass` or
`<n>. <step>: FAIL: <why>`. Stop at the first failure and go to Cleanup. A call
that fails for a backend reason (a timeout, a server error) gets one retry, as
`ntm-user:backend` says; a second failure is the step's failure. An answer of
`Backend CAN'T: <why>` fails the step with that why.

### 1: ready-check

`/ntm:ready-check`. Pass on `Ready-check OK` or `Ready-check OK (no style)`; the
text after `Ready-check FAILED:` is the why.

### 2: create task

Ask `ntm-user:backend` to create a task with the title, a one-line description
(`ntm self-test, <today>; safe to remove`), the label, and nothing else. Create
it new; a canceled one from an earlier run is not a match. Pass when it comes
back with an id. If the backend rejects the label, the why is
`no-autoschedule label missing; run /ntm:setup`.

### 3: plan

`/ntm:plan put ABC-12 on today and move nothing else`. The user asked for this
test, so that is their approval. Take the plan it proposes as approved when it
dates only that task, paused day or not; otherwise answer that only ABC-12
moves, and approve that. The $no-autoschedule label doesn't stop it; in chat the
user has the final say. Pass when task ABC-12, asked of `ntm-user:backend`,
shows the planned date as today.

### 4: today

`/ntm:today`. Pass when a line starts with `ABC-12`.

### 5: style

```
/ntm-user:style --for morning
    "Morning reminder; self-test, ABC-12 planned for today"
    ABC-12 is planned for today
```

Pass when the output contains `ABC-12` and ends with a `Title:` line. When
`ntm-user:style` won't load, the line is `5. style: skipped (no style)` and the
next step uses the message as given with the title `Morning reminder`. Keep the
message and the title for the next step.

### 6: notify

Read Channel in Notifications in your settings first. On `pushover`,
`/ntm:notify --title "<the title>" --message "<the message>"`. Pass on `Sent:`,
as `6. notify: pass (push sent; check your phone)`. Nobody waits for the phone:
the user asked for this test, so one push is expected, and whether it arrived is
theirs to confirm. On the `claude-push` channel, run `ntm:notify` anyway; it
returns its delivery block instead of sending. Show the block and pass as
`6. notify: pass (claude-push; shown, not sent)`. `Notify FAILED` is the why.

### 7: close

Ask `ntm-user:backend` to change ABC-12's status to done. Pass when task ABC-12
shows it closed.

### 8: completed

`/ntm:show-completed today`. Pass when `ABC-12` is listed under `Done`.

### 9: fix-todo-list

`/ntm:fix-todo-list --dry-run`. Pass on `Dry run <today>:` with any lines, or
`Dry run <today>: nothing to fix.`; `Fix-todo-list FAILED` is the why.

### 10: pause --check

`/ntm:pause --check`. Pass on one `<today>: true` or `<today>: false` line.

### 11: database

Ask `ntm-user:backend` to write the throwaway database with the content
`self-test <today>`, then to read it. Pass when the read returns the same
content.

### 12: write comment

Ask `ntm-user:backend` to add the comment `ntm self-test comment, <today>` to
ABC-12. Pass when task ABC-12 shows it; keep its id.

### 13: update comment

Ask `ntm-user:backend` to change that comment, by its id, to
`ntm self-test comment, <today>, updated`. Pass when task ABC-12 shows the new
text.

### 14: add label

Ask `ntm-user:backend` to add the $pending-shipment label to ABC-12. Pass when
task ABC-12 shows it. If the backend rejects the label, the why is
`pending-shipment label missing; run /ntm:setup`.

### 15: remove label

Ask `ntm-user:backend` to remove the same label from ABC-12. Pass when task
ABC-12 no longer shows it and still shows the $no-autoschedule label.

### 16: agent

Ask the estimator agent for an Estimate, a time, for ABC-12, with its id, title
and description. Pass on a `time: ABC-12 ~<time>` line. When the estimator agent
isn't available in this session, read `agents/estimator.md` from the newest
installed `ntm` and follow it yourself, and end the line
`(no agent here; followed agents/estimator.md)`.

## Cleanup

Always, whether the steps passed or stopped, and in this order; one line each,
`cleanup: <what>` or `cleanup: couldn't <what>: <why>`.

- **The task:** if it was created, ask `ntm-user:backend` to change its status
  to canceled, so it never counts as work done (leave it done when the todo list
  has no canceled status). When `ntm-user:backend` keeps databases in tasks,
  cancel the database's task the same way.
- **The database:** if it was written, ask `ntm-user:backend` to write it empty.
- **The label:** if step 14 added it and step 15 didn't remove it, ask
  `ntm-user:backend` to remove it.

Nothing else on the todo list is touched: the test dates, comments on, labels,
closes and cancels its own task and empties its own database only, plus the one
history entry the style writes in step 5, which ages out. The estimator only
answers; it writes nothing.

## Result

After the cleanup lines, one line:

- `Self-test OK`
- `Self-test FAILED at <step>: <why>`, the step being the number and name from
  Steps.

On a failure, add one line with the fix when it's plain: a `ready-check` failure
carries its own fix; a missing label is `/ntm:setup`; a notify failure is
`/ntm:configure-notifications`; a request that errored on a backend of your own
means its calls in `ntm-user:backend` need correcting, with `/ntm:setup`.
