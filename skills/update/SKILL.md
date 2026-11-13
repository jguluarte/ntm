---
name: update
description: >-
    Brings the user's setup up to the installed version of ntm, with them in
    chat: shows what changed since their last update, walks them through what
    each new version asks of them, and rebuilds their ntm-user plugin when a
    version needs it. Run by the user in chat after installing a new version of
    ntm, never by a job ("update ntm", "what's new in ntm", "I installed a new
    version").
---

# ntm:update

Takes the user's setup from the version of ntm it last took in to the installed
one, a version at a time, from each version's update note.

## Usage

```
/ntm:update
```

## Setup

Run `/ntm:ready-check`, unless it already ran in this session. It loads
`ntm-user:backend`, `%Settings` and ntm's core rules; if it fails, end the run
with its result line.

## Updating

### 1. Find the notes

| Version   | Where it comes from                                             |
| --------- | --------------------------------------------------------------- |
| Theirs    | Version under Updates in `%Settings`; 0.4.0 when there is none  |
| Installed | `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` |

The update notes are in `references/`, each named for its version, such as
`0.5.0.md`. Take the ones newer than theirs, up to the installed version, oldest
first. With none, tell them their setup is up to date, and go to step 4.

### 2. Take in each note

For each note in turn, show its What's new, then follow its For ntm:update with
the user. Offer each change, and make only the ones they agree to.

### 3. Rebuild the user plugin

When any note says `Rebuild ntm-user: yes`, rebuild the user plugin once, after
the last note. Load `ntm:setup` and build their user plugin again the way it
does, filled in with what their installed `ntm-user` holds: their task list,
where each database lives, their channel and their connector. Have them install
it, then run `/ntm:self-test` in a new chat.

### 4. Record the version

Write the installed version to Version under Updates in `%Settings`, adding the
Updates part when it isn't there.

## Result

Tell the user which version of ntm their setup is on now, and what's left for
them, such as installing the rebuilt plugin.
