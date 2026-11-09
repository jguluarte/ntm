# Self-test: price watch steps

Run after step 16, the same way: one line each, stop at the first failure and go
to Cleanup.

## 17: watch

Step 7 closed ABC-12, and the watched items are open tasks only. Ask
`ntm-user:backend` to change ABC-12's status back to an open one, add the
$price-watch label to it, then ask for the watched items. Pass when ABC-12 is
among them. If the backend rejects the label, the why is
`price-watch label missing; run /ntm:setup`.

## 18: unwatch

Ask `ntm-user:backend` to remove the same label from ABC-12, then ask it for the
watched items again. Pass when ABC-12 is no longer among them and task ABC-12 no
longer shows the label.

## Cleanup

If step 17 added the label and step 18 didn't remove it, ask `ntm-user:backend`
to remove it. The task's own cleanup cancels it, open or not.
