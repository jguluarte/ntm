---
name: configure
description: The ntm wizard. Walks the user through everything ntm needs in one chat (about you, todo list, notifications, style, schedule), hands each part to its configure skill, and ends with ntm-user.plugin to install. Run when the user says "set up ntm", "configure ntm", "get started", or installs ntm for the first time; "/ntm:configure schedule" (or any other part) goes straight to that part.
---

# ntm:configure

Everything happens in chat, in short rounds: you bring proposals, they react. Never hand them a form. This skill writes nothing itself: each part returns its section text, and `ntm:settings` packages everything once at the end.

## Usage

```
/ntm:configure
/ntm:configure <part>
```

Parts: `about-you`, `todo list`, `notifications`, `style`, `schedule`.

## Before you start

Load `ntm-user:settings` by name.

- **Won't load:** nothing is configured. Follow First run.
- **Loads:** follow Configured.

## First run

Say two lines first:

1. ntm keeps your settings and style in a small plugin of your own, `ntm-user`; this builds it with you and hands it back to install at the end.
2. The steps: about you, your todo list (and how planning and shopping work on it), how reminders reach you, how they talk to you, and the schedule. Each is a short conversation, and your own plugin is written once, at the end.

### About you

This skill owns About you. Ask:

- Name: how a message title addresses you.
- Timezone: an IANA name; confirm the city when they give one instead. Every date in the system is computed in it.
- Country and currency, for price watch (`US, USD`).

Write them as the About you section, in the shape `ntm-user:settings` uses.

### The parts

In order, each by loading its skill and saying it runs from `ntm:configure`:

1. `ntm:configure-todo-list`: which backend, which todo list, statuses, labels, notes, and the agreements the planner and the shopper work by. Returns Todo list, Labels, Planning and Shopping (Shopping only when a price watch project was chosen).
2. `ntm:configure-notifications`: the channel, the keys and a test push. Returns Notifications.
3. `ntm:configure-style`: plain, a theme, or a persona skill they have. Returns the `ntm-user:style` body.
4. `ntm:configure-schedule`: which jobs, which days, what time, what title. Hand it the timezone from About you, the price watch project from Todo list and Planning days from Planning, as settled above. Creates the scheduled tasks itself; returns nothing to package.

Keep the returned text; write nothing.

The sections and what reads them, in case they ask: About you is read by everything; Todo list and Labels by `ntm:conventions`; Planning (rhythm, days, how far ahead the week plans, sizing, what's never picked, what the weekly message includes) by `ntm:plan`, the planner and the weekly planning; Shopping (condition, delivery, what counts as a deal) by the shopper and `ntm:price-watch`; Notifications by `ntm:notify`. `ntm:configure-todo-list` settles Planning and Shopping alongside Todo list, since each default is about the same todo list.

### Packaging

Load `ntm:settings` and follow its "Regenerating `ntm-user.plugin`" section with every section the parts returned: About you, Todo list, Labels, Planning, Shopping, Notifications, the style body. `ntm:settings` tells them to install it and open a new chat. Add that the first thing to run there is `/ntm:self-test`: it starts with `ready-check` and exercises the operations the jobs use, on a throwaway ticket. Until it's installed, every scheduled run ends with "not configured".

## Configured

One line of state per part, from what loads: About you (name, timezone); todo list (backend, todo list name, price watch project or off); notifications (channel); style (`ntm-user:style` loads, or not); schedule (which tasks exist, from `ntm:configure-schedule`'s listing). Ask which to change and hand off to that part; it shows its current state and asks what to change. About you is handled here the same way. Then package as Packaging says, with what it returned. A schedule change alone changes nothing in `ntm-user`, so there's nothing to package after it.

## `configure <part>`

Straight to that part, no state lines: `about-you` to About you above; the other four to their skill. Then Packaging for `about-you`, `todo list`, `notifications` and `style`. `schedule` packages nothing: a schedule change changes nothing in `ntm-user`.
