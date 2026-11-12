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

The theme lives in the `%Theme` database, in the parts
`skills/setup/references/theme.md` describes.

### Jobs

Jobs are composed from base skills however the user wants. Setup creates them
last, in its Create the jobs step, after the install and `self-test`, and the
scheduled tasks are the source of truth. Re-running `/ntm:setup` creates any
that aren't scheduled.

Every job starts with `/ntm:ready-check`.

### Setup

`setup` is the wizard, and the only place the user plugin gets built. Run again
for a user who is set up, it creates only their missing jobs, or says to change
things by telling ntm or editing `%Settings`, and stops. `update` is deferred,
below.

### Versions

Each time the user plugin is built, its version mirrors the installed `ntm`'s
exactly, `major.minor.patch`. `ntm-user:backend` opens with a Built line naming
its version, the `ntm` version it was built from, and the date.

0.3 installs start fresh. The base and the user plugin update together.

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

Reminders vary more. Today the frame repeats: "darling" is in 9 of 16 lines, and
11 of 16 open the same way.

### The shape

In Justin's words: "the message history should probably support whatever theme
components are needed ... that way it can have whatever context is needed for
any kind of theme". The theme says what each history entry records, and
`ntm:style` writes and reads that record.

### The work

- `%Message-history` holds the record the theme describes.
- The theme guide, `skills/setup/references/theme.md`, gets spots for a cast of
  speakers, motif groups, ways to play each motif, builds (how a line is put
  together) and per-part rests.
- `ntm:style` rests from the records, rolls its picks in the shell, keeps a
  day's episode, and builds the joke from the task.
- Justin's `%Theme` is redone with him in chat after the guide lands.

### Held back

Writing three drafts per message.

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

`%Theme` has no template; setup builds it from the parts in
`skills/setup/references/theme.md`.

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

### The update skill

`update` waits until ntm is shared with other people. Until then, a change to
someone's setup is a fresh setup or an edit to `%Settings`.

When he shares, it may become "any new features I might want?": it compares the
user's setup to the base plugin, finds what's new, and sets that up in their
backend, since everything that changes lives there.

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

How long does one read of a `%Settings` section, and of `%Theme`, take from a
job on Linear? If the `%Theme` read costs too much, the build copies the theme
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
