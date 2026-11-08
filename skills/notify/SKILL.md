---
name: notify
description: >-
    Sends a notification to the user's phone through the channel chosen in their
    settings, Pushover or the scheduled task's own push. Use whenever a skill,
    job or workflow needs to deliver a notification, alert or reminder to the
    user, even if the channel isn't named. Trigger on phrases like "notify me",
    "send me a push", "remind me on my phone", "alert me", "ping me", or any
    context where the output is a mobile notification rather than a file or
    message in another app.
---

# ntm:notify

Sends a notification to the user's phone.

## Usage

```
/ntm:notify --title "<title>" --message "<message>" [--url <link>]
    [--priority n] [--from "<job name>"] [--app-token <t> --user-key <u>]
```

- `url`: a link shown below the message, usually a task's `url` field.
- `priority`: see Optional fields. Default 0.
- `from`: the calling job's name, which picks that job's Pushover app token.
- `app-token` and `user-key`: Pushover keys for this one call, in place of the
  ones in settings. `/ntm:configure-notifications` uses them for its test push.

## Channel

Load `ntm-user:settings` by name and read Notifications. Its Channel line picks
the section below: `pushover` or `claude-push`. Follow anything else written
there as written (quiet hours, priorities, a token per reminder).

A line `Pushover app token for <job>: …` is the token when `--from` names that
job. Otherwise use the default token.

With `--app-token` and `--user-key`, use Pushover with those keys whatever
Notifications says. Settings that don't load are no failure then: the test push
runs before they exist.

With no channel and no keys, return:

```
Notify FAILED: no channel configured; run /ntm:configure-notifications
```

A linked task arrives in `message` in the form the conventions' "Talking to the
user about tasks" gives: `[<words> (<id>)](<url>)`. Pushover turns it into
`<a href="<url>"><words> (<id>)</a>`; Claude push keeps the markdown.

## Pushover

Send through the [Pushover API](https://pushover.net/api), with the app token
and user key from Notifications, or from `--app-token` and `--user-key`.

### Sending

Send in one Bash call, in exactly this pattern:

```bash
TITLE='Morning reminder'
MSG=$(cat <<'EOF'
Today's pick is a quick one, ~5 min from the couch.

<a href="https://tracker.example/ABC-12">the storage boxes (ABC-12)</a>
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

- Use `--form-string`, never `-F`. With `-F`, curl reads a value starting with
  `<` or `@` as a file, so a message opening with `<a href=...>` breaks.
- Build the message with a quoted heredoc (`<<'EOF'`), so quotes, `$` and
  backticks stay literal.
- Put the title in single quotes, or in a heredoc if it contains one.
- Keep it to one call: shell variables don't carry between calls.

### HTML

`html=1` allows `<a href>`, `<b>`, `<i>`, `<u>` and `<font color>`, and keeps
newlines. In plain text you insert, such as task titles, escape `&`, `<` and `>`
as `&amp;`, `&lt;` and `&gt;`, or a title like "Tubing & fittings" breaks the
markup.

### Optional fields

Add these as extra `--form-string` lines when useful:

| Field       | Purpose                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| `url`       | A tappable link below the message, e.g. a task.                         |
| `url_title` | Label for `url` instead of the raw link, e.g. `Open task`.              |
| `priority`  | `-2` silent, `-1` quiet, `0` normal (default), `1` high, `2` emergency. |
| `sound`     | Notification sound; `pushover` is the default.                          |

- Priority 1 bypasses quiet hours. Use it sparingly.
- Priority 2 repeats until acknowledged and needs `retry` (30 seconds or more)
  and `expire` (at most 10800 seconds). Emergencies only.

### Limits

Pushover takes at most 1,024 characters for the message as sent (links
converted) and 250 for the title. If either is over, don't trim it and don't
send. Return `Notify TOO LONG: <the cap and why>; this was <n>`, with the cap in
plain words: "Pushover takes at most 1,024 characters as sent, links included"
for the message, "at most 250 characters" for the title.

### Checking the result

Success is `{"status":1,"request":"..."}`. Anything else is a failure: print the
full response body (its `errors` say what went wrong), report the failure, and
don't claim it was sent. If curl itself fails (a network error or timeout),
retry once. Never retry after `"status":1`: that sends a duplicate.

## Claude push

Send nothing. The scheduled task's own completion push carries the message, so
return it to the job as a delivery block, linked tasks left as markdown:

```
NOTIFY VIA FINAL REPLY
<title>
<message>
```

The job's final reply is then the title and message, verbatim, as the
conventions' Results say. `url` and `priority` do nothing here. In chat, return
the block the same way; the reply that shows it is the delivery.

## Result

- `Sent: <title>` when Pushover answered `"status":1`.
- The delivery block, on Claude push. It has no length cap.
- `Notify TOO LONG: <the cap and why>; this was <n>` when over a Pushover cap.
  Nothing was sent; the caller shortens it and calls once more.
- `Notify FAILED: <why>` otherwise, with the response's `errors` or curl's error
  as the why.
