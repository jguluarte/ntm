---
name: help
description: >-
    What Neurodivergent Task Manager (ntm) is and how to use it, answered from
    the installed plugin's README. Shown when the user asks what ntm does, how
    to get started, what a skill is for, or for help with ntm.
---

# ntm:help

The plugin's README is the one text about ntm. This skill holds none of it: it
finds the README and answers from it.

## Finding the README

```bash
find ~/.claude/plugins -path '*neurodivergent-task-manager*' -name README.md
```

If nothing is found, say in one line that the README is on the plugin's Contents
tab under Customize > Plugins, or in the repository, and stop.

## Answering

Read the file. Answer the question from the section that covers it, in prose,
short; never paste the whole file. With no specific question, give its opening
paragraph and First steps. If the README doesn't answer it, say so and name the
skill in its Skills list that would know.
