---
name: ready-check
description: >-
    Proves this session can run an ntm job: the user's plugin loads and the todo
    list answers. Run at the start of a scheduled run, or by hand ("can you see
    my todo list?", "check the connection", "is ntm ready?").
---

# ntm:ready-check

## Usage

```
/ntm:ready-check [--notify-failure <skill>]
```

- `--notify-failure <skill>`: on failure, send the result through
  `ntm-user:notify`, for the skill named, such as `morning-reminder`. Without
  it, nothing is sent.

## The check

Stop at the first failure.

### 1: Load `ntm-user:backend`

If it can't be loaded: **Not configured**.

### 2: Ping the todo list

Ask `ntm-user:backend` to ping, and make the call it gives. If that call's tool
isn't loaded, search for it with ToolSearch. If it still isn't there:
**Connector not attached**.

If the ping answers `Backend CAN'T: <why>` and the why is a backend error, ask
once more. A second `Backend CAN'T: <why>`, or any other why, fails the check as
`<why>`.

### 3: Load `ntm-user:style`

It's optional: if it won't load, the check still passes, as `(no style)`.

## Result

End with one result line, after the notification if there is one:

- Pass: `Ready-check OK`, or `Ready-check OK (no style)` when `ntm-user:style`
  didn't load
- Fail: `Ready-check FAILED: <failure> — <fix>`, or `Ready-check FAILED: <why>`
  for a ping's why, which carries its own fix

The failures of its own, and the fix for each:

### Not configured

ntm-user:backend couldn't be loaded. Run /ntm:setup and install the ntm-user
plugin it produces.

### Connector not attached

The todo list's connector isn't in this session. For a scheduled task, attach it
there; otherwise connect it again.

## With `--notify-failure`

When the check fails, load `ntm-user:notify` and run:

```
/ntm-user:notify --from <skill> --title "<List name> — <name> failed"
    --message "<name>: <failure>. <fix>"
```

`<name>` is the skill's name in plain words: `morning-reminder` becomes Morning
reminder. `<List name>` is the todo list's name in `ntm-user:backend`. For a
ping's why, the message is `<name>: <why>`.

This is the one error that may use the notification channel; a job reports every
later error in its final reply instead. If `ntm-user:notify` can't be loaded, or
returns `Notify FAILED` or `Notify TOO LONG`, append
`(notification not sent: <reason>)` to the result line.

When `ntm-user:notify` returns `NOTIFY VIA FINAL REPLY` with the title and
message, that's not a failure: return the result line, then the title and the
message (not the marker line). A job that ends its run with what this check
returned then shows the failure once, as the completion push.
