# Settings

<!--
The values the user agreed to in setup, read by the ntm skills that need them.
Its contents are suggested defaults the user can customize, with an example
wherever the value is the user's own. Setup creates this database from this
template, filled with the user's answers, and writes it without these comments:
they are for you, never for the user. Skills find each section and line by its
name; the user can edit, delete or add them.
-->

## About you

<!--
Timezone is an IANA name: jobs run in it, and it gives today's date when
nothing else does. Country is where the price watch shops, and Currency the
currency it prices in.
-->

- Timezone: America/Los_Angeles
- Country: US
- Currency: USD

## Labels

<!--
The name on the user's task list for each label ntm uses, by ntm's name for it.
Only the labels of the features the user picked: `$no-autoschedule` and
`$pending-shipment` for task management, `$price-watch` for price watch, and
the two Amazon labels only when Amazon interface isn't `off`. Skills read each
label's name here.
-->

| Label                 | Name on your task list |
| --------------------- | ---------------------- |
| `$no-autoschedule`    | `no-autoschedule`      |
| `$pending-shipment`   | `pending-shipment`     |
| `$price-watch`        | `price-watch`          |
| `$has-amazon-alert`   | `has-amazon-alert`     |
| `$amazon-unavailable` | `amazon-unavailable`   |

## Planning

<!--
How the user wants their task list planned, read by `ntm:plan`. Task
management only. Labels to exclude from auto-scheduling are the ones planning
never picks. By default they are `$no-autoschedule` and `$pending-shipment`,
which mean the user's own names for those labels, in Labels. Anything else the
user says about planning goes in its own subsection, in their words.
-->

### Labels to exclude from auto-scheduling

- `$no-autoschedule`
- `$pending-shipment`

## Shopping

<!--
How the price watch shops, for every watched item unless the task says
otherwise. Price watch only. Amazon interface is how
`ntm:sync-price-watch-to-amazon` reaches Amazon to keep its price alerts:
Claude's built-in browser, or the user's own browser through the Claude
extension. `off` means no Amazon alerts. Its subsection is always written: it
has no default to fall back on when missing. Anything else the user says about
how they shop goes in its own subsection, in their words. Stores they trust or
block go in the `%Price-watch-stores` database instead.
-->

### Amazon interface

Claude's built-in browser

## Notifications

<!--
How the user wants to be notified, in their words, such as quiet hours or a
priority for one reminder. `ntm-user:notify` follows it as written. The channel
and any keys live in `ntm-user:notify`, never here.
-->
