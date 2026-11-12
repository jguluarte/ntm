# Settings

<!--
The values the user chose in setup. Setup writes this database from this
template, with the user's answers, for the features they picked. The user can
edit, delete or add any part; anything they add goes in its own subsection, in
their words. These comments are for the agent, and are never written into the
user's database.
-->

## About you

<!--
Timezone is an IANA name. It decides what today is for the user, and their jobs
run in it.
-->

- Timezone: America/Los_Angeles

## Labels

<!--
Each label ntm uses, by ntm's name, with its name on the user's task list.
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
Planning never picks a task with one of the labels to exclude from
auto-scheduling. A `$` name there means the user's own name for that label, from
Labels.
-->

### Labels to exclude from auto-scheduling

- `$no-autoschedule`
- `$pending-shipment`

## Shopping

<!--
Country is where the stores must deliver, and Currency is the one every price is
in. Amazon interface is the browser ntm uses to keep the user's Amazon price
alerts: Claude's built-in browser, or their own browser through the Claude
extension. `off` when they want no Amazon price alerts.
-->

### Country

US

### Currency

USD

### Amazon interface

Claude's built-in browser

## Notifications

<!--
How the user wants to be notified, in their words, such as quiet hours. Their
channel lives in `ntm-user:notify`, which reads its Pushover keys here when it
sends. Write Pushover keys only for a Pushover user, with their keys in full.
-->

### Pushover keys

| Key       | Value         |
| --------- | ------------- |
| App token | `<app token>` |
| User key  | `<user key>`  |
