# ntm-user:notify

Delivers one notification to the user through the AI app's own push. Nothing is
sent mid-run: the job ends its run with the message, and the app pushes that
final reply to their phone.

## Usage

```
/ntm-user:notify --from <skill> --title "<title>" --message "<message>"
```

| Input       | What it is                                               |
| ----------- | -------------------------------------------------------- |
| `--from`    | The skill the message is for, such as `morning-reminder` |
| `--title`   | The notification's title                                 |
| `--message` | The message, with task links in markdown                 |

## Notifications

Load `ntm-user:backend` to read the user's conventions, then read Notifications
in their `%Settings` database: how they want to be notified, in their words.
Follow it for this message, and match anything it says about one skill by
`--from`.

## Deliver

Return the title and message for the job to end its run with:

```
NOTIFY VIA FINAL REPLY
<title>
<message>
```

Run by hand in chat, nothing is pushed: the reply that shows the title and
message is the delivery.

## Result

The block above. It has no length cap.
