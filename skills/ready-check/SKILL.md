---
name: ready-check
description: >-
    Proves this session can run an ntm job: the user's settings load, the
    backend connector is present, and the todo list answers. Run at the start of
    a scheduled run, or by hand ("can you see my todo list?", "check the
    connection", "is ntm ready?").
---

# ntm:ready-check

## Usage

```
/ntm:ready-check [--notify-failure "<job name>"]
```

`--notify-failure "<job name>"` sends a failure through `ntm:notify`, from the
job named, such as `"Morning reminder"`. Without it, nothing is sent.

## The check

Stop at the first failure.

1. **Load `ntm:conventions`.** If it won't load: **Dependency missing**. Its
   first step loads `ntm-user:settings`; if that won't load (it says "not
   configured"): **Not configured**.
2. **Find the connector's tool.** The backend guide's `ping` names it; with no
   guide, Todo list in your settings does. If it isn't loaded, search for it
   with ToolSearch. Still missing: **Connector not attached**.
3. **Ping the todo list** as the guide's `ping` says. It passes when the todo
   list named by List name in Todo list comes back. A different todo list:
   **Wrong account**.
4. **If the call errors,** classify it as the guide's `ping` says:
    - Authentication or authorization (unauthorized, forbidden, invalid or
      expired token): **Sign-in expired**.
    - Todo list not found: **Wrong account**.
    - Anything else (a timeout, a server error): retry once. If a todo list
      comes back, judge it as in step 3. Another error is classified as above,
      except that anything else is now **Backend error**.
5. **Load `ntm-user:style`.** It's optional: if it won't load, the check still
   passes, as `(no style)`.

## Result

End with one result line, after the notification if there is one:

- Pass: `Ready-check OK`, or `Ready-check OK (no style)`
- Fail: `Ready-check FAILED: <failure> — <fix>`

The fix for each failure:

- **Dependency missing:** The ntm:conventions skill couldn't be loaded. Check
  the ntm plugin is installed and enabled.
- **Not configured:** ntm-user:settings couldn't be loaded. Run /ntm:configure
  and install the ntm-user plugin it produces.
- **Connector not attached:** The backend connector isn't in this session.
  Connect it as /ntm:configure-todo-list shows; for a scheduled task, attach it
  there.
- **Sign-in expired:** The backend rejected the connector's sign-in. Reconnect
  the connector.
- **Wrong account:** The connector can't see the todo list named in Todo list in
  your settings. Reconnect it with the account that owns that todo list.
- **Backend error:** The backend returned <the error, shortened> on retry.
  Usually temporary; if it repeats, check the backend's status page.

## With `--notify-failure`

When the check fails, load `ntm:notify` and run `/ntm:notify` with:

- `--from "<job name>"`
- `--title "<List name> — <job name> failed"`
- `--message "<job name>: <failure>. <fix>"`

If `ntm:notify` can't be loaded or the send fails, append
`(notification not sent: <reason>)` to the result line.

With the `claude-push` channel, `ntm:notify` sends nothing and returns
`NOTIFY VIA FINAL REPLY` with the title and message. That's not a failure:
return the result line, then the title and the message (not the marker line).
The job ends its run with that, so the failure shows once, as the completion
push.
