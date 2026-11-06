---
name: notify
description: Sends a notification to the user's phone through the channel chosen in the config, Pushover or the scheduled task's own push. Use whenever a task, scheduled job or workflow needs to deliver a notification, alert, nudge or reminder to the user, even if the channel isn't named. Trigger on phrases like "notify me", "send me a push", "remind me on my phone", "alert me", "ping me", or any context where the output is a mobile notification rather than a file or message in another app.
---

# nudge:notify

Sends a notification to the user's phone. Any scheduled task or workflow can use it to reach them directly, without depending on another app's notification quirks. This is the only skill in the system that sends anything; every other skill returns text and the job decides what goes out.

## Usage

```
/nudge:notify --title "<title>" --message "<message>" [--url <link>] [--priority n]
```

- `title` and `message` are the notification.
- `url`: optional link attached below the message, usually a ticket's `url` field.
- `priority`: optional; see the optional-fields table. Default 0.

## Channel

The config's `channel` says which section below applies: `pushover` or `claude-push`. Links in messages use the ticket's `url`.

## Pushover

Sends through the [Pushover API](https://pushover.net/api).

### Credentials

The config's `pushover app token` and `pushover user key`. In a personalized copy they are filled in below; the template holds placeholders.

### Sending

Always send in a single Bash call using this exact pattern:

```bash
TITLE='Nudge'
MSG=$(cat <<'EOF'
Tonight's pick: <a href="https://tracker.example/ABC-12">ABC-12</a>, order storage boxes (~5 min from the couch).
EOF
)
curl -sS --max-time 20 \
  --form-string "token=~~pushover app token" \
  --form-string "user=~~pushover user key" \
  --form-string "html=1" \
  --form-string "title=$TITLE" \
  --form-string "message=$MSG" \
  https://api.pushover.net/1/messages.json
```

Rules, each of which prevents a real failure:

- **Use `--form-string`, never `-F`.** With `-F`, curl treats a value starting with `<` as "read this file" and one starting with `@` as "upload this file". An HTML message that opens with `<a href=...>` would fail or send the wrong content.
- **Build the message with a quoted heredoc (`<<'EOF'`).** It keeps quotes, `$` and backticks in the text literal, with no shell escaping to get wrong.
- **Put the title in single quotes.** If the title contains a single quote, use a heredoc for it too.
- **Keep it to one Bash call.** Shell variables don't persist between calls.

### Optional fields

Add these as extra `--form-string` lines when they're useful:

| Field | Purpose |
|---|---|
| `url` | A link attached below the message, e.g. a ticket. Tappable. |
| `url_title` | Label for `url` instead of the raw link, e.g. `Open ticket`. |
| `priority` | `-2` silent, `-1` quiet, `0` normal (default), `1` high, `2` emergency. |
| `sound` | Notification sound; `pushover` is the default. |

- **Priority 1** bypasses quiet hours. Use it sparingly.
- **Priority 2** repeats until acknowledged and requires `retry` (seconds, 30 or more) and `expire` (seconds, at most 10800). Reserve it for genuine emergencies.

### HTML mode

`html=1` is on by default in the pattern above. Supported tags: `<a href>`, `<b>`, `<i>`, `<u>`, `<font color>`. Newlines are kept.

Escape `&`, `<` and `>` in plain text you insert, such as ticket titles, as `&amp;`, `&lt;` and `&gt;`. Otherwise a title like "Tubing & fittings" breaks the markup.

### Limits

- The message can be at most 1024 characters and the title at most 250. Pushover rejects anything longer, so trim before sending.
- The rate limit is 10,000 messages per month per app, well beyond what scheduled tasks use.

### Checking the result

Success returns `{"status":1,"request":"..."}`. Anything else is a failure:

- Print the full response body. Its `errors` array says what went wrong, e.g. an invalid token or a message that's too long.
- Report the failure in the run's output. Don't claim the notification was sent.
- If curl itself fails (a network error or timeout), retry once. Never retry after a `"status":1` response, because that would send a duplicate.

## Claude push

Nothing is sent mid-run. The scheduled task's own completion push carries the message instead, so this skill only hands it back to the job as a delivery block:

```
NOTIFY VIA FINAL REPLY
<title>
<message>
```

Return the title on the line after the marker and the message under it, with HTML tags removed and each link as its bare url. The job's final reply is then everything after the marker line, verbatim, followed by anything else its FINAL REPLY calls for, as the board rules' Results paragraph says; the completion push shows that reply. `url` and `priority` have no effect on this channel.

In chat, this channel can't send anything; say so in one line and show the title and message instead.
