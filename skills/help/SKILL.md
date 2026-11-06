---
name: help
description: What Neurodivergent Task Manager (ntm) is and how to use it, answered from the installed plugin's README. Shown when the user asks what ntm does, how to get started, what a skill is for, or for help with ntm.
---

# ntm:help

The README is the one text about ntm. This skill reads it and answers the person from it, in prose; it never pastes the file.

## What ntm is

Say this in your own words when they ask what ntm is or where it came from, and let the README fill in the rest.

Neurodivergent Task Manager (ntm) is a personal task system on the user's own board. It was built by one person for the places that got in their way: starting things, keeping multi-day work moving, noticing when things have quietly gone stale, not forgetting things, and buying on a good price instead of on impulse. The price watch is there to bridge the impulse to buy: sometimes we buy right away only so we don't forget, and we don't always still want it later; an item on the watch isn't forgotten, and waiting for a good price becomes the easy option.

The trigger word is the plugin's name, `ntm`; to use another, fork the template and rename it with your agent (whole-word `ntm` to yours and `NTM` to yours in capitals, in every file and in `plugin.json`'s `name`), then create your jobs from that copy.

## Finding the README

```bash
find ~/.claude/plugins -path '*/ntm/README.md'
```

Read the file it finds. If nothing is found, say where to read it: the plugin's Contents tab under Customize > Plugins, or the repository. Then answer what you can from the section above.

## Answering

- **How do I start?** The README's First steps, told as the next thing to do: connect the system that holds their tickets, run `/ntm:configure`, install `ntm-user`, run `/ntm:self-test`.
- **What does X do?** Find X in the README (the skill tables, What's what, the customize list) and answer with that, plus the one-line call to make.
- **Where does a value live, what can I change?** Where your values live and What you can customize.
- **What does it send where?** That section, as written.
- **Anything else about ntm:** the section that covers it, in prose.

Keep it short: the section they asked about, not the whole file. If the answer isn't in the README, say so and name the skill that would know (`/ntm:settings` for a current value, `/ntm:configure-schedule` for the jobs).
