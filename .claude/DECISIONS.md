# ntm decisions

What's decided and still shapes the work to come: the plugin's shape on main,
the 0.5 work, the patterns every rewritten file follows, what was declined or
deferred, and what's still unknown. What the plugin already does is recorded by
the plugin itself; read the file. The working rules are in `CLAUDE.md`. When
something changes, edit it here; don't add a dated entry.

## The plugin's shape

"The base" is the published plugin, `ntm`. "The user plugin" is `ntm-user`,
which setup generates and which holds only what's tailored to this user.

### The base

It holds every procedure that is the same for everyone. Its skills are called
directly (`/ntm:today`), and a job's prompt loads `ntm:<skill>`.

### The user plugin

It holds two skills. `backend` teaches how to work with this user's task list:
its calls and statuses, what counts as open, and where each database lives.
`notify` is their channel. Linear users also get the Linear connector bundled.

### Skills do their own work

A skill loads `ntm-user:backend` as knowledge, then does the lookup or the write
itself. Only agents are handed work and send something back.

### Generic text lives in the base

The rules live in ntm's `references/rules/`, and runs read them there. The
backend guides and database templates are setup's, in
`skills/setup/references/`. A rule fix reaches users with the next version of
the base. Tokens matter most.

### Plugin files

Skills and agents reach the plugin's files through `${CLAUDE_PLUGIN_ROOT}`
(#198), which expands to the plugin root in skill and agent text, in the CLI and
in Cowork. A file read later keeps the literal.

### Runs load only the user's paths

No day-to-day run loads text about a path the user isn't set up for (another
backend, a feature they didn't pick).

### Where values live

The values setup collects live in the `%Settings` database, label names
included, and skills load them from there. Changing a setting is an edit to
`%Settings`, with no rebuild.

`ntm-user:backend` holds only what has to be built in: how to work with the task
list, and where each database lives, `%Settings` included.

The Pushover keys live in `%Settings`, and changing them needs no rebuild. A
job's own app token goes in that job's prompt.

The theme lives in its theme files, described under 0.5.

### Jobs

Jobs are composed from base skills however the user wants. Setup creates them
last, in its Create the jobs step, after the install and `self-test`, and the
scheduled tasks are the source of truth. Re-running `/ntm:setup` creates any
that aren't scheduled.

Every job starts with `/ntm:ready-check`.

### Setup

`setup` is the wizard, and builds the user plugin. Run again for a user who is
set up, it creates only their missing jobs, or says to change things by telling
ntm or editing `%Settings`, and stops.

### Update

`/ntm:update` brings the user's setup up to the installed `ntm`, with them in
chat. Each version ships an update note in `skills/update/references/`: a
changelog, then instructions for update, including whether the user plugin needs
rebuilding. `%Settings` records the version the setup was last brought up to, as
Last synced under `## ntm version`.

The 0.5.0 note lands last, before release. It offers the theme builder and reads
the user's current theme to pre-fill it.

### Versions

Each time the user plugin is built, its version mirrors the installed `ntm`'s
exactly, `major.minor.patch`. `ntm-user:backend` opens with a Built line naming
its version, the `ntm` version it was built from, and the date.

0.3 installs start fresh. After installing a new `ntm`, the user runs
`/ntm:update`.

### Publishing

Publishing waits for the test-drives, and needs:

- `setup` never sending or creating without being asked
- a privacy page
- an icon, and a homepage and repository in `plugin.json`
- no credentials or brand names

How the published release is identified is open.

## 0.5: the Theme

Built on `release-0.5`.

### The goal

Reminders stay fresh. The research found that the frame converges when one model
call both picks it and writes the line, so 0.5 splits picking from writing.

### Who does what

The job picks. The `writer` agent, which is the messenger renamed, writes
several versions of the message from the picks and today's facts, and never
reads the history. The job chooses among them, and notify delivers, unchanged.

### The deal alert

The price watch's deal alert goes out plain, straight through notify, with no
style and no writer. It gives each deal's store link and no task id. The run's
result in the job's chat carries everything needed to act: the item, task id,
price, store, link, conditions and sale end.

### The pick

The pick is a bandit. Each value has a score, minus a penalty that halves over a
computed half-life since its last use, and a weighted random draw takes one, so
a value's place in its list means nothing.

Each message gets one hook, from the pool of motifs, references and actors'
lines. It names a speaker only sometimes, at a rate computed from the pool.
Messages never address the user.

### Theme files

A theme is a set of YAML files named after it. The root, for Justin
`Dragify.yaml`, is the guide: the world, the reads, the reminders, and what each
other file holds.

The options file, `<theme>-options.yaml`, is the only file the picker reads. It
holds the computed numbers and a checksum of the content they came from.

Other files are added and named as a theme needs them: actors (each actor's
lines, plus lines any actor can say), motifs, references, and terminology, which
holds only the terms a model wouldn't know or would misuse.

Fan reviewers judge lines one at a time. A line that only lands from one person
stays with that person.

### The nightly job

It rates each message by whether the user acted on its tasks: closing one,
moving its date or clearing the day all count. ntm's own date changes are known
from each task's `Planned date history`, and set aside. It then updates the
scores.

It recomputes the half-lives, actor weights and speaker rate only when the
checksum shows the content changed. It also runs just before `ntm:clean` in the
weekly job. Building a theme computes the numbers up front.

### `%Message-history`

One row per message: the date and time, the reminder, the theme, the picks, the
opening words, the task ids with their planned dates at send, the user's
feedback and the rater's verdict.

### Inside ntm

All of this stays inside ntm for the user. When they ask how it works, the core
rules' "Explaining how ntm works" section covers it.

### Later

- An examples pool the user builds from job chats. The writer reads it only once
  it's big enough.
- `/ntm:theme-builder`, a skill that researches a world and builds a theme.

### Justin's theme

It's built on a `dragify` branch, which never merges anywhere and is deleted
once the theme is in Linear.

### Release

`release-0.5` merges into main, and the version is tagged there.

## Patterns every rewritten file follows

From Justin's reviews of #116, #117 and #120. His words there win over this
summary.

### Rewriting a file

1. The rewrite is drafted beside the current file, as `SKILL-new.md`. An agent's
   draft goes in `drafts/`, as `drafts/<name>-new.md`, because every file in
   `agents/` loads as an agent.
2. The owner reviews the draft. Each round of his comments is a new commit.
3. When he approves, the draft's text replaces the current file and the draft
   file goes.
4. A second agent does a comprehension pass: could a person follow this? It is
   never a hunt for edge cases.

### Databases

#### A template per database

Each user database has a template in `skills/setup/references/databases/`: its
real shape, with default or dummy values. Only setup reads a template, to create
the user's database from it. Agents read the user's own database.

A theme's files have no template; they're built with the user.

#### Comments are for agents

A `<!-- -->` comment in a template tells setup how to fill in its part, and it
is never written into the user's database. Each agent or skill that keeps a
database carries its own rules for keeping it.

#### Parts are composable

The user edits, deletes or adds a template's parts.

#### Setup creates every database

Setup creates every database from its template during onboarding.

#### Parts by name

Agents and skills refer to a database's parts by name ("the `morning` message
rule"), never by heading structure.

### Configuration is guaranteed

Setup and self-test guarantee the user's configuration. Agents and skills are
written for a configured user and the typical flow: every database, part and
setting they name is there.

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

- Schedules (job titles or times) kept in `%Settings`.
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

## Deferred

After 0.5, or when the owner raises them.

### A closer look at the Message rules template

The owner asked to be reminded at a calm point.

### Recurring reminders

At an interval (pet care, medicine), where the next date follows from when it
was last done. It comes after 0.5. Justin is first trying it with Linear and his
settings, and it may not need a feature.

### A price watch talk

Its default pattern makes too much busywork, and setup needs better guidelines.

## Unknowns: one experiment each

### The bundled Linear connector

Does it ask for its own sign-in, and does a job created afterwards carry it?

### A job reaches the user plugin

Does a job whose prompt loads `ntm:today` also load `ntm-user:backend` and reach
the messenger agent?

### The cost of reading Settings and the theme

How long does one read of a `%Settings` section, and of a theme file, take from
a job on Linear? If the theme read costs too much, the build copies the theme
into `ntm-user`.

### The size of the backend skill

How big is `ntm-user:backend` for a Linear user with both features, and with
task management only? The plugin's shape is for tokens; this proves it.

### A list in a Claude Doc or an artifact

Does a list built in one work from a job? Until it does, setup offers only what
passed.

### Where the build folder goes

`/tmp` or the working directory?

## Test-drive findings

Not handled by the plugin yet.

- An imported persona may carry its own history instructions and double-write
  the message history database. Watch real runs.
- Installing through Chrome: `file_upload` rejects `/mnt/user-data/outputs/`; a
  path under the working directory works.

## Justin's installed copy

ntm 0.4.0 and ntm-user 0.4.0 in his Cowork, migrated 2026-11-11, with five jobs:
Price watch, Morning, Afternoon and Evening reminders, and Weekly planning.
Touch none of it unasked.
