---
name: settings
description: >-
    Shows the user's ntm settings, the `%Settings` document on their todo list,
    and changes them, or says where a change goes: a scheduled task, the
    `%Style` document, or a rebuild. Run when the user says "show my settings",
    "change my timezone", "rename a label", or asks where a value lives.
---

# ntm:settings

The `%Settings` document on the user's todo list holds the values they agreed to
in setup, under fixed headings: About you, Labels, Planning, Shopping,
Notifications. A missing section means its defaults.

## Usage

```
/ntm:settings
/ntm:settings <words>
```

## Setup

Load `ntm-user:backend` to read the user's conventions. If it won't load, say in
one line that nothing is set up yet and that `/ntm:setup` is the start, and
stop.

If the `%Settings` document can't be read or written, say what went wrong and
stop.

## Where a change goes

- **About you, Planning, Shopping, Notifications:** that section of the
  `%Settings` document; the next run uses it.
- **Labels:** the Labels section, then `/ntm:update` rebuilds.
- **Their jobs** (what runs, on which days, at what time, the model): their
  scheduled tasks, through `ntm:schedules`.
- **How reminders talk to them:** the `%Style` document, through `ntm:style`.
- **Built-in choices** (their backend, todo list, notification channel, Pushover
  keys, features): `/ntm:update`.

## Bare

Read the `%Settings` document and show it section by section, as written. Then
say in a line or two where a change goes, as the list above gives it.

## With words

When the words only ask to see the `%Settings` document, show it and stop. For a
change to a section of it, find the line by section and label, and write the new
value in the same style; ask once if the words leave the line unclear. For their
jobs or the `%Style` document, load the skill the list names and follow it with
their words. For anything else, say where it goes, and stop.

## Regenerating `ntm-user.plugin`

You build `ntm-user` yourself from this guide, in a fresh folder,
`/tmp/ntm-user`; it says what the plugin must hold, not its text. First load
`ntm-user:settings` and `ntm-user:style` by name: what loads is the current
text; what won't is new. If something you need is missing, build what you can
and say what's missing.

Never paste the keys back into chat; they go in the file.

### 1: The plugin

Named `ntm-user`, with a one-sentence description: the user's settings and style
for ntm, kept private because it can hold notification keys. Version
`1.<YYYYMMDD>.<HHMM as a number>` from the session clock,
`1.$(date -u +%Y%m%d).$((10#$(date -u +%H%M)))`, which is always higher than the
last regeneration's.

### 2: `ntm-user:settings`

Its description says it holds the user's values for ntm, read by
`ntm:conventions`, changed with `/ntm:settings`. Its sections are the headings
`ntm:conventions` reads, in its order: About you, Todo list, Labels, Planning,
Shopping, Notifications, Deviations. A changed section is the text its configure
skill returned, which says what it holds; every other section is carried over
unchanged. A section nobody has set is its heading alone, which means its
defaults.

### 3: Zip

```
cd /tmp/ntm-user && rm -f /tmp/ntm-user.plugin &&
    zip -r /tmp/ntm-user.plugin .
```

Without `zip`, the last command is
`python3 -m zipfile -c /tmp/ntm-user.plugin .`.

### 4: Present

Copy it to the session's outputs folder, the folder the session's instructions
name for files to hand back (`/mnt/user-data/outputs/` on chat). That copy is
what shows the accept card in Cowork; say where it is. Where a SendUserFile tool
exists, send it with that as well.

### 5: Then say

Install it in place of the old one (from Customize > Plugins if no card
appears), open a new chat, and run `/ntm:self-test`.
