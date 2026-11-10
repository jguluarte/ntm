# Neurodivergent Task Manager (ntm)

ntm runs a personal task system on your own task list, with a few scheduled jobs
that keep it moving. It plans your days and weeks, reminds you in a style you
choose, asks in the evening how the day went, tidies what has gone stale, and
watches prices on things you want to buy.

It was built by one person for the places that got in their way: starting
things, keeping multi-day work moving, noticing when things have quietly gone
stale, not forgetting things, and buying on a good price instead of on impulse.
It stays low-process. If it starts bogging you down, turn pieces off.

More is added here as each part of ntm is rebuilt.

## Skills

A skill is something you run by name in a chat.

### `/ntm:today`

Lists what's planned on your task list: every open task planned for today. Add a
few words to narrow it down, such as `/ntm:today errands` for today's errands
only. It only reads your task list and never changes it.

## Agents

An agent does one job for the skills that ask it; you don't run one yourself.
Some use a database: a record ntm keeps on your task list, which you can read
and change.

### The messenger

The messenger sends your reminders, with one question in mind: what will make
you actually read this one? A reminder hands it the facts, such as today's
tasks. It writes the message in your style, takes its tone from the day, and
sends it through the channel you chose. It has no fixed shape: the same message
every day stops getting read.

Every reminder goes through it, whether a job sends it on schedule or you run it
by hand.

#### Message rules

Your Message rules database says, for each reminder, what its message holds and
what list goes under it: the evening rule, for example, covers what's still open
and what got done. A rule can also say when a reminder isn't needed, and then
nothing is sent. Edit a rule to change its reminder, or delete it to go back to
ntm's own. How the message sounds is your style's job.

### The estimator

The estimator works out how big each task is, the way you would size it, and
whether you could do all of it in one go after a workday. An estimate is in
hours unless your settings say otherwise, and goes on the last line of the
task's description in full words, such as `Estimate: 2 hours`.

When ntm picks tasks to plan, it asks the estimator how long each one takes. In
a review of the task list with you, the estimator proposes each task's estimate
and records the one you decide on.

#### Task review log

Your Task review log database is how the estimator's guesses get closer to
yours, review after review. It holds what it has learned about how you work: how
you like tasks written and broken up, how you like a review to go, and what you
keep correcting. It also holds each estimate you decided, beside its guess.
