# Connectors

Neurodivergent Task Manager (ntm) holds no connector of yours; what it needs
depends on your todo list and your channel, both named in `ntm-user:settings`.

A scheduled task inherits the connectors of the session that creates it, so the
list's connector must be attached when `/ntm:configure-schedule` runs.

## Your todo list, on Linear

Linear's connector, added on the Connectors tab in Claude's settings;
`/ntm:configure-todo-list` walks you through it. Free for individuals.

## Your todo list, on anything else

Your own connector for that backend. Todo list in `ntm-user:settings` says how
each operation is done; `/ntm:configure-todo-list` writes it with you and
`/ntm:self-test` proves it.

## Notifications

None. Pushover is reached over HTTPS from the run, with the keys in
`ntm-user:settings`. The claude-push channel uses the scheduled task's own
completion push.

## Amazon alert sync

Claude's built-in browser, or your own through the Claude extension. Only for
`/ntm:sync-price-watch-to-amazon`.
