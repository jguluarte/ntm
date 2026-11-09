---
name: settings
description: >-
    Shows the user's ntm settings, the Settings document on their todo list, and
    says where a change goes: a section of that document, a scheduled task, the
    Style document, or a rebuild. Run when the user says "show my settings",
    "change my timezone", "rename a label", or asks where a value lives.
---

# ntm:settings

The Settings document on the user's todo list holds the values they agreed to in
setup, under fixed headings: About you, Labels, Planning, Shopping,
Notifications. A missing section means its defaults. Runs read About you,
Planning, Shopping and Notifications live, so a change there takes effect on the
next run. Labels are built into `ntm-user:backend`, so a change there needs a
rebuild.

## Usage

```
/ntm:settings
/ntm:settings <words>
```

## Setup

Load `ntm-user:backend` and read the Settings document as it says. If it won't
load, say in one line that nothing is set up yet and that `/ntm:setup` is the
start, and stop. If the read fails, or `ntm-user:backend` answers
`Backend CAN'T: <why>`, explain what happened to the user and stop.

## Where a change goes

- **About you, Planning, Shopping, Notifications:** that section of the Settings
  document.
- **Labels:** the Labels section, then `/ntm:update` rebuilds.
- **Their jobs** (what runs, on which days, at what time, the model): their
  scheduled tasks, through `ntm:schedules`.
- **How reminders talk to them:** the Style document, through `ntm:style`.
- **Built-in choices** (their backend, todo list, notification channel, Pushover
  keys, features): `/ntm:update`.
- **The trigger word `ntm`:** a renamed fork of ntm, as the README says.

## Bare

Show the Settings document section by section, as written. Then say in a line or
two where a change goes, as the list above gives it.

## With words

When the words only ask to see something, show it and stop. Asked about their
jobs, load `ntm:schedules` and list them: the scheduled tasks are the source,
and the Settings document holds no schedules.

For a change to a section of the Settings document, find the line by section and
label, write the new value in the same style, and write that section as
`ntm-user:backend` says. Ask once if the words leave the line unclear. For
Labels, add that their runs use the change once `/ntm:update` rebuilds.

For their jobs or the Style document, load the skill the list names and follow
it with their words. For anything else, say where it goes, and stop.

## Regenerating `ntm-user.plugin`

The only place this happens. Every `configure-<part>` and `ntm:configure` ends
by loading this skill and following this section with the section text it
produced.

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

### 3: `ntm-user:style`

Its description says it writes ntm's reminders in the user's style, run by the
messenger, changed with `/ntm:configure-style`. The messenger calls it as
`/ntm-user:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>`:
`<reminder>` is `morning`, `afternoon`, `evening`, `week` or `completed` and
implies `--stay-fresh`; the tone is freeform. It must:

- rewrite the message in the user's register, from their Profile
  (`references/builder.md` in `ntm:configure-style` says what each section
  means);
- with `--stay-fresh`, use the message history database, read through
  `ntm:conventions`. Keep lines fresh: avoid what recent entries used. Let a
  slipping task climb: a carried-over task's earlier days are the days before
  today whose entries name its id, and its level is the one the Profile's When
  something keeps slipping section gives for that count (for a persona, its own
  levels); any other task is on the first level. Then add one entry, with
  today's date, the new line and the task ids the tone names, pruned to the
  `Keep:` line in the database's frontmatter;
- with `--for`, end with a `Title:` line that says what the message is about in
  the same style, never just the reminder's name;
- output only the message, plain text, and that `Title:` line.

For plain or a theme, it carries the Profile `ntm:configure-style` wrote, and
its procedure is written fresh from the list above every time; for a persona,
the persona's body as handed in, under the `## For ntm` section
`configure-style` wrote. When nothing changed, the current Profile, or persona
and section, goes in as it is.

### 4: Zip

```
cd /tmp/ntm-user && rm -f /tmp/ntm-user.plugin &&
    zip -r /tmp/ntm-user.plugin .
```

Without `zip`, the last command is
`python3 -m zipfile -c /tmp/ntm-user.plugin .`.

### 5: Present

Copy it to the session's outputs folder, the folder the session's instructions
name for files to hand back (`/mnt/user-data/outputs/` on chat). That copy is
what shows the accept card in Cowork; say where it is. Where a SendUserFile tool
exists, send it with that as well.

### 6: Then say

Install it in place of the old one (from Customize > Plugins if no card
appears), open a new chat, and run `/ntm:self-test`.
