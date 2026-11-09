---
name: ready-check
description: >-
    Proves this session can run an ntm job: the user's plugin loads, the backend
    connector is present, and the todo list answers. Run at the start of a
    scheduled run, or by hand ("can you see my todo list?", "check the
    connection", "is ntm ready?").
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

Load `ntm-user:backend` to read the user's conventions. If it can't be loaded:
**Not configured**.

### 2: Find the connector's tools

The ping in `ntm-user:backend` names the tool it uses. If that tool isn't
loaded, search for it with ToolSearch. If it still isn't there: **Connector not
attached**, or **Sign-in expired** when the connector looks the way
`ntm-user:backend` describes one waiting on a sign-in.

### 3: Ping the todo list

Ping the todo list as `ntm-user:backend` says. If it fails, sort the failure the
way it says: **Sign-in expired**, **Wrong account** or **Backend error**. On a
backend error, ping once more, and sort a second failure the same way.

### 4: Load `ntm-user:style`

It's optional: if it won't load, the check still passes, as `(no style)`.

## Result

End with one result line, after the notification if there is one:

- Pass: `Ready-check OK`, or `Ready-check OK (no style)` when `ntm-user:style`
  didn't load
- Fail: `Ready-check FAILED: <failure> — <fix>`

The failures, and the fix for each, unless `ntm-user:backend` gives its own:

### Not configured

ntm-user:backend couldn't be loaded. Run /ntm:setup and install the ntm-user
plugin it produces.

### Connector not attached

The todo list's connector isn't in this session. For a scheduled task, attach it
there; otherwise connect it again.

### Sign-in expired

The backend rejected the connector's sign-in. Reconnect the connector.

### Wrong account

The connector can't see the todo list named in `ntm-user:backend`. Reconnect it
with the account that owns that todo list.

### Backend error

The backend returned <the error, shortened> on retry. Usually temporary; if it
repeats, check the backend's status page.

## With `--notify-failure`

When the check fails, load `ntm-user:notify` and run:

```
/ntm-user:notify --from <skill> --title "<List name> — <name> failed"
    --message "<name>: <failure>. <fix>"
```

`<name>` is the skill's name in plain words: `morning-reminder` becomes Morning
reminder. `<List name>` is the todo list's name in `ntm-user:backend`.

This is the one error that may use the notification channel; a job reports every
later error in its final reply instead. If `ntm-user:notify` can't be loaded or
the send fails, append `(notification not sent: <reason>)` to the result line.

When `ntm-user:notify` puts the notification in the final reply instead of
sending it, that's not a failure: end with the result line, then the title and
the message, without the `NOTIFY VIA FINAL REPLY` line. A job that ends its run
with what this check returned then shows the failure once, as the completion
push.
