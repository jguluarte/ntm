---
name: settings
description: Shows the user's ntm settings (ntm-user:settings) and changes them: a line, a section, or Deviations. The one place ntm-user.plugin is regenerated; every configure skill ends here. Run when the user says "show my settings", "change my timezone", "add a deviation", or asks where a value lives.
---

# ntm:settings

`ntm-user:settings` holds every value the user agreed to: About you, Todo list, Labels, Planning, Shopping, Notifications, Deviations. It lives in the `ntm-user` plugin, which only this skill produces. Changing a value means a new `ntm-user.plugin` the user installs in place of the old one.

## Usage

```
/ntm:settings
/ntm:settings <words>
```

## Bare

Load `ntm-user:settings` by name. If it won't load, say in one line that nothing is configured yet and that `/ntm:configure` is the start, and stop.

Show it section by section, as written, with the Pushover keys shortened to their last four characters. Then say what can change here: a line (a name, a timezone, a label's real name, the planning rhythm), a whole section, and Deviations (anything they do differently from `ntm:conventions`). Add that `/ntm:configure <part>` is the guided version for a whole part, and that a different trigger word than `ntm` means a renamed fork of the template, as the README says.

## With words

Load `ntm-user:settings` by name. If it won't load, say `/ntm:configure` is the start and stop.

Make that change:

- **A line:** find it by section and label and write the new value in the same style. Ask once if the words leave the line unclear.
- **A section:** the text they give replaces the section under its heading. A `configure-<part>` arriving here brings its sections the same way.
- **Deviations:** write what they say under `## Deviations`, as they say it; `ntm:conventions` reads it last and lets it override. To drop one, remove its lines.

Then regenerate, as the next section says. When the words only ask to see something, show it and stop.

## Regenerating `ntm-user.plugin`

The only place this happens. Every `configure-<part>` and `ntm:configure` ends by loading this skill and following this section with the section text it produced.

1. **The template** is `references/user-plugin/` in this skill's folder (the directory this SKILL.md was loaded from): `plugin.json.template`, `README.md`, `skills/settings/SKILL.md.template`, `skills/style/SKILL.md.template` (the `.template` suffix keeps the plugin installer from reading them as a second plugin). Copy it to a fresh folder and put the files in their installed places: `rm -rf /tmp/ntm-user && cp -r <this skill's folder>/references/user-plugin /tmp/ntm-user && cd /tmp/ntm-user && mkdir .claude-plugin && mv plugin.json.template .claude-plugin/plugin.json && mv skills/settings/SKILL.md.template skills/settings/SKILL.md && mv skills/style/SKILL.md.template skills/style/SKILL.md`.
2. **The current values.** Load `ntm-user:settings` and `ntm-user:style` by name. One that won't load means the template's own text is the current one.
3. **`skills/settings/SKILL.md`:** the template's text above `## About you`, then the current sections, with each changed section in place of its current one under the same heading. A section nobody has set keeps the template's text, hints included.
4. **`skills/style/SKILL.md`:** the template is the whole skill with an empty Profile. A Profile from `ntm:configure-style` (plain or a theme) replaces the template's `## Profile` section, hints included, heading kept; the Usage and the procedure stay the template's. A handed-in persona replaces everything below the template's frontmatter: the `## For ntm` section `configure-style` wrote, then the persona's body, unchanged. When nothing changed, the current `ntm-user:style` goes in as it is.
5. **Bump the version** in `.claude-plugin/plugin.json`: `1.<YYYYMMDD>.<HHMM as a number>` from the session clock, `1.$(date -u +%Y%m%d).$((10#$(date -u +%H%M)))`, which is always higher than the last regeneration's.
6. **Zip:** `cd /tmp/ntm-user && rm -f /tmp/ntm-user.plugin && zip -r /tmp/ntm-user.plugin .` (without `zip`: `python3 -m zipfile -c /tmp/ntm-user.plugin .`).
7. **Present:** copy it to the session's outputs folder, the folder the session's instructions name for files to hand back (`/mnt/user-data/outputs/` on chat). That copy is what shows the accept card in Cowork; say where it is. Where a SendUserFile tool exists, send it with that as well.
8. **Then say:** install it in place of the old one (from Customize > Plugins if no card appears), open a new chat, and run `/ntm:self-test`.

Never paste the keys back into chat; they go in the file.
