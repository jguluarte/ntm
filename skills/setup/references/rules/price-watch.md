# Price watch rules

## System labels

- **$has-amazon-alert:** an Amazon price alert is set for this task.
  `ntm:sync-price-watch-to-amazon` sets and clears it.
- **$amazon-unavailable:** the item isn't sold on Amazon in a condition the user
  allows, so no alert is set.
- **$price-watch:** usually on a project: its tasks are purchases waiting for a
  good price. The watched tasks are the open tasks carrying this label. Price
  watch is off when nothing carries it or the Price watch job isn't scheduled;
  there is no separate switch. A watched task's description names the exact item
  (model and variant) and its target price, and says, in the user's words,
  anything that differs from the defaults: the condition (new), how it reaches
  them (ordered online and delivered), and what counts as a deal (at or near the
  target, or well below the usual price). The shopper reads them there.

## Databases

- **price watch stores** (`Price watch stores`): stored in the project that
  carries the $price-watch label, not at list level. `ntm:price-watch` keeps it,
  from the user's vouch and block replies; the shopper reads it.
