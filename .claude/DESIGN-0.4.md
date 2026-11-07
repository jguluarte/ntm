# ntm 0.4: the base builds the user plugin, and the user plugin is the way in

> **Out of date (2026-11-07).** Kept as raw material, not a plan. Since this was
> written: the 0.3 patch work it bundled shipped as small PRs (#3–#16); the
> generator is to be a guide the user's agent follows, not templates (main
> already does this for ntm-user, #16); the `$` rule is only for configured
> label names; there is no Claude Docs guide; the planner agent is merged into
> `ntm:plan` and an estimator agent exists; agents can't start agents. Talk 0.4
> through with Justin before authoring anything.

The theme: a scheduled run loads only what this user uses, and a user who wants
something different changes it in their own plugin. The published base holds the
default patterns, the contracts and the generator; it builds and maintains the
user's plugin. Every way in, a job or a command the user types, starts in the
user's plugin.

Standards: `/domain-first-design` (Justin's skill). Models: Opus 5.5 on high
authors; Opus 5.5 at the top effort setting reviews (architect, naming critic);
the comprehension reader stays generic; Fable reviews this page before authoring
and does the final comprehension pass. A review round that surfaces a design
question stops and brings it to Justin; it does not decide on Opus.

## The plugins

| Plugin | Name                                      | What it is                                         | What it holds                                                                                                                                             |
| ------ | ----------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| base   | `neurodivergent-task-manager` (published) | the default patterns, the contracts, the generator | rules (`conventions`), the agents, every skill's default procedure, every channel and backend guide, the templates, `configure`, the base self-test       |
| user   | `ntm` (fixed, generated)                  | this user's way in                                 | the contract skills (`settings`, `style`, `notify`, `todo-list`, `ready-check`, `self-test`) and an entry point for every job and every command they type |
| alias  | the user's word (optional)                | a name of their own                                | one forward per entry point: `/foo:today` loads `ntm:today`                                                                                               |

The base's long name is the published one (Justin, 2026-11-06): commands
autofill, so its length costs nothing, and it reads clearly in the directory's
review. People type the short one, `ntm`, which is theirs.

The dependency runs one way at each level. The alias calls `ntm`'s entry points;
`ntm`'s entry points call the base. The base calls back into `ntm` only through
the contracts below, by their fixed names, never anything else in it, so the
base depends on the contracts, not on any one user's plugin.

`ntm` keeps its fixed name so the base can always reach the contracts. A user
who wants their own word gets an alias plugin on top. The plugin's own name is
the word; there is no setting for it (Justin, 2026-11-06). `configure` builds it
when asked, and the generator rebuilds an installed one, found by its forwards,
under the same name. The alias only replaces the prefix; every skill keeps its
name (`/foo:today` is `/ntm:today`). Renaming or adding a skill is the user's
own edit: the generator carries over, unchanged, anything in either plugin it
doesn't generate.

## Entry points

Every job and every command a person types is a skill in `ntm`. By default it is
one line of body:

Load `neurodivergent-task-manager:today` and follow it with the words this skill
was called with.

Its description is the base skill's, so either answers the same phrase. A user
who wants to deviate replaces that line with their own version, or adds steps
before or after it, in their own plugin; nothing in the base changes, and it
just works. The alias plugin's forwards are the same one line, pointing at
`ntm`'s entry point.

An entry point changes only what starts there: the base's skills call each
other, not the entry points, so a changed `ntm:today` changes what `/ntm:today`
shows, not what the morning reminder lists. To change a reminder, change its own
entry point, or write the rule under Deviations in settings, which every base
skill reads.

The generator writes an entry point only when the installed one is missing or
its body is still the default line; one the user changed is kept whole, and the
generator lists it. Every `configure` run that changes settings or style, or
finds an older `ntm`, goes through the generator, so a changed entry point
survives upgrades and settings changes alike; a schedule change packages
nothing. A changed entry point is, with settings and style, the only thing in
`ntm` the generator can't rebuild; the generator reads the installed plugin's
`skills/*/SKILL.md` (found with `find ~/.claude/plugins -path '*/ntm/*'`) to
tell a default from a changed one (default: the body below the frontmatter is
exactly the default line). The frontmatter is always regenerated.

Which skills get entry points: the list in
`configure/references/user-plugin/entry-points.md`, one line per entry point:
the name, or `<name> → <base skill>` when the base skill's name differs
(`setup → configure`, `update → configure`). Each is written from
`configure/references/user-plugin/skills/entry-point/SKILL.template.md` with the
base skill's description and the default line. The list is every job and every
skill a person types, setup included (`configure`, `configure-*`, `help`), even
when the entry point only forwards to the base: a user who named their alias
`foo` reruns setup with `/foo:configure` and never has to remember the base's
name (Justin, 2026-11-06). `setup` and `update` are two more entry points for
`configure`. `/neurodivergent-task-manager:configure` is only for the first run,
before `ntm` exists. A base skill whose name is a contract's (`notify`,
`self-test`) gets no entry point: `/ntm:notify` and `/ntm:self-test` are the
contracts themselves.

Jobs' prompts load `ntm:<reminder>` (or the alias); `configure-schedule` writes
them that way, and their fallback line says to check that `ntm` and
`neurodivergent-task-manager` are both installed and enabled.

## Contracts

The base calls these in `ntm`, by their fixed names, once it is set up. How the
user's version does it is theirs.

| Contract      | The one question                                                                                                                                    | How the base calls it                                                                                                                                                                |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `settings`    | What are this user's values? The source of every value; the other contracts are derived from it. Only `ntm` has settings; the base has none.        | loaded by name; read by heading and key                                                                                                                                              |
| `style`       | How do reminders talk to this user?                                                                                                                 | `/ntm:style [--stay-fresh] [--for <reminder>] ["<tone>"] <message>` → message, then `Title: …`                                                                                       |
| `notify`      | How does a message reach this user's phone, on their one channel?                                                                                   | `/ntm:notify --from "<job>" --title "<t>" --message "<m>"` → `Sent: <t>`; on `claude-push`, the delivery block (`NOTIFY VIA FINAL REPLY`, title, message); or `Notify FAILED: <why>` |
| `todo-list`   | How is each operation done on this user's backend?                                                                                                  | loaded by `conventions` in place of `references/<backend>.md`; read by operation heading                                                                                             |
| `ready-check` | Is this user's setup ready for a run: settings load, their backend's connector is here, their list answers? Only `ntm` has it (Justin, 2026-11-06). | `/ntm:ready-check [--notify-failure "<job>"]` → `Ready-check OK` or `Ready-check FAILED: …`                                                                                          |
| `self-test`   | Does the whole loop work for this user?                                                                                                             | `/ntm:self-test` → `Self-test OK`                                                                                                                                                    |

`settings` is the source of every value. `notify`, `todo-list`, `ready-check`
and `self-test` are derived from it and the base templates and are never the
only copy of anything: the generator can always rebuild them from settings
alone. The text above `## About you` in settings carries `Version:`; the
generator writes it.

`ready-check`, generated: the 0.3.2 check with the backend's `ping`, the tool it
uses and List name written in; its failures lose Not configured (settings live
in the same plugin), and Dependency missing names
`neurodivergent-task-manager:conventions`.

The `settings` template's description says to change values with
`/ntm:configure`.

`todo-list`, generated: for `linear` and `claude-docs` it is one line, "The
guide is `references/linear.md` under `neurodivergent-task-manager:conventions`;
follow it." For an own backend it is the description from Todo list in settings,
shaped under the guide's operation headings.

## Nouns and the one question each answers

All in the base; `ntm` holds only contracts and entry points.

| Noun                                         | The one question                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Ideal call site                                                                                            |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `configure`                                  | What does this user want? With no `ntm`, every part; with an `ntm` from an older version, what the version files say to ask (see Upgrading); otherwise one part, or a single value ("change my timezone"). Every answer that changes settings or style ends at the generator. Showing and changing settings is here; there is no base `settings`, and no separate `update` (Justin, 2026-11-06: setup and update differ only in whether there is a plugin to carry forward). | `/ntm:configure`, `/ntm:setup` or `/ntm:update`; `/neurodivergent-task-manager:configure` on the first run |
| `configure/references/generator.md`          | What does `ntm` look like, built from this user's settings and style? Writes the contracts, the entry points (by the keep rule above), the README, `plugin.json`, the alias plugin, from the templates in `configure/references/user-plugin/`.                                                                                                                                                                                                                               | loaded by `configure` at its last step, and by a `configure-*` skill run on its own                        |
| `notify`                                     | Which channels exist and how is each one done? Run by `configure-notifications` for its test push with explicit keys; read by the generator. Without `--app-token` and `--user-key` it says "use `/ntm:notify`" and stops.                                                                                                                                                                                                                                                   | `/neurodivergent-task-manager:notify --app-token … --user-key … --title … --message …` during setup        |
| `conventions`                                | What are the rules of the todo list? It reads `ntm:settings` by key and loads `ntm:todo-list` for the operations. `configure-todo-list`'s first run, with no `ntm` yet, reads `references/<backend>.md` from the base.                                                                                                                                                                                                                                                       | loaded by name before any list operation                                                                   |
| `configure/references/versions/<version>.md` | What does a user plugin of this version look like, and how does each of its files become the next version's? Named for the version it describes: `0.4.md` is what a 0.4 install holds and how it becomes 0.5. One file per version, starting with 0.4; emptied at 1.0.                                                                                                                                                                                                       | read by `configure` from the user's version to current                                                     |
| `self-test`                                  | Is the base intact, and does the installed `ntm` fit it? See Self-tests.                                                                                                                                                                                                                                                                                                                                                                                                     | `/neurodivergent-task-manager:self-test`                                                                   |

What stays unchanged in shape: `conventions` (rules), `plan`, `today`,
`show-completed`, `fix-todo-list`, `pause`, the four reminders, `price-watch`,
`sync-price-watch-to-amazon`, the agents, `configure-*`, `help`. Gone from the
base: `settings` (into `configure` and the `ntm` contract) and `ready-check` (an
`ntm` contract). The base README says once that commands are typed as
`/ntm:<skill>` (or the alias) once `ntm` is installed.

## `notify`, generated

The generator writes the chosen channel's `##` section of the base `notify` with
the keys in place of `<app token>` and `<user key>`, the per-job token lines as
a table, and the Notifications free text (quiet hours, priorities) under a
heading of its own; the `--app-token`/`--user-key` override is left out. It
never loads settings. The frontmatter and Usage come from
`configure/references/user-plugin/skills/notify/SKILL.template.md`. The trigger
phrases in the base `notify`'s description ("notify me", "ping me") move to
`ntm:notify`'s, so a chat request lands on one skill.

Every call site moves to `ntm:notify`: the messenger,
`ready-check --notify-failure`, the reminders' error handling, conventions'
Results, the README's "No skill but `ntm:notify` sends anything", the self-test.

## Self-tests

- `ntm:self-test` is the 0.3.2 self-test with four things written in by the
  generator: the real `no-autoschedule` label name (Labels), the done and
  canceled status names (Todo list), and the channel (Notifications), so its
  notify step has one branch. Everything else is base skill calls, unchanged. It
  sends one real push and makes one throwaway ticket, so it runs only when the
  user asks.
- The base `self-test` passes when every file the generator copies exists under
  `configure/references/user-plugin/`, each `SKILL.template.md` opens with
  frontmatter carrying `name:` and `description:`, and `plugin.template.json`
  parses. With no `ntm` installed it says "no user plugin yet; run
  `/neurodivergent-task-manager:configure`" and succeeds; publishing needs that.
  With one installed it also checks `Version:`, that each contract loads, and
  that `style`, `notify`, `ready-check` and `self-test` carry the Usage above,
  then offers `/ntm:self-test` for the loop.
- Both keep the name `self-test` (Justin, 2026-11-06).

## The audit: what varies by user

Done during the authoring, by the rule "would two users with different settings
read different text here on a run?":

- channel procedure → `notify` contract (yes)
- backend guide → `todo-list` contract (yes)
- whether this setup is ready → `ready-check` contract (yes)
- style → already a contract
- settings → already a contract
- reminders, planner, messenger → no: default patterns in the base, reached
  through entry points
- shopper → no, reads Shopping by key
- conventions → no, but it loads the user's guide instead of its own

Anything the audit adds becomes a contract, in the generator's output list.

## Upgrading (part of `configure`)

When `configure` finds an installed `ntm` older than the base:

1. Load `ntm:settings`; read `Version:`, the version whose templates generated
   the plugin, and compare it with the base's, the `Version:` line in
   `conventions`. The plugin's own `plugin.json` keeps its `1.<date>.<hhmm>`
   build number; that's a different thing.
2. Read `references/versions/` from that version to the current one; each file
   says how each of that version's files becomes the next: what to carry, what
   to generate, what to ask.
3. Carry every section of settings and all of style verbatim, unless a version
   file says otherwise; the text above `## About you` comes from the current
   template, which carries `Version:`. Run the generator for the rest.
4. Entry points: the generator's keep rule; its list of kept entry points goes
   in the result, so the user can check them against the new base.
5. Package `ntm` (and the alias plugin when one is installed; the generator
   finds it by its forwards) and hand them over to install.
6. Offer `/ntm:self-test`. Never run it unasked: it sends a push and writes a
   ticket.

The base and the user plugin update together; nothing is designed for the moment
in between (Justin, 2026-11-06).

## Terms of art: `$` names

Justin's proposal (2026-11-06): a word whose meaning the plugin defines, or
whose value comes from settings, is written with a `$`: $ticket, $todo-list,
$project; $has-amazon-alert, $no-autoschedule, $price-watch. The bare word keeps
its general meaning, so a model reads it close to right even cold, and the `$`
tells models and people alike that it is defined somewhere. One rule: a $name is
a key in `ntm:settings` (its value is the real name on the user's list), or else
a term in the conventions' Vocabulary.

- What the `$` says (Justin, 2026-11-06): "this is a concept, and what it is
  varies with the user's setup". $ticket is a ticket-like thing, whatever the
  user's backend calls it; $has-amazon-alert is a label, whatever the user named
  it. `$PUSHOVER_TOKEN` in a command is the one specific value. Revised the same
  evening (Justin): no Vocabulary word takes a `$`. The `$` marks only values
  the user configures, written by their default name: in practice the labels
  ($no-autoschedule, $pending-shipment, $price-watch, $has-amazon-alert,
  $amazon-unavailable). Overloaded words are rewritten instead of marked: the
  plugin's word for an item is "task" (not "ticket"); Vocabulary says once how
  each tracker represents a task (a Linear issue, a reminder, a todo), and
  sub-task, parent task, project and label follow plainly. "Groom" goes; the
  process is review (`review-todo-list`). The README and anything shown to the
  user stay plain.
- The README states the convention once; `help` explains it when asked, as
  plainly as what the agent knows of the user calls for. Option: an About you
  line for how technical an explanation should be, for users whose agent has few
  memories of them.
- Nothing the user reads in a reminder or a reply carries a `$`; agents
  translate.
- $names are bare, lower-kebab, never in backticks. Shell variables are
  upper-case and stay inside the command's backticks. Bare means the plugin's
  own; backticked means the command's.
- Plugin and skill names are fixed and never take a `$`.
- Every backticked label and status name in 0.3.2 (`no-autoschedule`) becoming
  $no-autoschedule is a rename commit of its own.

## Publishing checklist (after Justin's and the friend's tests; not now)

- base self-test succeeds with no `ntm` installed
- `configure` never sends or creates without being asked
- icon; privacy page (keys, Pushover, Linear); name check for
  `neurodivergent-task-manager`
- `Template source:` in `conventions` points at a release
- `references/versions/` emptied at 1.0

## Order of work

1. 0.4 on branch `v0.4`, PR targeting `main`. Done: the names commit (the base
   is `neurodivergent-task-manager`, the user plugin `ntm`, the plugin-folder
   lookups follow) and the title fix. Next, mechanical: the templates move under
   `configure`, `ready-check` becomes a template; then `$` names. Then one
   commit per noun (`notify` with its call sites; the generator with the keep
   rule; entry points; `configure` absorbing settings and upgrades; self-tests).
   Opus rounds; Fable's final comprehension pass only when Justin says so. No
   migration from 0.3: it's a work in progress, and installs start fresh
   (Justin, 2026-11-06).
2. A markdown linter (line length 80) in its own PR. The `/domain-first-design`
   revision and Justin's design agents are parked (GULU-314).
