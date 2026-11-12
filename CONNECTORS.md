# Connectors

Ntm works on a task list you own and reaches you on your phone, so it needs a
few things connected. `/ntm:setup` walks you through each one.

## Your task list

Linear is the task list ntm is built around. It's free for individuals, and
setup helps you make an account and add Linear on the Connectors tab in Claude's
settings. Your own plugin, which setup builds, brings Linear along so your
scheduled jobs reach your list too. It asks you to sign in to Linear once more
the first time.

Your tasks can live somewhere else instead, through that service's own
connector. That's a custom setup you work out with Claude during setup.
`/ntm:self-test` checks that it works.

## Notifications

Reminders reach your phone one of two ways, and you pick one in setup.

### Pushover

Reminders arrive in their own app, which your phone's focus settings can handle
differently from other apps. It needs an inexpensive license you buy, the
Pushover app on your phone, and two keys from pushover.net: your user key and an
app token. Setup saves the keys in your `%Settings`, a page ntm keeps with your
tasks, and sends one test push.

### The AI app's own push

Nothing to buy or set up: you need the AI app on your phone, with its
notifications allowed. Each reminder arrives as a push when its job finishes.

## Amazon price alerts

The price watch can't check Amazon itself, so Amazon's own price alerts cover
it. If you turned them on, run `/ntm:sync-price-watch-to-amazon` in chat now and
then. It sets the alerts from a browser signed in to Amazon, either Claude's
built-in browser or your own through the Claude extension. Amazon needs no
connector.
