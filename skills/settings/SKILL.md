---
name: settings
description: Shows the user's ntm settings (ntm-user:settings) and changes them: a line, a section, Deviations, or the trigger word. The one place ntm-user.plugin is regenerated; every configure skill ends here. Run when the user says "show my settings", "change my timezone", "add a deviation", "rename the trigger word", or asks where a value lives.
---

# ntm:settings

`ntm-user:settings` holds every value of the user's: About you, Board, Labels, Notifications, Deviations. It lives in the `ntm-user` plugin, which only this skill produces. Changing a value means a new `ntm-user.plugin` the user installs in place of the old one.

## Usage

```
/ntm:settings
/ntm:settings <words>
```

## Bare

Load `ntm-user:settings` by name. If it won't load, say in one line that nothing is configured yet and that `/ntm:configure` is the start, and stop.

Show it section by section, as written, with the Pushover keys shortened to their last four characters. Then say what can change here: a line (a name, a timezone, a label's real name), a whole section, Deviations (anything they do differently from `ntm:conventions`), and the trigger word. Add that `/ntm:configure <part>` is the guided version for a whole part.

## With words

Load `ntm-user:settings` by name. If it won't load, only the trigger word can change (see Trigger word). For anything else, say `/ntm:configure` is the start and stop.

Make that change:

- **A line:** find it by section and label and write the new value in the same style. Ask once if the words leave the line unclear.
- **A section:** the text they give replaces the section under its heading. A `configure-<part>` arriving here brings its sections the same way.
- **Deviations:** write what they say under `## Deviations`, as they say it; `ntm:conventions` reads it last and lets it override. To drop one, remove its lines.
- **The trigger word:** see Trigger word.

Then regenerate, as the next section says. When the words only ask to see something, show it and stop.

## Regenerating `ntm-user.plugin`

The only place this happens. Every `configure-<part>` and `ntm:configure` ends by loading this skill and following this section with the section text it produced.

1. **The template** is `references/user-plugin/` in this skill's folder: `plugin.json.template`, `README.md`, `skills/settings/SKILL.md.template`, `skills/style/SKILL.md.template` (the `.template` suffix keeps the plugin installer from reading them as a second plugin). Copy it to a fresh folder and put the files in their installed places: `rm -rf /tmp/ntm-user && cp -r <this skill's folder>/references/user-plugin /tmp/ntm-user && cd /tmp/ntm-user && mkdir .claude-plugin && mv plugin.json.template .claude-plugin/plugin.json && mv skills/settings/SKILL.md.template skills/settings/SKILL.md && mv skills/style/SKILL.md.template skills/style/SKILL.md`.
2. **The current values.** Load `ntm-user:settings` and `ntm-user:style` by name. One that won't load means the template's own text is the current one.
3. **`skills/settings/SKILL.md`:** the template's text above `## About you`, then the current sections, with each changed section in place of its current one under the same heading. A section nobody has set keeps the template's text, hints included.
4. **`skills/style/SKILL.md`:** the same way: the template's frontmatter and opening line, then the current body, or the new one when the style changed. A handed-in profile goes in as `ntm:configure-style` returned it: its `Profanity:` line, its `## When something keeps slipping` section and its `## Motifs` section when it has one, then the unchanged body.
5. **Bump the version** in `.claude-plugin/plugin.json`: `1.<YYYYMMDD>.<HHMM as a number>` from the session clock, `1.$(date -u +%Y%m%d).$((10#$(date -u +%H%M)))`, which is always higher than the last regeneration's.
6. **Zip:** `cd /tmp/ntm-user && rm -f /tmp/ntm-user.plugin && zip -r /tmp/ntm-user.plugin .`
7. **Present:** copy it to the session's outputs folder, the folder the session's instructions name for files to hand back (`/mnt/user-data/outputs/` on chat). That copy is what shows the accept card in Cowork; say where it is. Where a SendUserFile tool exists, send it with that as well.
8. **Then say:** install it in place of the old one (from Customize > Plugins if no card appears), open a new chat, and run `/ntm:self-test`.

Never paste the keys back into chat; they go in the file.

## Trigger word

`ntm` is the trigger word on every skill (`/ntm:plan`, `ntm-user`). A renamed copy differs from the template only by `name` in `plugin.json` and the trigger word in its text. The substitution is whole-word and in two forms: `ntm` becomes the new word, `NTM` becomes the new word in capitals. That covers `/ntm:`, `ntm:`, `ntm-user`, the `NTM:` note-title defaults and the `ntm-user` displayName; nothing in either plugin spells the trigger word any other way. Note titles already written into the user's Board stay as they are.

1. **The word.** Ask for it: one word, lowercase letters, digits and hyphens. Below it is `<word>`, and `<WORD>` in capitals.
2. **The template bytes.** Start with a fresh, empty folder: `rm -rf /tmp/ntm-rename && mkdir -p /tmp/ntm-rename/<word>`. Load `ntm:conventions` and read its `Template source:` line. A URL: `curl -sL -o /tmp/ntm-rename/template.zip <url>` in Bash. `none yet` (the line reads so until a release sets it): ask the user to attach the `ntm` zip they installed, and wait for it. Unpack it into that folder: `cd /tmp/ntm-rename/<word> && unzip -q <the zip>`. The commands below find the folder that holds `.claude-plugin/` themselves.
3. **The substitution**, over every text file in that folder, in one Bash call. `OLD` is the template's own trigger word, read from `name` in its `.claude-plugin/plugin.json`, so the commands hold no trigger word of their own:

   ```bash
   cd "$(dirname "$(find /tmp/ntm-rename/<word> -path '*/.claude-plugin/plugin.json' | head -1)")/.."
   OLD=$(sed -n 's/.*"name": *"\([^"]*\)".*/\1/p' .claude-plugin/plugin.json | head -1)
   [ -n "$OLD" ] || { echo "no plugin name found"; exit 1; }
   grep -rlw -e "$OLD" -e "${OLD^^}" . | xargs perl -pi -e "next if /^Template source:/; s/\\b$OLD\\b/<word>/g; s/\\b${OLD^^}\\b/<WORD>/g"
   grep -rnw -e "$OLD" -e "${OLD^^}" . | grep -v '^.*Template source:'
   ```

   The last line must print nothing. The `Template source:` line in `conventions` stays verbatim, so the upstream watch still finds the release. `plugin.json`'s `name` is now `<word>`; its `version` stays the template's.
4. **Package:** `cd /tmp/ntm-rename/<word> && zip -r /tmp/<word>.plugin .`
5. **First run** (`ntm-user:settings` won't load): present `/tmp/<word>.plugin` as Regenerating's step 7 says, and end with: install it, uninstall `ntm`, open a new chat and run `/<word>:configure` to continue. Nothing else exists yet to rename.
6. **Configured:** also regenerate `ntm-user` under the new word: follow Regenerating from step 1 with `/tmp/ntm-rename/<word>/skills/settings/references/user-plugin/` as the template (step 3 already renamed it), copied to `/tmp/<word>-user`. The result is `<word>-user.plugin`, version bumped like any regeneration. Present both files as Regenerating's step 7 says. Tell them: install both, then uninstall the originals (`ntm` and `ntm-user`), open a new chat and run `/<word>:self-test`.
7. **The jobs.** Load `ntm:configure-schedule` for its Tools and Already set up sections. `list_triggers` and match the jobs as Already set up says. For each one, `update_trigger` with its stored prompt (`derived_state.prompt`) after the substitution of step 3: `ntm` → `<word>` and `NTM` → `<WORD>`, whole-word. Don't re-read the prompt files: the installed plugin's still carry the old word. Titles, times and history stay.
8. **Upstream watch.** Ask: should the weekly job watch upstream for changes? If yes, and `Template source:` names a URL, `update_trigger` the weekly planning job with this step added at the end of its stored prompt: `Last: download the zip at the Template source: line of <word>:conventions with curl -sL -o /tmp/template.zip <url>, unpack it into an empty folder, and compare version in the top .claude-plugin/plugin.json with the Version: line in <word>:conventions. When it's newer, end the reply with: template <v> is published; run /<word>:settings to regenerate.` Nothing else: a scheduled run never presents a `.plugin`. With `none yet`, say the watch can't be set until a release names a source, and that `/<word>:settings` can add it then.
