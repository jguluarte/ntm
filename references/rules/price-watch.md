# Price watch conventions

The price watch checks the things the user wants to buy, and tells them when one
is a good deal. Each item is represented as a task on their task list.

## `$price-watch`

Marks what the user wants to buy. On a task, it watches that task; on a project,
every task in the project. The watched tasks are the open ones it covers. Each
is the purchase itself, and closes once the user buys it (or they change their
mind).

## The watched item

Everything about an item lives on its task. The task names the exact item, with
its model and variant, and its target price. A different variant is a different
item.

Where the user wants something other than these defaults, the task says so in
their words:

| Detail    | Default                                                      |
| --------- | ------------------------------------------------------------ |
| Condition | New                                                          |
| Delivery  | Bought online and delivered                                  |
| A deal    | A price at or near the target, or well below the usual price |

The stores for an item are on its task too: the ones the user trusts or blocks
for it.

## Amazon price alerts

Only when the Amazon interface setting, in `%Settings`, isn't `off`.

The price watch can't read Amazon, so Amazon's own price alerts cover Amazon.
`/ntm:sync-price-watch-to-amazon` sets and removes them in a browser, and keeps
these labels:

| Label                 | The task's item                                     |
| --------------------- | --------------------------------------------------- |
| `$has-amazon-alert`   | has an Amazon price alert                           |
| `$amazon-unavailable` | isn't sold on Amazon in a condition the user allows |

`$has-amazon-alert` stays on a task that closes until the sync removes its
alert: the label is the only record that the alert is live.
