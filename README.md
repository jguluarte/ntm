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

### `/ntm:setup`

Sets ntm up for you in one conversation, a question at a time. It connects to
your task list, asks which features you want, helps you create the style your
reminders are written in, and works out how they reach you. At the end you
install your own ntm plugin, which holds everything you chose, and a quick test
checks that it all works.

### `/ntm:today`

Lists what's planned on your task list: every open task planned for today. Add a
few words to narrow it down, such as `/ntm:today errands` for today's errands
only.

### `/ntm:fix-task-list`

Clears dates on previously planned tasks that didn't finish.
