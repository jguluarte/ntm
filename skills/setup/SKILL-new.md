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

Setup is a conversation, one question at a time, never a form. Speak as ntm, in
the first person, as the intro does. Do all the talking first, so the build runs
without stopping.

Each area ends by saving what the user agreed to, with no separate ask: what it
makes on the task list, and its values in the `Settings` database. Step 2
creates `Settings` and step 3 `Style`, each as its area ends; step 8 creates the
other databases. What goes into their plugin (the backend, the channel, any
keys) is kept for the build.

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
says under The backend and Linear. Leave out its price watch project: step 5
makes that project when they pick price watch.

Confirm the name of the `Settings` database, as `references/databases.md` says.
Create it from its template with only their timezone under About you; each later
area adds its own section.

### 3. The persona

The persona is the character who writes every reminder, so the reminders get
read. Push a little when they decline: without one, ntm is no different from
Apple or Google reminders.

Open with: "think about the formula of a show you enjoy, where they can snap
back at you when you need it, or celebrate you when you've earned it".

Build it with them as `references/persona.md` says. Its parts are the ones in
the `Style` template.

Confirm the names of the `Style` and `Message history` databases. Then save the
persona: create the `Style` database from its template, with their persona in
place of the placeholders.

### 4. Features

Offer these as a numbered list. They pick everything or a subset.

| Feature         | What it is                                              |
| --------------- | ------------------------------------------------------- |
| Task management | A small task planned each weekday, with reminders       |
| Price watch     | What they want to buy, watched until the price is right |

### 5. Each picked feature

#### Task management

Read `references/rules/task-management.md`.

Propose its jobs from the table under What a job can run in `ntm:schedules`.
Agree a time for each, and keep the schedule for the handoff.

Then its labels, $no-autoschedule and $pending-shipment, as
`references/todo-list.md` says under Labels.

Confirm the names of the `Message rules`, `Paused dates` and `Task review log`
databases. Save its two label names in Settings, under Labels and as the labels
to exclude under Planning.

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
Then say in a line where each database lives.

### 9. The build

Say in a few lines what's about to happen, and wait for their go-ahead.

Then narrate as you go: build their plugin as `references/build.md` says,
install it, and hand off with one prompt for a new chat:

```
Run /ntm:self-test. If it passes, run
/ntm:schedules --setup "<schedules and model>"
```

`<schedules and model>` holds the schedule of each feature picked in this run
and the jobs' model, in their words.

Tell them, in a line meant to make them smile, that a passing self-test sends a
success message in their persona, in chat and on their phone.

## Already set up

Say in a line what the Built line in `ntm-user:backend` names: the versions,
backend, channel and features. Offer each feature they haven't picked, then ask
what else to change. Walk the step for each change, then steps 8 and 9.

| Change                           | Step                       |
| -------------------------------- | -------------------------- |
| A feature they pick              | 5 for that feature, then 6 |
| The task list                    | 2                          |
| A label's name                   | 5, its feature's labels    |
| The channel or the Pushover keys | 7                          |

With no feature picked, step 9 hands off with `Run /ntm:self-test.` alone.

Their persona, settings and jobs change without a build, with `/ntm:style`,
`/ntm:settings` and `/ntm:schedules`.
