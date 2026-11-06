# Connectors

## How tool references work

Plugin files use a placeholder (two tildes, then the category's key) for whatever the user connects or chooses in that category. The plugin describes its workflow in terms of categories rather than specific products; `nudge:setup` replaces the placeholders with the user's own values and the result is a personalized copy of the plugin.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
| --- | --- | --- | --- |
| Ticket tracker | `~~tracker` | Linear (free for individuals; the tested path), declared in `.mcp.json` so installing the plugin offers it | another tracker with an adapter drafted during setup |
| Claude Docs, for the `claude-docs` adapter only | — | Claude Docs (first-party; no sign-in) | — |
| Notifications | `~~channel` | — | Pushover (needs an app token and user key), or the scheduled task's own Claude push notification (needs nothing) |
| Browser, for Amazon price-alert sync only | — | — | Claude in Chrome on the user's computer |

The tracker connector (or Claude Docs, with the `claude-docs` adapter) must be attached to the session that creates the scheduled tasks, since jobs inherit the connectors of the session they were created from.

`nudge:setup` leaves this file out of its placeholder replace, so the table above stays a table of placeholders in a personalized copy.
