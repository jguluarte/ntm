# ntm decisions

What's decided and still shapes the work to come: the 0.4 shape being built, the
patterns every rewritten file follows, and what was declined. What the plugin
already does is recorded by the plugin itself; read the file. The order of work
is in `.claude/plans/0.4-build-plan.md`, and the working rules are in
`CLAUDE.md`. When something changes, edit it here; don't add a dated entry.

## The 0.4 shape

Built on `release-0.4`; main stays installable as 0.3. "The base" is the
published plugin, `ntm`. "The user plugin" is `ntm-user`, which setup generates
and which holds only what's tailored to this user.

### The base

It holds every procedure that is the same for everyone. Its skills are called
directly (`/ntm:today`), and a job's prompt loads `ntm:<skill>`.

### The user plugin

It holds two skills. `backend` teaches how to work with this user's task list:
its calls, labels and statuses, what counts as open, and where every document
lives. `notify` is their channel, with the Pushover keys when they use Pushover.
Linear users also get the Linear connector bundled.

### Skills do their own work

A skill loads `ntm-user:backend` as knowledge, then does the lookup or the write
itself. Only agents are handed work and send something back.

### Generic text lives in the base

The list rules, every backend guide and each feature's rules live in the base as
setup reference files that the build reads. A rule fix reaches users through
`update` and a rebuild. Tokens matter most.

### Runs load only the user's paths

No day-to-day run loads text about a path the user isn't set up for (another
backend, a feature they didn't pick).

### Where values live

The values setup collects live in the `Settings` document on the task list; a
value is defined there, or the backend skill is updated. The persona's Profile
lives in the `Style` document, which `ntm:style` reads.

Labels are built into `ntm-user:backend` and the Pushover keys into
`ntm-user:notify`, so changing one means `update` rebuilds. A job's own app
token goes in that job's prompt.

### Jobs

Jobs are composed from base skills however the user wants. Setup creates them
from the prompt frame and job steps it carries, `/ntm:settings` changes them,
and the scheduled tasks are the source of truth.

The suggested weekly job: `show-completed` for the span just past,
`fix-task-list`, `plan --auto` for the next span, then one message.

### Setup and update

`setup` is the wizard. `update` is tiny: it loads `setup`, which offers what's
new from per-version reference files and rebuilds. Setup's build is the one
rebuild path.

### Versions

The user plugin's `major.minor` mirrors the base's; its patch counts the user's
rebuilds. `ntm-user:backend` opens with a Built line naming the versions,
backend, channel and features.

0.3 installs start fresh. The base and the user plugin update together.

### Publishing

Publishing waits for the test-drives, and needs:

- the base self-test passing with no user plugin installed
- `setup` never sending or creating without being asked
- a privacy page
- a README of 40+ words, LICENSE, icon, author, homepage and repository
- no credentials or brand names

How the published release is identified is open.

## Setup, as a new user meets it

Setup's flow, step by step, is in `.claude/plans/0.4-setup-flow.md` until the
`setup` skill encodes it.

## Patterns every rewritten file follows

From Justin's reviews of #116, #117 and #120. His words there win over this
summary.

### Databases

#### A template per database

Each user database has a template in `references/databases/`: its real shape,
with default or dummy values.

#### Comments are for agents

A `<!-- -->` comment in a template is an instruction to agents, including the
agent another user runs during setup. It says what a part is for and how to keep
it, and it is never written into the user's database.

#### Parts are composable

The user edits, deletes or adds a template's parts.

#### Setup creates every database

Setup creates every database from its template during onboarding.

#### Parts by name

Agents and skills refer to a database's parts by name ("the `morning` message
rule"), never by heading structure.

#### A PR per template

A template lands in its own PR, never in a batch, before setup's rewrite creates
databases from it. It may still change then.

### Configuration is guaranteed

Setup and self-test guarantee the user's configuration. Agents and skills are
written for a configured user and the typical flow: every database, part and
setting they name is there.

### The messenger

- It takes one `type:` input: `freeform` with a `message:` line, or a path into
  the user's Message rules, such as `reminders.morning`, with that rule's facts.
- The user's rule for a type says what the message holds, and may say when no
  notification is needed. The messenger follows it.
- It drafts the core message in plain words first, then puts it in the user's
  style. The tone is its read of today's facts.

### Estimates

- An estimate is an `Estimate: 2 hours` line at the end of the task's
  description, on every backend.
- Estimates are in hours unless the user's Settings say otherwise. Anyone can
  estimate in hours.
- Estimates and times are written in full words, in the user's language:
  `2 hours`, `~20 minutes`.

### Writing

#### Trust the agent

Describe the outcome. An agent that has loaded a skill knows what to do with it,
so steps never read like shell commands piped together.

#### Say what it is where it's introduced

Say what something is, in the section that introduces it.

#### Write for any user

An approval is worded so anyone's simple yes works.

#### Messages have no formula

No formula and no fixed opener; the same shape every day stops getting read.

#### Decided, not settled

Say "decided" or "agreed", never "settled".

#### Sections, not dense lists

A list holds brief items. Anything longer is a named section with whitespace,
never `- **title**: paragraph`.

#### Steps, fields and inputs

Steps are numbered `###` subsections. Fields and values go in a table, a long
list of inputs in a usage block like a man page, and prose never in a code
block.

#### Task list and todo list

Prose says "task list". A description also says "todo list" where a user would
say it, so their words find the skill.

#### Examples in agent descriptions

In an agent's description, each `<example>` has a blank line between its
Context, user, assistant and `<commentary>` parts.

#### Cleanup and delivery in tests

In a test, cleaning up and delivering the result are steps; failing either fails
the run.

## Declined

Justin said no to each of these. Don't propose them again.

### Plugin shape

- `userConfig`, hidden skills (`user-invocable: false`) and any path that works
  only in Claude Code. The plugin targets Cowork and chat.
- A skill or a plugin per backend. Backend guides are reference files.
- Entry skills, an alias plugin, and setup asking what to call ntm. The README
  says "fork and rename with your agent".
- A skill per job.
- Skills worded as requests to another skill and its replies.

### Settings and jobs

- Schedules kept in Settings, or anything comparing the jobs against Settings.
- A catch-all section in Settings for whatever the user does differently.

### Persona

- Shipped personas, Justin's own included.
- A tone ladder defined by the plugin.

### Estimates

- A backend's estimate field, story points, or a mapping onto points, unless the
  user asks.
- Explaining ways to estimate.

### Planning

Special planning rules for parents or deadlines. Parents and sub-tasks are the
backend's task hierarchy, and their words stay.

### Edge cases

- Guards for a missing database, part or setting.
- Reviews that hunt for edge cases.
- Fixing date-math edges in report spans ("last month" on the 1st).

### Price watch

An Amazon alert steps database.

## Test-drive findings

Not handled by the plugin yet.

- An imported persona may carry its own history instructions and double-write
  the message history database. Watch real runs.
- Installing through Chrome: `file_upload` rejects `/mnt/user-data/outputs/`; a
  path under the working directory works.

## Justin's installed copy

ntm 0.3.2, rebuilt 2026-11-08, with five jobs on Opus. Touch none of it unasked.

For his fresh 0.4 setup: the weekly planning plans weekdays; the morning plans
today if it's empty and not paused. Both aim for an hour or less where they can,
without ruling out bigger tasks; a bigger task is the signal to break it up.
