---
name: help
description: >-
    What Neurodivergent Task Manager (ntm) is and how to use it, answered from
    the installed plugin's README. Shown when the user asks what ntm does, how
    to get started, what a skill is for, or for help with ntm.
---

# ntm:help

Answer from the plugin's README. This skill holds no text about ntm itself.

## Find the README

```bash
find ~/.claude/plugins -path '*ntm*' -name README.md -not -path '*ntm-user*'
```

If nothing is found, say in one line that the README is on the plugin's Contents
tab under Customize > Plugins, or in the repository, and stop.

## Answer

Read the README and answer from the section that covers the question: short, in
prose, never the whole file. With no specific question, give its opening
paragraph and First steps. If the README doesn't answer it, say so and name the
skill in its Skills list that would know.
