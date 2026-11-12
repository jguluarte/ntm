# Connectors

Ntm works on a task list you own and reaches you on your phone, so it needs a
few things connected. `/ntm:setup` walks you through each one.

## Your task list

Linear is the task list ntm is built around. It's free for individuals, and
setup helps you make an account and add Linear on the Connectors tab in Claude's
settings. The plugin setup builds for you carries the same connection, so your
scheduled jobs reach your list too.

Your tasks can live somewhere else instead, through that service's own
connector. That's a custom setup you work out with your agent during setup, and
`/ntm:self-test` shows whether it holds.

## Notifications

Reminders reach your phone one of two ways, and you pick one in setup.

### Pushover

Reminders arrive in their own app, which your phone's focus settings can treat
apart from everything else. It needs an inexpensive license you buy, the
Pushover app on your phone, and two keys from pushover.net: your user key and an
app token. Setup saves the keys in your `%Settings` and sends one test push.

### The AI app's own push

Nothing to buy or set up: you need the AI app on your phone, with its
notifications allowed. Each reminder arrives as a push when its job finishes.

## Amazon price alerts

Only if you turn them on for the price watch. `/ntm:sync-price-watch-to-amazon`
sets the alerts from a browser signed in to Amazon: Claude's built-in browser,
or your own through the Claude extension. Amazon needs no connector.
