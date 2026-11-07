# Connectors

neurodivergent-task-manager holds no connector of yours; what it needs depends
on your todo list and your channel, both named in `ntm:settings`.

| Need | Connector | Notes |
| --- | --- | --- |
| Your todo list, on Linear | The Linear MCP server (`https://mcp.linear.app/mcp`), declared in `.mcp.json` so installing neurodivergent-task-manager lists it on the Connectors tab | Free for individuals. |
| Your todo list, on Claude Docs | None | Claude Docs is first-party and needs no connector. `neurodivergent-task-manager:conventions`' guide for it is untested. |
| Your todo list, on anything else | Your own connector for that backend | Todo list in `ntm:settings` says how each operation is done; `/neurodivergent-task-manager:configure-todo-list` writes it with you and `/neurodivergent-task-manager:self-test` proves it. |
| Notifications | None | Pushover is reached over HTTPS from the run, with the keys in `ntm:settings`. The claude-push channel uses the scheduled task's own completion push. |
| Amazon alert sync | Claude's built-in browser, or your own through the Claude extension | Only for `/neurodivergent-task-manager:sync-price-watch-to-amazon`. |

A scheduled task inherits the connectors of the session that creates it, so the
list's connector must be attached when
`/neurodivergent-task-manager:configure-schedule` runs.
