# The theme builder, reworked

A sketch of the new `/ntm:theme-builder`, to react to line by line. Lines marked
"To decide" wait on a decision, and are listed again at the end. Stage names are
working names.

## What it is for

`/ntm:theme-builder` builds a theme with the user: a world they enjoy,
researched until it holds enough to keep their reminders changing for months.
Today it builds one `%Theme` database and replaces the user's theme. Now a theme
is a set of files named after it, added beside the user's others, never
replacing one.

## The conversation

It keeps today's intro text and asks one question at a time in chat. A user who
already has a theme can start from it: the builder sorts it into the new files.

| Stage           | What the user is asked                        | What gets written                           |
| --------------- | --------------------------------------------- | ------------------------------------------- |
| 1. World        | Their world, where they sit, what hooks them  | The root's `theme` and `world`              |
| 2. Levels       | How it sounds when tasks slip, and get done   | The root's ladders; the default thresholds  |
| 3. Kinds        | The world's kinds of material; which can talk | The options file's pools and roles; `files` |
| 4. Perspectives | Who else would comment on their week          | The options file's `perspectives`           |
| 5. Research     | Which kind first; may ntm use their browser   | One entry file per kind                     |
| 6. Terminology  | Words from the research a writer would miss   | The terminology file                        |
| 7. Try-out      | Whether a few sample messages make them smile | Any fixes to how a level sounds             |
| 8. Switch on    | Whether to use it this week or wait its turn  | The numbers, the history, `%Settings`       |

Stages 4, 6 and 7 can be skipped, and research can stop after one kind. Each
stage saves its part, so each is a place to stop and come back.

## What gets built

| File                      | Written by                                | True before it's used                   |
| ------------------------- | ----------------------------------------- | --------------------------------------- |
| `<Theme>.yaml`, the root  | The skill, with the user                  | Every part there, every level described |
| `<Theme>-<kind>.yaml`     | Research agents, then the review and user | Each line from a page read, or the user |
| `<Theme>-options.yaml`    | The skill; a script adds the numbers      | Passes the schema; matches entry files  |
| `<Theme>-terminology.md`  | Research agents; the user agrees          | Optional                                |
| `<Theme>-message-history` | The skill, from its template              | Exists, empty                           |

The smallest theme that works: a root, an options file, a history and one entry
file of hooks. About 20 hooks, an estimate and not a rule, is more than a week
of messages. Speakers, perspectives, terminology and more kinds come later. The
builder offers this one first.

## The research pass

The skill starts the agents, since an agent can't start others: one per batch of
one kind, about 15 entries as an estimate to tune. Each gets the root's `world`,
the kind's `about` and keys, the entries the theme already has, its part of the
world, and these rules. It writes a scratch file of entries, each line with the
page it came from.

- Every quote and moment comes from a page read in that run.
- Nothing about illness, death, identity or a scandal.
- No song lyrics added by an agent.
- No crawl, no site's API, no changed user agent, nothing submitted.

To decide: today's skill maps the day onto the theme's world (the week as a
season, the morning as a preview, the evening as the main event), and the root
has no place for it now. Either it goes, and time-of-day flavour comes only from
entries whose `when` names a reminder, or the builder still asks for it and
briefs the research with it, so entries are written and tagged for the morning,
the evening or the week.

### Lines judged alone

A reviewer agent, briefed as a devoted fan of the world, reads each line alone,
with no name beside it. A generic line is cut or replaced with a sharper one; a
line that lands only from one person stays with that person. Then the user sees
the kept entries, cuts any or asks for more, and the file is saved.

To decide: whether the user reads every line, or each entry's name and one line.

### The user's browser

Some sites, fan wikis often among them, refuse automated reads. The builder asks
once whether agents may read those pages in the user's browser, a tab each,
clicking only to read. Without it they skip those pages, and the builder says
when a world comes out thinner for it.

## The levels

The builder asks how the theme should sound as a task keeps slipping, and as the
user finishes things, as today's skill does, then names each level in the
theme's words and writes how it sounds. The thresholds are ntm's defaults; the
user sees a number only if they ask, and "push harder sooner" moves one a step.

| Level | `escalation`, reached by   | `finishing_tasks`, reached by                                              |
| ----- | -------------------------- | -------------------------------------------------------------------------- |
| 1st   | Where every message starts | Any finished task                                                          |
| 2nd   | A bump only                | Over 5 closed a day or 10 a week, or a big or hard task; 2.5-day half-life |
| 3rd   | A task slipped 1 day       | Something truly shocking, at most once in 7 days                           |
| 4th   | A task slipped 3 days      |                                                                            |

A bump raises a message one level with no slip behind it, likelier the longer
since the last raised one (3-day half-life), so a good stretch still gets read.

To decide: whether these are every user's defaults.

## Roles and perspectives

Entries that talk, in a manner of their own, can be a speaker; entries with
something to build on (lines, a scene, a moment to call back to) can be a hook.
In `Casebook`, characters are both; scenes and clues are hooks.

A perspective is a group a speaker comes from. The builder asks who else would
comment on the user's week, and looks in the research for groups that comment in
the story: a crowd, staff, an audience, a newspaper, an object that tells it.

| `Casebook` perspective | Members                      | Speaks                  |
| ---------------------- | ---------------------------- | ----------------------- |
| the office             | the detective, the assistant | as one of them, or both |
| the suspects           | none                         | together, as alibis     |
| the morning paper      | none                         | as the day's headline   |

To decide: whether a memberless perspective's sound lives in its own entry file
or beside the speakers.

To decide: whether every speaker must belong to a perspective, or one in none is
still drawn straight from its pool.

## Validation

A script beside the options schema checks the theme before it joins the
rotation, and whenever the builder changes it:

- the options file against the schema
- every entry in the options file is in its entry file, and the reverse
- every file the root lists exists
- the level names in the root and the options file agree
- every perspective's members are speakers

It prints one plain line per problem, naming the file and entry. The builder
fixes what it can, and asks the user only when a fix is a choice. A failing
theme is never added to `%Settings`.

## Saving and switching on

Each stage saves its part as it finishes. At switch on, the builder creates
`<Theme>-message-history` from its template in the user's backend, and runs the
nightly job's script (`docs/nightly-job.md`) to compute the first numbers into
the options file, so the formulas live in one place. Then it adds the root to
All themes, in the Themes part of `%Settings`. The theme is first used on its
turn, or this week, as This week's theme, when the user says so. No other theme
or history is touched; a name already taken gets another.

To decide: whether a new theme goes right after this week's, or at the end.

To decide: whether an unfinished theme waits in the backend, where the user sees
it, or on the computer, which may not survive between chats.

## Coming back

Running the builder on an existing theme grows it: more entries, or a new kind.
Research, review, the check and the script run for the new entries only. A new
entry starts with no score; existing scores stay. The nightly job recomputes a
file's numbers when its checksum changes, so a hand edit is covered too.

To decide: how the user asks to grow one: `/ntm:theme-builder Casebook`, or the
builder asking whether to grow a theme or add one.

## What it costs

Building costs more, once per theme. Upkeep stays cheap: scripts do the math,
and a reminder reads only the root, the picked entry and the options file.

| Build, estimated                    | Agents, estimated    | On a normal subscription, estimated |
| ----------------------------------- | -------------------- | ----------------------------------- |
| The small theme, about 20 hooks     | 2 research, 2 review | One sitting                         |
| A later batch of about 15 entries   | 1 research, 1 review | Part of a sitting                   |
| A large theme, 4 kinds, 180 entries | 12 to 20 of each     | Several sittings over a few days    |

A research agent reads 20 to 40 pages, about a long chat's worth. Every number
here is an estimate, not a requirement; the first real build measures them. The
next run picks up after the last saved stage or batch.

To decide: whether setup builds only the small theme, so its time stays honest.

## The build order

Each PR leaves something to run, updates the README entry, and grows the schema
as it needs.

| PR                   | What a person can run after it                       | Waits on                           |
| -------------------- | ---------------------------------------------------- | ---------------------------------- |
| 1. The theme check   | The check on `Casebook`'s files, passing and failing | Nothing                            |
| 2. The small theme   | A theme from entries the user writes, switched on    | 1                                  |
| 3. The research pass | Research of one kind, reviewed                       | 2                                  |
| 4. The first numbers | Numbers filled in at switch on                       | 2; the script's first slice        |
| 5. The levels        | Thresholds written, level names checked              | 2; the picker's levels slice       |
| 6. The perspectives  | Stage 4                                              | 2; the picker's perspectives slice |
| 7. Coming back       | Growing a theme                                      | 3                                  |

## Open questions

1. Whether the day mapped onto the world goes, or still briefs the research.
2. How much of the research the user reads.
3. Whether the level thresholds are every user's defaults.
4. Where a memberless perspective's sound lives.
5. Whether every speaker must belong to a perspective.
6. Where a new theme goes in the rotation.
7. Where an unfinished theme waits between sittings.
8. How the user asks to grow a theme.
9. Whether setup builds only the small theme.
