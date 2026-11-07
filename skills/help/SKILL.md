---
name: help
description: >-
    What Neurodivergent Task Manager is and how to use it, answered from the
    installed plugin's README. Shown when the user asks what ntm does, how to
    get started, what a skill is for, or for help with ntm.
---

# ntm:help

The README is the one text about ntm. This skill reads it and answers the person
from it, in prose; it never pastes the file.

## Finding the README

```bash
find ~/.claude/plugins -path '*ntm*' -name README.md -not -path '*ntm-user*'
```

Read the file it finds and answer from it. If nothing is found, say in one line
that Neurodivergent Task Manager (ntm) is a personal task system on the user's
own todo list, with reminders in their own style and a price watch, and that the
README is on the plugin's Contents tab under Customize > Plugins, or in the
repository.

## Answering

- **How do I start?** The README's First steps, told as the next thing to do:
  connect the system that holds their tasks, run `/ntm:configure`, install
  `ntm-user`, run `/ntm:self-test`.
- **What does X do?** Find X in the README (Skills, What's what, the customize
  list) and answer with that, plus the one-line call to make.
- **Where does a value live, what can I change?** Where your values live and
  What you can customize.
- **What does it send where?** That section, as written.
- **Anything else about ntm:** the section that covers it, in prose.

Keep it short: the section they asked about, not the whole file. If the answer
isn't in the README, say so and name the skill that would know (`/ntm:settings`
for a current value, `/ntm:configure-schedule` for the jobs).
