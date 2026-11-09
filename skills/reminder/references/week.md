# The week's facts

The week's facts, in place of today's open tasks, each task written as the
skill's The facts says:

- `weekly message:` the job prompt's `Weekly message:` line; without one, what
  got done, what's still open, and the week ahead.
- `done:` one line per task done in the span, oldest first, or `done: none`.
- `open:` one line per task still open from the span, or `open: none`.
- `planned:` one line per task planned for the week ahead, or `planned: none`.

Find the tasks done in the span. If that fails, write `done: unavailable` and
carry on: the week ahead is still sent.

The week ahead job runs `/ntm:fix-todo-list`, then `/ntm:plan --auto <range>`,
just before this. Fix-todo-list clears the planned date of every open task
planned before today, so after it only its own lines still say which tasks are
open from the span. Each of its `Cleared <id> <title> <url> (was <date>)` lines
is an `open:` line, with its `was` date; `Nothing to fix.` is `open: none`. When
fix-todo-list didn't run or failed, find the open tasks planned in the span,
before today.

Plan's `planned:` lines from earlier in this run are the week ahead, as they
came. Run without plan, find the open tasks planned in the 7 days after today.
