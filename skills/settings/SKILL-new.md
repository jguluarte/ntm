---
name: settings
description: >-
    Shows and changes the user's ntm settings, kept on their todo list, or says
    where a change goes. Run when the user says "show my settings", "change my
    timezone", "rename a label", or asks where a value lives.
---

# ntm:settings

The user's `Settings` database holds the values they agreed to in setup: About
you, Labels, Planning, Shopping and Notifications. Skills read it as they run,
so a change there reaches the next run.

## Setup

Load `ntm-user:backend` to read the user's conventions, then read the user's
`Settings` database. The comments in its template,
`references/databases/settings.md` in the newest installed `ntm`, say what each
section holds and how it's written. Follow them whenever you save it. If it
can't be read or written, say what went wrong.

## Usage

```
/ntm:settings [<what to see or change, in words>]
```

## Where a value lives

| Value                                        | Lives in                     | Changed by                   |
| -------------------------------------------- | ---------------------------- | ---------------------------- |
| About you, Planning, Shopping, Notifications | Settings                     | this skill                   |
| Label names                                  | Labels in Settings           | this skill                   |
| Jobs: what runs, when, and on which model    | the user's scheduled tasks   | `ntm:schedules`              |
| How reminders talk to the user               | the `Style` database         | `ntm:style`                  |
| What a reminder's message says               | the `Message rules` database | the user, on their task list |
| Backend, task list, features                 | `ntm-user`                   | `/ntm:update`                |
| Notification channel, Pushover keys          | `ntm-user:notify`            | `/ntm:update`                |

## Seeing Settings

With no words after `/ntm:settings`, or words that only ask to see Settings,
show the sections they name, or all of them, as written. Then say in a line or
two where a change goes, as the table gives it, and stop.

## Changing Settings

Find the line by its section and name, and write the new value the way the
template writes it. Ask once if their words leave the line unclear. Save it,
then show the section as it now reads.

For a renamed label, rename it on the task list too, and in Planning wherever
it's listed. Then tell the user to run `/ntm:update`, which builds the new name
into `ntm-user:backend`.

## Everything else

For their jobs or style, follow the skill the table names with their words; for
anything else, say where it lives and what changes it.
