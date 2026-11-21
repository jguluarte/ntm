---
name: update
description: >-
    Brings the user's setup up to the installed version of ntm, following each
    new version's update note. Run by the user in chat after installing a new
    version ("update ntm", "what's new in ntm", "I installed a new version"), or
    by ntm:ready-check when no new version needs the user.
---

# ntm:update

Follows each new version's update note.

## Usage

```
/ntm:update
```

## Setup

Run `/ntm:ready-check`, unless it already ran in this session or loaded this
skill. It loads `ntm-user:backend`, `%Settings` and ntm's core rules; if it
fails, end the run with its result line.

## Updating

### 1. Find the notes

| Version   | Where it comes from                                                    |
| --------- | ---------------------------------------------------------------------- |
| Theirs    | Last synced under ntm version in `%Settings`; 0.4.0 when there is none |
| Installed | `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`        |

The update notes are in `${CLAUDE_PLUGIN_ROOT}/skills/update/references/`, each
named for its version, such as `0.5.0.md`. Take the ones newer than theirs, up
to the installed version, oldest first. With none, go to step 4.

### 2. Take in each note

For each note in turn, show its What's new, then follow its For ntm:update with
the user.

### 3. Rebuild the user plugin

When any note says `Rebuild ntm-user: yes`, and any condition it names holds,
rebuild the user plugin once, after the last note, as The user plugin, ntm
backend assets and Notifications in
`${CLAUDE_PLUGIN_ROOT}/skills/setup/SKILL.md` build it, filled in from their
installed `ntm-user`'s skills and `.mcp.json`. Their `%Settings` and keys stay
as they are. Have them install it, then say "run the ntm self-test" in a new
chat.

### 4. Record the version

Write the installed version to Last synced under ntm version in `%Settings`,
adding the part when it isn't there.

## Result

Tell the user which version of ntm their setup is synced with now, and what's
left for them, such as installing the rebuilt plugin.
