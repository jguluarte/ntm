# ntm-user:notify

Sends one notification to the user through Pushover, and says whether it went.

## Usage

```
/ntm-user:notify --title "<title>" --message "<message>"
    [--app-token <token>]
```

| Input         | What it is                                                  |
| ------------- | ----------------------------------------------------------- |
| `--title`     | The notification's title                                    |
| `--message`   | The message, with task links in markdown                    |
| `--app-token` | A job's own Pushover app token, in place of the one in Keys |

## Keys

| Key       | Value         |
| --------- | ------------- |
| App token | `<app token>` |
| User key  | `<user key>`  |

## Send

Pushover takes a title of up to 250 characters and a message of up to 1,024 as
sent, links included. When either is longer, send nothing and return
`Notify TOO LONG`.

Otherwise, post it to Pushover's messages API with these fields:

| Field     | Value                                         |
| --------- | --------------------------------------------- |
| `token`   | The app token                                 |
| `user`    | The user key                                  |
| `title`   | `--title`                                     |
| `message` | `--message`, each markdown link as `<a href>` |
| `html`    | `1`                                           |

Add `priority` or `sound` when Notifications calls for one.

## Result

| Return                                                   | When                                             |
| -------------------------------------------------------- | ------------------------------------------------ |
| `Sent: <title>`                                          | Pushover accepted it                             |
| `Notify TOO LONG: <title or message>, <length> of <cap>` | One is over its cap; nothing was sent            |
| `Notify FAILED: <why>`                                   | Anything else, with Pushover's errors as the why |
