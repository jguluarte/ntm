# The job frame

Every job's prompt is this frame, filled in: the ready check first, then the
job's steps, then what the run ends with. It lives in the prompt, so no skill
carries it and a chat run never loads it.

```
<Title>.
Timezone: <Timezone from About you>.
<Planning: ..., only when it differs from plan's defaults>
<Weekly message: ..., the week ahead only; always written there>
1. Run `/ntm:ready-check --notify-failure <key>`. On
   `Ready-check FAILED`, end the run with what it returned.
<steps>
Final reply: what the last step returned, as it came, then every
other line earlier steps returned. A `... FAILED` line from a later
step ends the run with that line, unless that step says to carry on;
never send it through ntm-user:notify. If a skill can't be loaded,
end the run with:
`<Title> FAILED: <skill> couldn't be loaded; check ntm is enabled.`
```

## The key

A job's key is its last step's call: the type for a reminder job (`morning`,
`afternoon`, `evening`, `week`, `completed`), `price-watch` for the price watch.
The ready check's failure push carries it, so what Notifications says about one
job keeps matching.

## The steps

Numbered from 2, one per skill, in the order they run:

```
2. Load `ntm:<skill>` and run `/ntm:<skill> <arguments>`.
```

A step whose failure shouldn't end the run says so on the next line:
``On `<Skill> FAILED`, carry on.``
