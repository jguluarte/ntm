# ntm-user:notify

Sends a notification to the user's phone through the scheduled task's own push.
Any job or workflow can use it to reach them. This is the only skill in the
system that sends anything; every other skill returns text and the job decides
what goes out.

## Usage

```
/ntm-user:notify --title "<title>" --message "<message>" [--url <link>]
    [--priority n] [--from <skill>] [--app-token <t>] [--user-key <u>]
```

- `title` and `message` are the notification.
- `from`: the skill this notification is for, by name, such as
  `morning-reminder`; anything Notifications says about one reminder is matched
  by it.
- `url`, `priority`, `app-token` and `user-key` have no effect on this channel.

## Notifications

Load `ntm-user:settings` by name and read Notifications: how the user wants to
be notified (quiet hours, priorities, …). Follow it as written.

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
linked tasks kept as the markdown they arrived in, as the conventions' "Talking
to the user about tasks" says. The job's final reply is then everything after
the marker line, verbatim, and nothing else, as the conventions' Results say.
The completion push shows that reply.

In chat the block is returned the same way; the reply that shows it is the
delivery.

## Result

The delivery block above, which has no length cap.
