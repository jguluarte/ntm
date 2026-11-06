---
name: ready-check
description: Proves this session can run an ntm job: the user's settings load, the backend connector is present, and the board answers. Run at the start of a scheduled run, or by hand ("can you see my board?", "check the connection", "is ntm ready?").
---

# ntm:ready-check

## Usage

```
/ntm:ready-check [--notify] [--job "<name>"]
```

- `--notify`: on failure, send the result through `ntm:notify`. Without it, nothing is sent.
- `--job "<name>"`: the job that called this check, such as `"Morning reminder"`. Defaults to `"Ready check"`.

## The check

Stop at the first failure.

1. **Load `ntm:conventions`.** If it can't be loaded: **Dependency missing**. Its first step loads `ntm-user:settings`; if that won't load (it says "not configured"): **Not configured**.
2. **Find the connector's tools.** The backend guide's `ping` names the tool it uses (for a backend with no guide, Board in your settings does). If that tool isn't loaded, search for it with ToolSearch. If it still isn't there: **Connector not attached**.
3. **Ping the board.** Carry out the guide's `ping`. If it comes back with the board named by Board name in Board in your settings, the ping passes; a different board is **Wrong account**. If the call errors, go to step 4.
4. **If the call errors,** classify it the way the guide's `ping` says:
   - An authentication or authorization error (unauthorized, forbidden, invalid or expired token): **Sign-in expired**.
   - The board isn't found: **Wrong account**.
   - Anything else (a timeout, a server error): retry once. If the retry returns a board, apply step 3 to it. If it errors, classify an authentication or not-found error as above, and anything else as **Backend error**.
5. **Load `ntm-user:style`.** It's optional: if it won't load, the check still passes, as `(no style)`.

## Result

End with one result line, after the notification if there is one:

- Pass: `Ready-check OK`, or `Ready-check OK (no style)` when `ntm-user:style` didn't load
- Fail: `Ready-check FAILED: <failure> — <fix>`

| Failure | Fix |
|---|---|
| Dependency missing | The ntm:conventions skill couldn't be loaded. Check the ntm plugin is installed and enabled. |
| Not configured | ntm-user:settings couldn't be loaded. Run /ntm:configure and install the ntm-user plugin it produces. |
| Connector not attached | The backend connector isn't available in this session. Connect it and, for a scheduled task, check it's attached there. |
| Sign-in expired | The backend rejected the connector's sign-in. Reconnect the connector. |
| Wrong account | The connector can't see the board named in Board in your settings. Reconnect it with the account that owns that board. |
| Backend error | The backend returned <the error, shortened> on retry. Usually temporary; if it repeats, check the backend's status page. |

## With `--notify`

When the check fails, load `ntm:notify` and run `/ntm:notify --job "<job name>" --title "<Board name> — <job name> failed" --message "<job name>: <failure>. <fix>"`.

This is the one error that may use the notification channel; a job reports every later error in its final reply instead. If `ntm:notify` can't be loaded or the send fails, append `(notification not sent: <reason>)` to the result line.

With the `claude-push` channel, `ntm:notify` sends nothing and returns `NOTIFY VIA FINAL REPLY` with the title and message. That's not a failure: return the result line, then the title and the message (not the marker line). A job that ends its run with what this check returned then shows the failure once, as the completion push.
