# Neurodivergent Task Manager (ntm)

Ntm runs a personal task system on your own task list, with a few scheduled jobs
that keep it moving. It helps you remember things you want or need to do, using
a customized messaging style of your creation so the reminders don't turn into
noise you just ignore. It plans things for you on whatever schedule you like,
that way you can make small meaningful steps to both starting AND finishing
projects you just haven't been making time for.

Also, to help prevent impulse purchasing things "so you won't forget", it has
price watch capabilities built into it. Then you won't forget about that thing,
but you also don't have to get it right now. This also means you have time to
change your mind later, and stop watching something that you didn't really need
to begin with.

It was built by a neurodivergent human that had a lot of cool ideas, but lacked
the initiative to get started (or worse, just forgot to finish after losing
steam). This system helps them remember the things that they want to do, and
says so in a way that they don't ignore. Hopefully it'll help you too!

## Skills

These are different components of ntm that work in concert to make your AI act
like an actual assistant.

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
