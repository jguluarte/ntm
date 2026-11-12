---
name: ready-check
description: >-
    Proves this session can run an ntm job: ntm-user loads, and the task list
    answers with the user's `%Settings`. Run at the start of a job, or by hand
    ("can you see my todo list?", "check the connection", "is ntm ready?").
---

# ntm:ready-check

## Usage

```
/ntm:ready-check [--notify-failure <skill>]
```

With `--notify-failure`, a failure is also sent to the user through
`ntm-user:notify`, on behalf of the skill named, such as `reminder`.

## The check

Stop at the first failure.

### 1. Load `ntm-user:backend`

If it doesn't load, the failure is Not configured.

### 2. Read `%Settings`

Read `%Settings` where `ntm-user:backend` says it lives. It's on the task list,
so this one read proves the connector, its sign-in and the account.

If the read fails, name the failure from what went wrong:

- Connector not attached: its tools aren't in this session, even after a search
- Sign-in expired: the connector rejects its sign-in, or waits on one
- Wrong account: the connector answers, but can't see `%Settings`
- Backend error: anything else, after one more try

## Result

One line: `Ready-check OK`, or `Ready-check FAILED: <failure> — <fix>`. A
backend error names the error, shortened.

| Failure                | Fix                                                               |
| ---------------------- | ----------------------------------------------------------------- |
| Not configured         | Run /ntm:setup and install the ntm-user plugin it builds          |
| Connector not attached | Attach the task list's connector to the job, or connect it again  |
| Sign-in expired        | Reconnect the task list's connector                               |
| Wrong account          | Reconnect the connector with the account that holds the task list |
| Backend error          | Usually temporary; if it repeats, check the backend's status page |

## With `--notify-failure`

On a failure, load `ntm-user:notify` and send:

| Input       | Value              |
| ----------- | ------------------ |
| `--title`   | `<name> failed`    |
| `--message` | `<failure>. <fix>` |

`<name>` is the job's title, such as Morning reminder, or the skill's name in
plain words when it runs in chat.

End with the result line, then what `ntm-user:notify` returned. When it can't be
loaded, add `(notification not sent: <reason>)` to the result line.
