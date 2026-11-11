# Estimator log

<!--
How estimating works with this user. The estimator agent keeps it. Setup creates
this database from this template, with every part empty. The user can edit,
delete or add any part. These comments are for agents, and are never written
into the user's database.
-->

## How you work

<!--
What the estimator has learned about how the user works. Short bullets, written
to the user, under the part they belong to. They come from what the user
changes, pushes back on or says. Related bullets fold together, and a change
rewrites a bullet rather than adding one.
-->

### Estimating

<!-- How the user sizes a task. -->

### Writing and breaking up tasks

<!-- How the user likes tasks written, and when and how a task gets split. -->

### Reviews

<!-- How the user likes a review to go. -->

### What you keep correcting

<!-- What the user keeps changing, so it isn't proposed again. -->

## Estimates

<!--
One JSON line per decided estimate, newest first: the date the user decided it,
the task's id, the estimator's last guess, the estimate the user decided, and a
few words on why it changed or why the guess was right. `guess` and `final` are
written as they go after `Estimate:`, such as `2 hours`. Keep the newest 150.
A line looks like
{"date":"2026-11-09","id":"ABC-12","guess":"2 hours","final":"3 hours","why":"wiring was slow"}
-->

```jsonl

```
