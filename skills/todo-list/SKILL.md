---
name: todo-list
description: Lists what's planned on the user's ntm board, by default every open ticket planned for today or earlier, or whatever scope the user or a job describes ("what's on today", "what's planned this week"). Read-only. Run by jobs, or by the user.
---

# ntm:todo-list

## Usage

```
/ntm:todo-list [<scope in words>]
```

With nothing after it, list every open ticket with a planned date of today or earlier. A planned date is all it takes: labels, status and sub-tickets don't matter.

With words, list the open tickets planned within the span they describe, such as "tomorrow" or "this week". Narrow to any scope they name, such as "the garage". Take whatever they describe; never ask.

This skill only reads the board. It never changes a ticket.

## Setup

1. Load `ntm:conventions`.
2. Compute `TODAY` as the conventions' Dates section says.
3. Fetch every open ticket with the guide's `fetch open`, keeping excluded tickets, and keep the ones with a planned date in range.

If any step fails, stop and return `Todo-list FAILED: <what failed>`.

## Result

Return plain text for whoever called the skill; the job or skill that called it decides what to tell the user and how. Write one ticket per line, oldest planned date first; same date: started first, then by id. Each line is `<id> <title> <url> <planned date> <status> <estimate or -> [label, label]`, with `(started)` after the status when it's the started one. The brackets hold the ticket's labels, inherited ones included, and stay empty (`[]`) when it has none. When the ticket's status is the one Board in your settings names as started, add `(started)` after the status, before the labels.

Typed in chat, present the result as the conventions' "Talking to the user about tickets" says (natural words, the id in parentheses); the raw lines are for skills and jobs.

- With nothing after `/ntm:todo-list`: `Planned by <TODAY> (<count>):` then the tickets, or `Nothing planned for today.`
- With words: `Planned <first day> to <last day> (<count>):`, plus the scope when it's narrowed, then the tickets, or `Nothing planned <first day> to <last day>.`, plus the scope when it's narrowed.
