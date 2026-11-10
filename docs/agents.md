# Agents

An agent does one job for the skills that ask it; you don't run one yourself.
Some use a database: a record ntm keeps on your task list, which you can read
and change.

## The messenger

The messenger sends your reminders, with one question in mind: what will make
you actually read this one? A reminder hands it the facts, such as today's
tasks. It writes the message in your style, takes its tone from the day, and
sends it through the channel you chose. It has no fixed shape: the same message
every day stops getting read.

Every reminder goes through it, whether a job sends it on schedule or you run it
by hand.

### Message rules

Your Message rules database says, for each reminder, what its message holds and
what list goes under it: the evening rule, for example, covers what's still open
and what got done. A rule can also say when a reminder isn't needed, and then
nothing is sent. Edit a rule to change its reminder, or delete it to go back to
ntm's own. How the message sounds is your style's job.

## The estimator

The estimator works out how big each task is, the way you would size it, and
whether you could do all of it in one go after a workday. An estimate is in
hours unless your settings say otherwise, and goes on the last line of the
task's description in full words, such as `Estimate: 2 hours`.

When ntm picks tasks to plan, it asks the estimator how long each one takes. In
a review of the task list with you, the estimator proposes each task's estimate
and records the one you decide on.

### Task review log

Your Task review log database is how the estimator's guesses get closer to
yours, review after review. It holds what it has learned about how you work: how
you like tasks written and broken up, how you like a review to go, and what you
keep correcting. It also holds each estimate you decided, beside its guess.
