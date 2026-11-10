---
name: setup
description: >-
    The ntm wizard. Takes a new user from a fresh install to a connected task
    list, a persona, the features they pick and reminders on their phone, then
    builds their ntm-user plugin. Run when the user says "set up ntm", "get
    started" or "set up my todo list", or installs ntm for the first time;
    /ntm:update loads it to offer what's new and rebuild.
---

# ntm:setup

Setup ends with a connected task list, a persona, the features the user picked
ready to run as jobs, reminders on their phone, and their own plugin,
`ntm-user`, built and installed.

It's a conversation, one question at a time, never a form. Speak as ntm, in the
first person, as the intro does. Do all the talking first, so the build runs
without stopping.

Each area ends by saving what the user agreed to, with no separate ask: what it
makes on the task list, and its values in the `Settings` database. What goes
into their plugin (the backend, the channel, any keys) is kept for the build.

## Usage

```
/ntm:setup [<what to change, in words>]
```

Bare for a new user. Once they're set up, the words say what to change.

## Before you start

Load `ntm-user:backend`. When it loads, the user is set up: follow Already set
up. Otherwise read `references/rules/terminology.md` and
`references/rules/core.md`, the words and rules every step uses, then follow the
steps in order.

The database templates are in ntm's `references/databases/`. Their `<!-- -->`
comments are for you, never the user: a database created from one leaves them
out.

## The steps

### 1. Intro

Send `references/intro.md`. It ends by confirming their timezone.

### 2. The task list

Connect their task list and check that it answers, as `references/todo-list.md`
says under The backend and Linear. The price watch project there waits for price
watch.

Confirm the name of the `Settings` database, as `references/databases.md` says.
Create it from its template with only their timezone under About you; each later
area adds its own section.

### 3. The persona

The persona is the character who writes every reminder, so the reminders get
read. Push a little when they decline: without one, ntm is no different from
Apple or Google reminders.

Open with: "think about the formula of a show you enjoy, where they can snap
back at you when you need it, or celebrate you when you've earned it". Build it
with them from generic parts, naming no show, character or brand, as
`references/persona.md` says, in the parts of the `Style` template.

Confirm the names of the `Style` and `Message history` databases. Then save the
persona: create the `Style` database from its template, with their persona in
place of the placeholders.

### 4. Features

Offer these as a numbered list. They pick everything or a subset.

| Feature         | What it is                                              |
| --------------- | ------------------------------------------------------- |
| Task management | A small task planned each weekday, with reminders       |
| Price watch     | What they want to buy, watched until the price is right |

New features join this list.

### 5. Each picked feature

#### Task management

Read `references/rules/task-management.md`.

Agree the schedule: Monday to Friday for doing, with a morning, afternoon and
evening reminder, and Sunday for cleanup and planning, when the week just past
is wrapped up and the next one planned. Agree a time for each, and keep the
schedule for the handoff.

Then its labels, $no-autoschedule and $pending-shipment, as
`references/todo-list.md` says under Labels.

Confirm the names of the `Message rules`, `Paused dates` and `Task review log`
databases. Save its rows of the Labels section and the Planning section in
Settings.

#### Price watch

Read `references/rules/price-watch.md`.

Ask their country and currency, for where it shops and the prices it looks for.
Agree a daily time for it, kept for the handoff.

Then the project that holds what they want to buy, and its labels, $price-watch,
$has-amazon-alert and $amazon-unavailable, as `references/todo-list.md` says
under The price watch project and Labels.

Then Amazon sync, the way around cloud agents not reaching Amazon: Amazon's own
price alerts watch each item, kept in step from a browser on their computer by
`/ntm:sync-price-watch-to-amazon`. Agree how it reaches Amazon, as
`references/todo-list.md` says under Shopping.

Confirm the name of the `Price watch stores` database, with any stores they
name, as `references/databases.md` says. Save their country and currency under
About you, its rows of the Labels section and the Shopping section in Settings.

### 6. The jobs' model

Suggest a lighter model for the jobs than the one running this chat, from the
ones this app offers. Keep their choice for the handoff.

### 7. Notifications

How reminders reach them, with one test push, as `references/notifications.md`
says.

### 8. Databases

Create each database confirmed above that doesn't exist yet, from its template.
`Price watch stores` gets the stores they named. Then say in a line where each
database lives.

### 9. The build

Say in a few lines what's about to happen, and wait for their go-ahead.

Then narrate as you go: build their plugin as `references/build.md` says,
install it, and hand off with one prompt for a new chat:

```
Run /ntm:self-test. If it passes, run
/ntm:schedules --setup "<schedules and model>"
```

`<schedules and model>` holds each picked feature's schedule and the jobs'
model, in their words.

### 10. The end

A passing self-test sends a success message in their persona, in chat and on
their phone. Tell them so, in a line meant to make them smile.

## Already set up

Say in a line what the Built line in `ntm-user:backend` names: the versions,
backend, channel and features. Offer each feature they haven't picked, then ask
what else to change: the task list, a label's name, the channel or the Pushover
keys. Walk those steps, then steps 8 and 9.

Their persona, settings and jobs change without a build, with `/ntm:style`,
`/ntm:settings` and `/ntm:schedules`.
