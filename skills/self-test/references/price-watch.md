# Self-test: price watch steps

Run after step 16, the same way: one line each, stop at the first failure and go
to Cleanup.

## 17: watch

Step 7 closed ABC-12, and the watched items are open tasks only. `set status` on
ABC-12 back to an open one, then `add labels` with the $price-watch label, by
its real name in `ntm-user:backend`. Then find the watched items, as
`ntm-user:backend` says. Pass when ABC-12 is among them. If the backend rejects
the label, the why is `price-watch label missing; run /ntm:setup`.

## 18: unwatch

`remove labels` on ABC-12 with the same label, then find the watched items
again. Pass when ABC-12 is no longer among them and `read task` no longer shows
the label.

## Cleanup

If step 17 added the label and step 18 didn't remove it, `remove labels` it. The
task's own cleanup cancels it, open or not.
