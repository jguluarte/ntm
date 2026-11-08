---
name: configure
description: >-
    The ntm wizard. Walks the user through everything ntm needs in one chat
    (about you, todo list, notifications, style, schedule), hands each part to
    its configure skill, and ends with ntm-user.plugin to install. Run when the
    user says "set up ntm", "configure ntm", "get started", or installs ntm for
    the first time; "/ntm:configure schedule" (or any other part) goes straight
    to that part.
---

# ntm:configure

Work in chat, in short rounds: bring proposals, let the user react, never hand
them a form. This skill writes nothing: each part returns its section text, and
`ntm:settings` packages it all once, at the end.

## Usage

```
/ntm:configure
/ntm:configure <part>
```

Parts: `about-you`, `todo-list`, `notifications`, `style`, `schedule`.

With a part, go straight to it, with no state lines: `about-you` to About you
below, the others to their skill. Then Packaging.

Without one, load `ntm-user:settings` by name. If it won't load, nothing is
configured: follow First run. If it loads, follow Configured.

## First run

Open with two lines:

1. Neurodivergent Task Manager (ntm) keeps your settings and style in a small
   plugin of your own, `ntm-user`; this builds it with you and hands it back to
   install at the end.
2. The steps: about you, your todo list (and how planning and shopping work on
   it), how reminders reach you, how they talk to you, and the schedule. Each is
   a short conversation.

Then About you, the parts in order, and Packaging.

## About you

This skill owns About you. Fill both lines from what you already know of the
user and the session, and ask only to confirm or correct:

- Timezone: an IANA name. Every date ntm computes uses it. If you can't tell,
  ask for their city.
- Country and currency, for price watch.

The section is one line each:

```markdown
- Timezone: America/Chicago
- Country and currency: US, USD
```

## The parts

Load each part's skill in order, saying it runs from `ntm:configure`, and keep
the text it returns:

1. `ntm:configure-todo-list`: backend, todo list, statuses, labels, notes, and
   how planning and shopping work. Returns Todo list, Labels, Planning, and
   Shopping when a price watch project was chosen.
2. `ntm:configure-notifications`: the channel, the keys and a test push. Returns
   Notifications.
3. `ntm:configure-style`: plain, a theme, or a persona skill they have. Returns
   the `ntm-user:style` body.
4. `ntm:configure-schedule`: which jobs, on which days, at what time, under what
   title. Hand it the timezone, whether a price watch project was chosen, and
   the Planning days. It creates the scheduled tasks itself and returns nothing.

## Packaging

Load `ntm:settings` and follow its "Regenerating `ntm-user.plugin`" section with
what the parts returned. On a first run that's every section: About you, Todo
list, Labels, Planning, Shopping, Notifications, the style body.

`ntm:settings` tells them to install it and open a new chat. Add that the first
thing to run there is `/ntm:self-test`: it starts with `ready-check` and tries
the operations the jobs use, on a throwaway task. Until it's installed, every
scheduled run ends with "not configured".

A schedule change alone changes nothing in `ntm-user`: skip Packaging after it.

## Configured

Show one line of state per part, from what loads:

- About you: timezone
- Todo list: backend and todo list name
- Notifications: channel
- Style: whether `ntm-user:style` loads
- Schedule: which jobs exist, from `ntm:configure-schedule`'s listing

Ask which to change and hand off to that part, About you included; it shows its
current state and asks what to change. Then Packaging.

## What reads each section

In case they ask:

- About you: everything.
- Todo list and Labels: `ntm:conventions`.
- Planning (rhythm, days, how far ahead the week plans, the estimate pattern,
  what's never picked, what the weekly message includes): `ntm:plan` and the
  weekly planning; the estimator reads its Estimate pattern.
- Shopping (condition, delivery, what counts as a deal): the shopper and
  `ntm:price-watch`.
- Notifications: `ntm:notify`.
