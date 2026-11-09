# Self-test: price watch steps

Run after step 16, the same way: one line each, stop at the first failure and go
to Cleanup.

## 17: watch

Ask `ntm-user:backend` to add the $price-watch label to ABC-12, then ask it for
the watched items. Pass when ABC-12 is among them. If the backend rejects the
label, the why is `price-watch label missing; run /ntm:setup`.

## 18: unwatch

Ask `ntm-user:backend` to remove the same label from ABC-12, then ask it for the
watched items again. Pass when ABC-12 is no longer among them.

## Cleanup

If step 17 added the label and step 18 didn't remove it, ask `ntm-user:backend`
to remove it.
