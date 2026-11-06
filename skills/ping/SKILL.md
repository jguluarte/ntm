---
name: ping
description: Checks whether this session can reach the user's nudge board through the tracker connector. Run at the start of a scheduled run, or by hand ("can you see my board?", "check the tracker connection").
---

# nudge:ping

## Usage

```
/nudge:ping [--notify] [--job "<name>"]
```

- `--notify`: on failure, send the result through `nudge:notify`. Without it, nothing is sent.
- `--job "<name>"`: the job that called this ping, such as `"Morning plan"`. Defaults to `"Board ping"`.

## The ping

Stop at the first failure.

1. **Load `nudge:board`**, which loads the config and the adapter. If it can't be loaded: **Dependency missing**. If it loads but reports the plugin isn't set up: **Not set up**.
2. **Find the connector's tools.** The adapter's `ping` names the tool it uses. If that tool isn't loaded, search for it with ToolSearch. If it still isn't there: **Connector missing**.
3. **Ping the board.** Carry out the adapter's `ping`. If it comes back with the board named by the config's `board name`, the ping passes; a different board is **Wrong account**. If the call errors, go to step 4.
4. **If the call errors,** classify it:
   - An authentication or authorization error (unauthorized, forbidden, invalid or expired token): **Sign-in expired**.
   - The board isn't found: **Wrong account**.
   - Anything else (a timeout, a server error): retry once. If the retry returns a board, apply step 3 to it. If it errors, classify an authentication or not-found error as above, and anything else as **Tracker error**.

## Result

End with one result line, after the notification if there is one:

- Pass: `Board OK`
- Fail: `Board FAILED: <failure> — <fix>`

| Failure | Fix |
|---|---|
| Dependency missing | The nudge:board skill couldn't be loaded. Check the plugin is installed and enabled. |
| Not set up | The plugin's config still holds placeholders. Run /nudge:setup and install the personalized copy. |
| Connector missing | The tracker connector isn't available in this session. Reconnect it and, for a scheduled task, check it's attached there. |
| Sign-in expired | The tracker rejected the connector's sign-in. Reconnect the tracker connector. |
| Wrong account | The connector can't see the board named in the config. Reconnect it with the account that owns that board. |
| Tracker error | The tracker returned <the error, shortened> on retry. Usually temporary; if it repeats, check the tracker's status page. |

## With `--notify`

When the ping fails, load `nudge:notify` and send:

- **Title:** `<board name> — <job name> failed`
- **Message:** `<job name>: <failure>. <fix>`

If `nudge:notify` can't be loaded or the send fails, append `(notification not sent: <reason>)` to the result line.

With the `claude-push` channel, `nudge:notify` sends nothing mid-run and returns `NOTIFY VIA FINAL REPLY`. That's not a failure: ignore the block it returns; the result line is what the job ends with, and the caller's error handling carries it in the run's final reply.
