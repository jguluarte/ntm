# Terminology

## Core

### Backend

The system behind the task list.

### Database

A document stored in the backend that ntm keeps persistent data in, written by
its default title with a `%` in front, such as `%Settings`. The titles are under
Databases in these rules, `ntm-user:backend` says where each one lives, and
ntm's `references/databases/` holds the templates.

### Guide

How each operation is done on this backend: the calls `ntm-user:backend` gives.

### Job

A scheduled run, what the Claude app calls a scheduled task. Never "trigger",
"routine" or "cron job" when talking to the user.

### Label

A tag on a task or project.

### Planned date

The task's one date field, the day the work is planned for. **A planned date
should NEVER be treated like a "deadline"**.

### Project

A collection of tasks. Projects can have labels which also apply to its tasks.

### Task

One thing on the todo list, shown the backend's own way. Its id is whatever the
backend gives it, such as `ABC-12`.

### Task list

The place that holds every task, named in `ntm-user:backend`.

## Task management

### Estimate

How big a task is; the estimator agent (`agents/estimator.md`) says what it
means.

### Pause

A day or range when nothing gets planned automatically. Work the user dated
themselves still gets its reminders. Kept in `%Paused-dates`.

### Planner

A skill that picks tasks and sets their planned dates, such as `ntm:plan`.

### Started

A plannable status that means work has begun (see Status classes). Jobs give
credit for it.
