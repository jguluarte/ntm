---
name: ready-check
description: >-
    Proves this session can run ntm: the user plugin loads and the task list
    answers. Run first in every job, and by self-test, or by hand ("can you see
    my todo list?", "check the connection", "is ntm ready?").
---

# ntm:ready-check

A broken connection ends the run with one plain line saying what to fix.

## Usage

```
/ntm:ready-check [--notify-failure <name>]
```

`--notify-failure <name>`: when the check fails, also send the failure to the
user's phone, for the job named, such as `price-watch`. Without it, nothing is
sent.

## The check

### 1. Load the user plugin

Load `ntm-user:backend`. If it won't load, the check fails: Not configured.

### 2. Ping the task list

Ping it as `ntm-user:backend` describes, and sort a failure the way it says:
Sign-in expired, Wrong account or Backend error. When the ping's tool can't be
found in this session, it's Connector not attached.

### 3. Send the failure

The check stops at its first failure. With `--notify-failure`, load
`ntm-user:notify` and send the failure from `<name>`, titled
`<List name> — <Job> failed`, with the message `<Job>: <failure>. <fix>`.
`<Job>` is `<name>` in plain words (`price-watch` is Price watch), and
`<List name>` is the task list's name in `ntm-user:backend`.

When `ntm-user:notify` returns a delivery block, deliver it the way
`ntm-user:notify` says, under the result line.

## Failures

When `ntm-user:backend` gives its own fix for a failure, use that.

| Failure                | What happened                                   | Fix                                                          |
| ---------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| Not configured         | `ntm-user:backend` won't load                   | Run `/ntm:setup` and install the `ntm-user` plugin it builds |
| Connector not attached | the task list's connector isn't in this session | Attach the connector to the job, or connect it again         |
| Sign-in expired        | the backend turned down the connector's sign-in | Reconnect the connector                                      |
| Wrong account          | the connector can't see the task list           | Reconnect it with the account that owns the task list        |
| Backend error          | the ping failed for another reason              | `<the error>`; if it repeats, see the backend's status page  |

## Result

The result line is one of these:

| Result                                                                 | When                                                   |
| ---------------------------------------------------------------------- | ------------------------------------------------------ |
| `Ready-check OK`                                                       | the task list answered                                 |
| `Ready-check FAILED: <failure> — <fix>`                                | a step failed                                          |
| `Ready-check FAILED: <failure> — <fix> (notification not sent: <why>)` | a step failed, and `--notify-failure` couldn't send it |
