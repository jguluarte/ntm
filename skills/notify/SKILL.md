---
name: notify
description: Sends a notification to the user's phone through the channel chosen in their settings, Pushover or the scheduled task's own push. Use whenever a task, scheduled job or workflow needs to deliver a notification, alert or reminder to the user, even if the channel isn't named. Trigger on phrases like "notify me", "send me a push", "remind me on my phone", "alert me", "ping me", or any context where the output is a mobile notification rather than a file or message in another app.
---

# ntm:notify

Sends a notification to the user's phone. Any scheduled task or workflow can use
it to reach them. This is the only skill in the system that sends anything;
every other skill returns text and the job decides what goes out.

## Usage

```
/ntm:notify --title "<title>" --message "<message>" [--url <link>] [--priority n] [--from "<job name>"] [--app-token <t> --user-key <u>]
```

- `title` and `message` are the notification.
- `url`: optional link attached below the message, usually a task's `url`
  field.
- `priority`: optional; see the optional-fields table. Default 0.
- `job`: the job this notification is for (the calling skill passes its job
  name); a per-reminder token written in Notifications is chosen by it.
- `app-token` and `user-key`: a Pushover app token and user key for this one
  call, in place of the ones in your settings (`/ntm:configure-notifications`
  uses them for its test push).

## Channel

Load `ntm-user:settings` by name and read Notifications. Its Channel line says
which section below applies: `pushover` or `claude-push`. Anything else written
there is how the user wants to be notified (quiet hours, priorities, a different
app token per reminder, …): follow it as written. A per-reminder token is a line
`Pushover app token for <job>: …` in Notifications, chosen by `--from`; without
`--from`, or with no such line, the default token. With `--app-token` and
`--user-key`, the channel is Pushover with those keys, whatever Notifications
says, and `ntm-user:settings` not loading is no failure (the test push runs
before it exists). With neither a channel nor those two, return
`Notify FAILED: no channel configured; run /ntm:configure-notifications`.

A linked task arrives in `message` as the conventions' "Talking to the user
about tasks" says (`[<words> (<id>)](<url>)`); each channel below converts it
as that section says.

## Pushover

Sends through the [Pushover API](https://pushover.net/api).

### Credentials

The Pushover app token and Pushover user key from Notifications in your
settings, or the ones `--app-token` and `--user-key` give.

### Sending

Always send in a single Bash call using this exact pattern, with the two keys in
place of `<app token>` and `<user key>`:

```bash
TITLE='Morning reminder'
MSG=$(cat <<'EOF'
Tonight's pick: <a href="https://tracker.example/ABC-12">the storage boxes (ABC-12)</a> (~5 min from the couch).
EOF
)
curl -sS --max-time 20 \
  --form-string "token=<app token>" \
  --form-string "user=<user key>" \
  --form-string "html=1" \
  --form-string "title=$TITLE" \
  --form-string "message=$MSG" \
  https://api.pushover.net/1/messages.json
```

Rules, each of which prevents a real failure:

- **Use `--form-string`, never `-F`.** With `-F`, curl treats a value starting
  with `<` as "read this file" and one starting with `@` as "upload this file".
  An HTML message that opens with `<a href=...>` would fail or send the wrong
  content.
- **Build the message with a quoted heredoc (`<<'EOF'`).** It keeps quotes, `$`
  and backticks in the text literal, with no shell escaping to get wrong.
- **Put the title in single quotes.** If the title contains a single quote, use
  a heredoc for it too.
- **Keep it to one Bash call.** Shell variables don't persist between calls.

### Optional fields

Add these as extra `--form-string` lines when they're useful:

| Field | Purpose |
|---|---|
| `url` | A link attached below the message, e.g. a task. Tappable. |
| `url_title` | Label for `url` instead of the raw link, e.g. `Open task`. |
| `priority` | `-2` silent, `-1` quiet, `0` normal (default), `1` high, `2` emergency. |
| `sound` | Notification sound; `pushover` is the default. |

- **Priority 1** bypasses quiet hours. Use it sparingly.
- **Priority 2** repeats until acknowledged and requires `retry` (seconds, 30 or
  more) and `expire` (seconds, at most 10800). Reserve it for genuine
  emergencies.

### HTML mode

`html=1` is on by default in the pattern above. Supported tags: `<a href>`,
`<b>`, `<i>`, `<u>`, `<font color>`. Newlines are kept. A linked task
`[<words> (<id>)](<url>)` in the message becomes
`<a href="<url>"><words> (<id>)</a>`, as the conventions' "Talking to the user
about tasks" says.

Escape `&`, `<` and `>` in plain text you insert, such as task titles, as
`&amp;`, `&lt;` and `&gt;`. Otherwise a title like "Tubing & fittings" breaks
the markup.

### Limits

- The message can be at most 1024 characters as sent (links converted) and the
  title at most 250. Pushover rejects anything longer, so trim before sending.
- The rate limit is 10,000 messages per month per app, well beyond what
  scheduled tasks use.

### Checking the result

Success returns `{"status":1,"request":"..."}`. Anything else is a failure:

- Print the full response body. Its `errors` array says what went wrong, e.g. an
  invalid token or a message that's too long.
- Report the failure in the run's output. Don't claim the notification was sent.
- If curl itself fails (a network error or timeout), retry once. Never retry
  after a `"status":1` response, because that would send a duplicate.

## Claude push

Nothing is sent mid-run. The scheduled task's own completion push carries the
message instead, so this skill only hands it back to the job as a delivery
block:

```
NOTIFY VIA FINAL REPLY
<title>
<message>
```

Return the title on the line after the marker and the message under it, with
linked tasks kept as the markdown they arrived in, as the conventions'
"Talking to the user about tasks" says. The job's final reply is then
everything after the marker line, verbatim, and nothing else, as the
conventions' Results say. The completion push shows that reply. `url` and
`priority` have no effect on this channel.

In chat the block is returned the same way; the reply that shows it is the
delivery.

## Result

- `Sent: <title>` when Pushover answered `"status":1`.
- The delivery block above on the `claude-push` channel.
- `Notify FAILED: <why>` otherwise, with the response's `errors` or curl's error
  as the why.
