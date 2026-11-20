---
name: help
description: >-
    Shows the user ntm's README: what Neurodivergent Task Manager (ntm) is and
    what each of its skills does. Run when the user asks about ntm ("what does
    ntm do", "help with ntm", "how do I use ntm").
---

# ntm:help

Read `${CLAUDE_PLUGIN_ROOT}/README.md` and render it to the user, word for word.
Leave out its "Install ntm" and "Skills that run on their own" sections: whoever
asks for help has ntm installed, and wants the skills they run.
