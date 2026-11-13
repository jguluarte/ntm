# Message rules

## Reminders

<!--
What every reminder shares. Each reminder's own part below adds to it, and wins
where they differ.
-->

- Load all tasks with today's date
- Load the message history

If there are no tasks, you can exit with nothing to send.

Include relevant details if any tasks have carried over (use their days slipped
and the dates they slipped from to see if this is a pattern, or how many times
it has been missed). That information could influence how the `%Theme` is
applied to the message content.

### Morning

Morning is responsible to let the user know what's on the docket for today.

### Afternoon

The afternoon is similar to the morning. If the set of tasks differs from what
they were this morning, note that a change happened but focus on the planned
tasks.

### Evening

This is ntm's last time to send reminders to the user.

Note changes as necessary, and what is outstanding.

## Weekly

The weekly reminder is a combination of describing what happened last week, and
what is scheduled for the upcoming week. By the time you're reading this, you
should have all of that information in your context.

It is fine to include task ids in the message body.
