# The theme builder, reworked

A sketch of the new `/ntm:theme-builder`, to react to line by line. Stage names
are working names.

## What it is for

`/ntm:theme-builder` builds a theme with the user: a world they enjoy,
researched until it holds enough to keep their reminders changing for months.
Today it builds one `%Theme` database and replaces the user's theme. Now a theme
is a set of files named after it, added beside the user's others, never
replacing one.

## The example theme

`Casebook`, a made-up detective story, is the example in this sketch, in
`references/theme-files.md` and in ntm's tests. It shows the shape of a theme's
files, and nothing more. The builder never builds `Casebook` or copies from it:
every theme comes from the user's own world and its sources. The skill says so
wherever it shows the example.

## The conversation

It keeps today's intro text and asks one question at a time in chat. A user who
already has a theme can start from it: the builder sorts it into the new files.

| Stage              | What the user is asked                        | What gets written                           |
| ------------------ | --------------------------------------------- | ------------------------------------------- |
| 1. World           | Their world, where they sit, what hooks them  | The root's `theme` and `world`              |
| 2. Levels          | How it sounds when tasks slip, and get done   | `escalation`, `finishing_tasks`; thresholds |
| 3. Kinds           | Kinds found in the sources; which can talk    | The options file's pools and roles; `files` |
| 4. Perspectives    | Who else would comment on their week          | The options file's `perspectives`           |
| 5. Research        | Which kind first                              | The entry files                             |
| 6. Terminology     | Words from the research a writer would miss   | The terminology file                        |
| 7. Sample messages | Whether a few sample messages make them smile | Any fixes to how an escalation level sounds |

Stage 1 also asks how the user's day maps onto their world, if it does at all,
and whether there is anything they don't want in it. The user decides what each
part of the day is or is not. Both answers go in the root's `world`.

Each stage saves its part, so each is a place to stop and come back.

## What gets built

| File                        | Written by                                | True before it's used                   |
| --------------------------- | ----------------------------------------- | --------------------------------------- |
| `<Theme>.yaml`, the root    | The skill, with the user                  | Every part there, every level described |
| `<Theme>-<descriptor>.yaml` | Research agents, then the review and user | Each line from a page read, or the user |
| `<Theme>-options.yaml`      | The skill; a script adds the numbers      | Passes the schema; matches entry files  |
| `<Theme>-terminology.md`    | Research agents; the user agrees          | Optional                                |
| `<Theme>-message-history`   | The skill, from its template              | Exists, empty                           |

The smallest theme that works is a mix: a root, an options file, a history, and
a few entries of each kind the sources suggest. About 20 entries, an estimate
and not a rule, is more than a week of messages. Setup builds this one. Its
research also notes what it found and left for later, such as more kinds,
sources and people. That list is kept in the user's backend beside the theme's
files, and briefs the bigger research when the theme grows.

The builder aims to give every theme, the small one included, entries kept for
`big_win`, so a big win has material of its own. A theme with none still works:
on a big win, the picker falls back to a normal win.

## Kinds

A kind is one sort of material in the world. Each kind has its own pool in the
options file and its own name in an entry file; one entry file can hold several
kinds. No list of kinds is fixed: each theme's kinds come from its source
material.

At stage 3, the builder searches the web for the world's sources: the pages that
hold its people, its scenes and what fans say about it, such as wikis, episode
guides and fan sites. It proposes kinds from what those sources hold, each with
an `about` saying what an entry is and how a message uses one, and the keys its
entries share. The user keeps, renames or drops them.

Most worlds have actors: people who talk in a manner of their own, so a message
can be spoken by one as well as built on them. Two more kinds turn up in many
worlds: recurring scenes a message can be set in, and single moments to call
back to. The sources decide which a theme has.

## The research pass

The skill starts the agents, since an agent can't start others: one per batch of
one kind, about 15 entries as an estimate to tune. Each gets the root's `world`,
the kind's `about` and keys, the sources found at stage 3, the entries the theme
already has, its part of the world, and these rules. It writes its entries, each
line with the page it came from, to a scratch file kept in the user's backend
beside the theme's files, so a later chat can pick up the review.

- Every quote and moment comes from a page read in that run.
- If you need to browse websites, ask to use the user's browser
    - Driving their browser is fine
    - This is investigating key information, not crawling the web

Some sites, fan wikis often among them, refuse automated reads, and the user's
browser reaches them. The builder asks the first time a page needs it, at stage
3 or in the research, and agents use a tab each. Without it they skip those
pages and say so in their report.

The research follows what `world` says to leave out, and how it maps the user's
day: entries that fit one part of the day are tagged with `type` for the
morning, the afternoon, the evening or the week.

When a kind turns up little, the research reports it, and the builder tells the
user what came back thin. A world with little to draw on may not work well for
them; a better defined one holds up longer.

### Lines judged alone

A reviewer agent, briefed as a devoted fan of the world, reads each line alone,
with no name beside it. A generic line is cut or replaced with a sharper one; a
line that lands only from one person stays with that person. Then the user sees
as many of the kept entries as they want, cuts any or asks for more, and the
file is saved.

Ask the user how involved they would like to be with their theme's content. It
is likely fine to make changes over time if they don't want to dedicate time
today.

## The levels

Two parts of the root have levels. `escalation` is how the theme sounds as a
task keeps slipping; `finishing_tasks` is how it marks finished tasks, up to a
big win. The builder asks how each should sound, as today's skill does, then
names each level in the theme's words and writes how it sounds. The table holds
the defaults for both parts, how many levels and when each applies, and a theme
may set its own for either. The user sees a number only if they ask, and "push
harder sooner" moves one a step.

| Level | `escalation`, reached by   | `finishing_tasks`, reached by                                              |
| ----- | -------------------------- | -------------------------------------------------------------------------- |
| 1st   | Where every message starts | Any finished task                                                          |
| 2nd   | A bump only                | Over 5 closed a day or 10 a week, or a big or hard task; 2.5-day half-life |
| 3rd   | A task slipped 1 day       | Something truly shocking, at most once in 7 days                           |
| 4th   | A task slipped 3 days      |                                                                            |

A bump raises a message one level with no slip behind it, likelier the longer
since the last raised one (3-day half-life), so a good stretch still gets read.
The bump is the theme's choice: the builder asks whether the theme ever presses
on a good day. A theme that doesn't has a `bump_rate` of 0, and only slips raise
its level.

## Roles and perspectives

Entries that talk, in a manner of their own, can be a speaker; entries with
something to build on (lines, a scene, a moment to call back to) can be a hook.
In `Casebook`, characters are both; shared lines and scenes are hooks.

A perspective is a group a speaker comes from. The builder asks who else would
comment on the user's week, and looks in the research for groups that comment in
the story: a crowd, staff, an audience, a newspaper, an object that tells it.

| `Casebook` perspective | Members                      | Speaks                  |
| ---------------------- | ---------------------------- | ----------------------- |
| the office             | the detective, the assistant | as one of them, or both |
| the suspects           | none                         | together, as alibis     |
| the morning paper      | none                         | as the day's headline   |

Perspectives are optional. A speaker in no perspective is drawn straight from
its pool. A perspective with no members, such as a narrator, gets its sound from
the root's `world`, which says who tells the story when no one in particular
speaks.

## Validation

The builder checks the theme with the picker, the style skill's script, before
the theme joins the rotation and whenever the builder changes it:

- the options file against its schema, in the picker's `theme.py`
- every entry in the options file is in its entry file, and the reverse
- every file the root lists exists
- the level names in the root and the options file agree
- every perspective's members are speakers

It prints one plain line per problem, naming the file and entry. The builder
fixes what it can, and asks the user only when a fix is a choice. A failing
theme is never added to `%Settings`. The builder's test run of picks uses the
same picker.

A theme that keeps nothing for `big_win` passes; the check says so, and the
builder offers to add some.

## Saving and switching on

Each stage saves its part in the user's backend as it finishes, so an unfinished
theme waits there, and a later chat picks it up instead of starting over. When
the last stage is done, the builder switches the theme on. It creates
`<Theme>-message-history` from its template, and runs the nightly job's script
(`docs/nightly-job.md`) to compute the first numbers into the options file, so
the formulas live in one place. Then it adds the root to the end of All themes,
in the Themes part of `%Settings`, or where the user asks for it. The weekly
job's rotation decides when it is used. No other theme or history is touched; a
name already taken gets another.

## Coming back

The user asks to grow a theme in their own words, such as "increase variety" or
"too much repetition". The builder grows it with more entries, or a new kind,
starting from what the last research left for later. Research, review, the check
and the script run for the new entries only. A new entry starts with no score;
existing scores stay. The nightly job recomputes a file's numbers when its
checksum changes, so a hand edit is covered too.

## What it costs

Building costs more, once per theme. Upkeep stays cheap: scripts do the math,
and a reminder reads only the root, the picked entry and the options file.

| Build, estimated                    | Agents, estimated             | On a normal subscription, estimated |
| ----------------------------------- | ----------------------------- | ----------------------------------- |
| The small theme, about 20 entries   | 1 research, 1 review per kind | One or two sittings                 |
| A later batch of about 15 entries   | 1 research, 1 review          | Part of a sitting                   |
| A large theme, 4 kinds, 180 entries | 12 or more of each            | Several sittings over a few days    |

A research agent reads 20 to 40 pages, about a long chat's worth. Every number
here is an estimate, not a requirement; the first real build measures them. The
next run picks up after the last saved stage or batch.

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
