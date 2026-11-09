# The morning's facts

The morning's facts are one `today:` line per open task, or `today: none`.

The morning job runs `/ntm:plan --auto day` just before this. Plan moves each
carried-over task to today, so after it only plan's own lines still say which
date a task had. When plan returned `today:` lines, or `today: none`, earlier in
this run, those lines are the facts, as they came: don't ask `ntm-user:backend`
for today's open items. Leave plan's `kept:` and `couldn't move:` lines out of
the facts.

When plan returned `paused`, today is paused: get the facts as the skill says,
and skip the pause read. Run without plan, get them as the skill says.
