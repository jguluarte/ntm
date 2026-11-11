# Estimator log

<!--
How estimating works with this user. The estimator agent keeps it: it reads the
log whenever it estimates, and writes to it when the user decides an estimate,
so its guesses come closer to the user's own, review after review. Setup creates
this database from this template, with every part empty. The user can edit,
delete or add any part. These comments are for agents, and are never written
into the user's database.
-->

## How you work

<!--
What the estimator has learned about how the user works, so it proposes what
they would. Short bullets, written to the user, under the part they belong to.
They come from what the user changes, pushes back on or says. Related bullets
fold together, and a change rewrites a bullet rather than adding one.
-->

### Estimating

<!-- How the user sizes a task, and which kinds of task the guesses miss. -->

### Writing and breaking up tasks

<!-- How the user likes tasks written, and when and how a task gets split. -->

### Reviews

<!-- How the user likes a review to go. -->

### What you keep correcting

<!-- What the user keeps changing, so it isn't proposed again. -->

## Estimates

<!--
One row per decided estimate, newest first: the date the user decided it, the
task's id, the estimator's last guess, the estimate the user decided, and a few
words on why it changed or why the guess was right. Guess and Decided are
written as they go after `Estimate:`, such as `2 hours`. Keep the newest 150.
-->

| Date | Task | Guess | Decided | Why |
| ---- | ---- | ----- | ------- | --- |
