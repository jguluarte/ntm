---
name: ready-check
description: >-
    Proves this session can run an ntm job and loads the user's settings and
    ntm's core rules for it: ntm-user loads, and the task list answers with the
    user's `%Settings`. On a failure, says what is wrong and how to fix it. Run
    at the start of a job, or by hand ("can you see my todo list?", "check the
    connection", "is ntm ready?").
---

# ntm:ready-check

## Usage

```
/ntm:ready-check
```

## The check

Stop at the first failure.

### 1. Load `ntm-user:backend`

If it doesn't load, the failure is Not configured.

### 2. Load `%Settings`

Read `%Settings` where `ntm-user:backend` says it lives. It's on the task list,
so this one read proves the connector, its sign-in and the account. Its values
are the user's settings for the rest of the run.

If the read fails, name the failure from what went wrong:

- Connector not attached: its tools aren't in this session, even after a search
- Sign-in expired: the connector rejects its sign-in, or waits on one
- Wrong account: the connector answers, but can't see `%Settings`
- Backend error: anything else, after one more try

### 3. Read the core rules

Read ntm's core rules, `${CLAUDE_PLUGIN_ROOT}/references/rules/core.md`, and
follow them for the rest of the run.

## Result

One line: `Ready-check OK`, or `Ready-check FAILED: <failure> — <fix>`. A
backend error names the error, shortened. In a job, the failure line ends the
run, and the job's own push delivers it.

| Failure                | Fix                                                               |
| ---------------------- | ----------------------------------------------------------------- |
| Not configured         | Run /ntm:setup and install the ntm-user plugin it builds          |
| Connector not attached | Attach the task list's connector to the job, or connect it again  |
| Sign-in expired        | Reconnect the task list's connector                               |
| Wrong account          | Reconnect the connector with the account that holds the task list |
| Backend error          | Usually temporary; if it repeats, check the backend's status page |
