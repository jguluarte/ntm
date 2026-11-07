---
name: settings
description: >-
    Shows the user's ntm settings (ntm-user:settings) and changes them: a line,
    a section, or Deviations. The one place ntm-user.plugin is regenerated;
    every configure skill ends here. Run when the user says "show my settings",
    "change my timezone", "add a deviation", or asks where a value lives.
---

# ntm:settings

`ntm-user:settings` holds every value the user agreed to: About you, Todo list,
Labels, Planning, Shopping, Notifications, Deviations. It lives in the
`ntm-user` plugin, which only this skill produces. Changing a value means a new
`ntm-user.plugin` the user installs in place of the old one.

## Usage

```
/ntm:settings
/ntm:settings <words>
```

## Bare

Load `ntm-user:settings` by name. If it won't load, say in one line that nothing
is configured yet and that `/ntm:configure` is the start, and stop.

Show it section by section, as written, with the Pushover keys shortened to
their last four characters. Then say what can change here: a line (a name, a
timezone, a label's real name, the planning rhythm), a whole section, and
Deviations (anything they do differently from `ntm:conventions`). Add that
`/ntm:configure <part>` is the guided version for a whole part, and that a
different trigger word than `ntm` means a renamed fork of ntm, as the README
says.

## With words

Load `ntm-user:settings` by name. If it won't load, say `/ntm:configure` is the
start and stop.

Make that change:

- **A line:** find it by section and label and write the new value in the same
  style. Ask once if the words leave the line unclear.
- **A section:** the text they give replaces the section under its heading. A
  `configure-<part>` arriving here brings its sections the same way.
- **Deviations:** write what they say under `## Deviations`, as they say it;
  `ntm:conventions` reads it last and lets it override. To drop one, remove its
  lines.

Then regenerate, as the next section says. When the words only ask to see
something, show it and stop.

## Regenerating `ntm-user.plugin`

The only place this happens. Every `configure-<part>` and `ntm:configure` ends
by loading this skill and following this section with the section text it
produced.

You build `ntm-user` yourself from this guide, in a fresh folder,
`/tmp/ntm-user`; it says what the plugin must hold, not its text. First load
`ntm-user:settings` and `ntm-user:style` by name: what loads is the current
text; what won't is new. If something you need is missing, build what you can
and say what's missing.

1. **The plugin:** named `ntm-user`, with a one-sentence description: the user's
   settings and style for ntm, kept private because it can hold notification
   keys. Version `1.<YYYYMMDD>.<HHMM as a number>` from the session clock,
   `1.$(date -u +%Y%m%d).$((10#$(date -u +%H%M)))`, which is always higher than
   the last regeneration's.
2. **`ntm-user:settings`:** its description says it holds the user's values for
   ntm, read by `ntm:conventions`, changed with `/ntm:settings`. Its sections
   are the headings `ntm:conventions` reads, in its order: About you, Todo list,
   Labels, Planning, Shopping, Notifications, Deviations. A changed section is
   the text its configure skill returned, which says what it holds; every other
   section is carried over unchanged. A section nobody has set is its heading
   alone, which means its defaults.
3. **`ntm-user:style`:** its description says it writes ntm's reminders in the
   user's style, run by the messenger, changed with `/ntm:configure-style`. The
   messenger calls it as
   `/ntm-user:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>`:
   `<reminder>` is `morning`, `afternoon`, `evening`, `week` or `completed` and
   implies `--stay-fresh`; the tone is freeform. It must:
    - rewrite the message in the user's register, from their Profile
      (`references/builder.md` in `ntm:configure-style` says what each section
      means);
    - with `--stay-fresh`, keep lines fresh: read the message history database
      through `ntm:conventions`, avoid what recent entries used, and add the new
      line, pruned to the `Keep:` line in the database's frontmatter;
    - with `--for`, end with a `Title:` line that says what the message is about
      in the same style, never just the reminder's name;
    - output only the message, plain text, and that `Title:` line.

    For plain or a theme, it carries the Profile `ntm:configure-style` wrote;
    for a persona, the persona's body as handed in, under the `## For ntm`
    section `configure-style` wrote. When nothing changed, the current one goes
    in as it is.

4. **Zip:**
   `cd /tmp/ntm-user && rm -f /tmp/ntm-user.plugin && zip -r /tmp/ntm-user.plugin .`
   (without `zip`: `python3 -m zipfile -c /tmp/ntm-user.plugin .`).
5. **Present:** copy it to the session's outputs folder, the folder the
   session's instructions name for files to hand back (`/mnt/user-data/outputs/`
   on chat). That copy is what shows the accept card in Cowork; say where it is.
   Where a SendUserFile tool exists, send it with that as well.
6. **Then say:** install it in place of the old one (from Customize > Plugins if
   no card appears), open a new chat, and run `/ntm:self-test`.

Never paste the keys back into chat; they go in the file.
