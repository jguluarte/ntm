# Connectors

ntm holds no connector of yours; what it needs depends on your board and your channel, both named in `ntm-user:settings`.

| Need | Connector | Notes |
| --- | --- | --- |
| Your board, on Linear | The Linear MCP server (`https://mcp.linear.app/mcp`), declared in `.mcp.json` so installing ntm lists it on the Connectors tab | Free for individuals; the tested path. |
| Your board, on Claude Docs | None | Claude Docs is first-party and needs no connector. `ntm:conventions`' guide for it is untested. |
| Your board, on anything else | Your own connector for that backend | Board in `ntm-user:settings` says how each operation is done; `/ntm:configure-integration` writes it with you and `/ntm:self-test` proves it. |
| Notifications | None | Pushover is reached over HTTPS from the run, with the keys in `ntm-user:settings`. The claude-push channel uses the scheduled task's own completion push. |
| Amazon alert sync | Claude in Chrome on your computer | Only for `/ntm:sync-price-watch-with-amazon`; never attached to a scheduled task. |

A scheduled task inherits the connectors of the session that creates it, so the board's connector must be attached when `/ntm:configure-schedule` runs.
