---
name: help
description: What Neurodivergent Task Manager (ntm) is and how to use it, answered from the installed plugin's README. Shown when the user asks what ntm does, how to get started, what a skill is for, or for help with ntm.
---

# neurodivergent-task-manager:help

The README is the one text about ntm. This skill reads it and answers the person
from it, in prose; it never pastes the file.

## Finding the README

```bash
find ~/.claude/plugins -path '*neurodivergent-task-manager*' -name README.md -not -path '*/user-plugin/*'
```

Read the file it finds and answer from it. If nothing is found, say in one line
that ntm is a personal task system on the user's own todo list, with reminders
in their own style and a price watch, and that the README is on the plugin's
Contents tab under Customize > Plugins, or in the repository.

## Answering

- **How do I start?** The README's First steps, told as the next thing to do:
  connect the system that holds their tasks, run
  `/neurodivergent-task-manager:configure`, install
  `ntm`, run `/neurodivergent-task-manager:self-test`.
- **What does X do?** Find X in the README (the skill tables, What's what, the
  customize list) and answer with that, plus the one-line call to make.
- **Where does a value live, what can I change?** Where your values live and
  What you can customize.
- **What does it send where?** That section, as written.
- **Anything else about ntm:** the section that covers it, in prose.

Keep it short: the section they asked about, not the whole file. If the answer
isn't in the README, say so and name the skill that would know
(`/neurodivergent-task-manager:settings`
for a current value, `/neurodivergent-task-manager:configure-schedule` for the
jobs).
