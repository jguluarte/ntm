# Message rules

<!--
What each reminder's message says, for the messenger agent. A skill asks the
messenger for a type such as `reminders.morning`, and the type is the path to
its rule: Reminders > Morning. Rules are found by those names, so keep them. How
a message sounds, and how and when it escalates, is `%Theme`'s job.

Setup creates this database from this template. The user edits a rule, adds to
it, or deletes it to go back to this template's. These comments are for the
agent, and are never written into the user's database.
-->

## Reminders

<!--
What every reminder shares. Each reminder's own part below adds to it, and wins
where they differ.
-->

- Load all tasks with today's date
- Load the message history

If there are no tasks, you can exit with nothing to send.

### Morning

Morning is responsible to let the user know what's on the docket for today.
Include relevant details if any tasks have carried over (check recent history to
determine if this is a pattern, or how many times it has been missed). That
information could influence how the `%Theme` is applied to the message content.

### Afternoon

The afternoon is similar to the morning. If the set of tasks differs from what
they were this morning, note that a change happened but focus on the planned
tasks.

### Evening

This is ntm's last time to send reminders to the user.

Note changes as necessary, and what is outstanding.

### Week

The weekly reminder is a combination of describing what happened last week, and
what is scheduled for the upcoming week. By the time you're reading this, you
should have all of that information in your context.
