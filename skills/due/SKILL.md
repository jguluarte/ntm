---
name: due
description: Lists what's due on the user's nudge board, by default every open ticket planned for today or earlier, or whatever the user or a job describes ("what's due today", "what's planned this week"). Read-only. Run by jobs, or by the user.
---

# nudge:due

## Usage

```
/nudge:due [what to look at]
```

With nothing after it, list every open ticket with a planned date of today or earlier. A planned date is all it takes: labels, status and sub-tickets don't matter.

With a description, list the open tickets planned within the span it describes, such as "tomorrow" or "this week", narrowed to any scope it names, such as "the garage". Take whatever it describes; never ask.

This skill only reads the board. It never changes a ticket.

## Setup

1. Load `nudge:board`.
2. Compute `TODAY` as the board rules' Dates section says.
3. Fetch every open ticket with the board rules' Scheduling fetch (the adapter's `fetch open`), keeping excluded tickets, and keep the ones with a planned date in range.

If any step fails, stop and return `Due FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write one ticket per line, oldest planned date first, as `<id> <title> <url> <planned date> <status> [label, label]`, where the brackets hold the ticket's labels, inherited ones included, and stay empty (`[]`) when it has none.

- With nothing after `/nudge:due`: `Due by <TODAY> (<count>):` then the tickets, or `Nothing due today.`
- With a description: `Due <first day> to <last day> (<count>):`, plus the scope when it's narrowed, then the tickets, or `Nothing due.`
