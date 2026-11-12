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

These are different components of ntm that work in concert to make your AI act
like an actual assistant.

## Core skills

These are the shared pieces the rest of ntm is built on. You run setup and the
self-test once, when you start; the others are there whenever you or ntm need
them.

### `/ntm:help`

Shows you this page in the chat, any time you want to know what ntm does or what
one of its skills is for.

### `/ntm:setup`

This acts as a setup wizard to make sure you have everything needed to run ntm.
It builds a plugin of your own for you to install, and schedules your jobs once
the self-test passes.

### `/ntm:self-test`

Tries out everything setup built, on a throwaway task it cleans up afterwards,
and ends with a test message to your phone. Run it when setup asks, once you've
installed the plugin it built.

### `/ntm:ready-check`

Checks that ntm can reach your task list, and says how to fix it when it can't.
Your scheduled jobs run it first; run it yourself if something seems off.

### `/ntm:style`

Writes ntm's messages to you in the theme you created during setup, so they
sound like something you enjoy and keep changing instead of repeating. A task
you keep putting off gets a stronger nudge the longer it slips. Ask it to write
something in your style, or to change how your reminders sound.

## Task management

These skills plan your days, remind you about them and keep your task list tidy.
Some run on their own from your scheduled jobs; you can run any of them
yourself, any time.

### `/ntm:today`

Lists what's planned on your task list: every open task planned for today. Add a
few words to narrow it down, such as `/ntm:today errands` for today's errands
only.

### `/ntm:plan`

Picks what you'll work on each day: one small task a weekday, unless you chose
otherwise in setup. Scheduled jobs plan your week ahead, and each morning move
unfinished work to today. Run it yourself to plan together, such as
`/ntm:plan next week around the garage`.

### `/ntm:reminder`

Sends your morning, afternoon and evening reminders to your phone, in the style
you set up. Scheduled jobs run it for you at the times you picked.

### `/ntm:pause`

Marks days off, such as a holiday or a busy week, so nothing new gets planned
for them. Name the days in your own words, like `/ntm:pause next week`, or run
it alone to see your pauses.

### `/ntm:review`

Goes through your task list with you, a project at a time: closes what's done or
no longer needed, then estimates each task and breaks up the big ones. Stop
whenever you like.

### `/ntm:clean`

Clears dates on previously planned tasks that didn't finish, and removes pause
dates that have since passed.

## Price watch

These skills keep an eye on the things you want to buy, so you can wait for a
good price instead of buying them now to remember them. The price watch runs on
its own each day.

### `/ntm:run-price-watch`

Checks the things you want to buy, the tasks in the project you picked for them
in setup, and tells you when one is a good deal today. A scheduled job runs it
once a day; run it yourself to check now.

### `/ntm:sync-price-watch-to-amazon`

If you turned on Amazon price alerts, this sets one for each item you're
watching, and removes the alerts for tasks you've closed. Run it in chat, in a
browser signed in to Amazon. The price watch tells you when it's time.
