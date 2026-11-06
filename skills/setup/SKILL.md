---
name: setup
description: One-time onboarding for the nudge plugin, in chat. Interviews the user about their tracker, notifications, price watch and rhythm, designs their messenger with nudge:messenger, hands them a personalized copy of the plugin and creates their scheduled tasks; for someone who already runs an earlier, skills-based version of this system (account skills plus scheduled tasks), takes the values from those instead of asking. Run when the user says "set up nudge", "run nudge setup", "import my nudge system", or installs the plugin for the first time.
---

# nudge:setup

Turns the template plugin into the user's own copy. Everything happens in chat, in short rounds: you bring proposals, they react. Never hand them a form.

Read `references/placeholders.md` once before starting; it lists every placeholder, which phase settles it, and its default.

## Before you start

1. Find the installed plugin: `find /mnt/.local-plugins /mnt/.plugins ~/.claude/plugins/synced -type d -name "*nudge*" 2>/dev/null`. Copy it to a working folder (`/tmp/nudge-setup/nudge`); you edit the copy, never the install.
2. Check for scheduling tools with ToolSearch (`select:mcp__claude-code-remote__list_triggers,mcp__claude-code-remote__create_trigger`). If they're missing, setup still produces the copy; say up front that the scheduled tasks will have to be created later from a session that has them.
3. If the copy's `config.md` has no `~~` placeholders left, this plugin is already set up. Ask what they want to change and go to the phase that owns it. On a copy that's already set up, phase 6 edits the changed values in place (the config.md row, the credentials in `nudge:notify`'s curl, the job templates' title lines) instead of replacing placeholders, and phase 7 re-syncs the jobs with `nudge:jobs` when a job's time, the timezone or the name changed.
4. Ask whether they already run an earlier, skills-based version of this system (account skills plus scheduled tasks). If yes, follow Import below; the phases are the same, but their values come from what they have.

Never load the installed template's `nudge:board` to do work: its config is unfilled, and it would stop. Everything below works from the settled values and the files in the copy.

Keep a running list of the values you've settled. Write them into the copy in phase 6, not as you go, so a change of mind costs nothing.

## Import

For someone moving an existing system, not starting one. Each phase takes its values from what they have; ask only where a value is missing. Their skills and scheduled tasks are read, never changed, and nothing of theirs is renamed or moved beyond the two moves below.

Ask them to paste the skill that holds the board rules, the skill that rewrites messages in a voice, the skill that sends notifications, and the skills that keep days off and grooming (each names the document it keeps), or, in a cloud session, read the installed account skills from `~/.claude/skills/synced`. The stores note's title is in the price-watch task's prompt, if they have one, from `list_triggers`. Then:

- **Phase 1:** `tracker`, `board name`, `board id` and `ticket prefix` from the skill that holds the board rules; the status names and label names as it names them. The labels exist already; create none. Each note key records the title of the document that holds that thing today (`days off note` the document their days off live in, `voice history note` their voice's history, and so on): their existing documents keep their titles; the config points at them. A note they don't have yet keeps its default name. Two moves it must name: an earlier version kept the Amazon alert flow in a ticket comment and headed the days-off list `## Blackout dates`; copy the first into the `amazon alert flow note` with `write note` and rename the second to `## Days off`.
- **Phase 2:** `channel` and, for Pushover, the credentials from the skill that sends notifications.
- **Phase 3:** `price watch on` is `yes` when they have a price-watch project; `price watch project` is its name and `stores note` the title of their store list, from the price-watch task's prompt. Nothing is created.
- **Phase 4:** `timezone` and `your name` from the skill that holds the board rules; `voice on` is `yes` when they have a skill that rewrites messages in a voice. The jobs from `list_triggers`: match each of their scheduled tasks to a job by purpose (morning plan, afternoon nudge, evening check-in, weekly recap and plan, daily price watch) and keep its time and days.
- **Phase 5:** run `nudge:messenger --import` with the text of the skill that rewrites messages in a voice and the job prompts matched in phase 4 (the job prompts say what the day count does). It builds the profile from them, without the interview, and writes it to the settled `messenger note`.
- **Phases 6 and 7** as written.

In the Ending, add which of their old scheduled tasks (the ones matched in phase 4) to turn off once each new job has run once, so the two don't both send for the same beat: `update_trigger` with `enabled: false`, not delete, so their history stays. List the two moves made (the Amazon alert flow copied into its note, the days-off heading renamed) and that the job prompts fed the messenger's escalation policy.

## 1. The tracker

Ask what they track tasks in today. If they're undecided, offer the three choices in one line: Linear (tested, free for individuals), a Claude Doc that Claude keeps for them (no tracker connector; untested; heavier per run), or another tracker with a drafted adapter. Then:

- **Linear:** the tested path. Confirm the connector is attached (ToolSearch for `mcp__Linear__list_teams`; if absent, ask them to connect Linear and come back). Call `list_teams`, propose the team, and record `board name`, `board id` and `ticket prefix`; `tracker` is `linear`. Call `list_issue_statuses` for it and map the status classes: propose the mapping from the names you see (a backlog, a to-do and an in-progress status as plannable; which one is started; done, canceled, duplicate). If the board has a blocked status, record it; if not, record `blocked status` as blank and say the pending-shipment label and blocked-by links cover the same ground.
- **A Claude Doc:** the board is one Claude Doc that Claude reads and edits itself, through the adapter `references/adapters/claude-docs.md` in the copy. Say what it costs: no tracker connector to set up, but every run reads the whole table and edits it row by row, so it's heavier per run and untested; fine for a few dozen tickets. Confirm the Claude Docs connector is attached (`mcp__Claude_Docs__batch` and `update` are listed when it is; load `read` with ToolSearch). Record `tracker` as `claude-docs`, `board name` as the doc's title (propose one), and `ticket prefix` as whatever they want on their ids. Statuses and labels are the config's own names: record the defaults (or their renames) and skip the status mapping above and the label creation below. A doc can't be found by title, so `board id` is the doc's id: if they already have a board doc, take it from the link they paste (the trailing part of `https://claude.ai/artifact/<id>`); otherwise, after the labels and notes below are settled, create the doc with the adapter's `create board` (it makes the Status enum, both tables and a Notes tab with a section per note) and record the id it mints. Then run `/nudge:adapter claude-docs --test`; a pass flips the adapter's mark.
- **Another tracker:** run `nudge:adapter` with the tracker's name. It confirms the connector, drafts `references/adapters/<tracker>.md` in the copy from `CONTRACT.md`, smoke-tests it against their board, and hands back `tracker` (the file's stem, without `.md`), `board name`, `board id` and `ticket prefix`. Where the tracker has no documents, the adapter keeps notes in pinned tickets, as the contract describes; say so. The rest of this phase then goes through that adapter's Setup operations.

Then the board's labels and notes. Show the defaults from `config.md`'s Labels and Notes sections in one table; most people keep them. Record any rename. Call the adapter's `list labels` and, for each system label the board lacks, create it now with `create label` under its settled name, with the one-line meaning from `config.md` as its description. Notes need nothing now; each is created the first time something writes it (the stores note, in phase 3).

## 2. Notifications

Two channels:

- **Pushover:** a push to their phone from inside the run. Needs their Pushover application token and user key, which will be written into their copy of the plugin. Say plainly: the copy must then stay private. This is the reliable channel.
- **Claude push:** the scheduled task's own completion push carries the message. Needs nothing, but it's best-effort: it fires when a run finishes with something noteworthy, not on every run, and chat requests to "ping me" can't use it.

Record `channel` and, for Pushover, the two credentials. Don't echo credentials back in chat after they give them.

## 3. Price watch

Ask whether they want the daily price watch. If no: `price watch on` = `no`, and the price-watch job isn't created.

If yes: `country and currency`, and which project holds purchases waiting on a good price (`price watch project`). Offer to create the project now with the adapter's `create project`, with the labels it should carry: the settled `price-watch label` and `no-autoschedule label`. If the project exists already, make sure it carries both.

Then create the stores note in that project with the adapter's `write note` (with the project), under the `stores note` name settled in phase 1, with the headings `## Seed`, `## Vouched`, `## Blocked`. Ask for a few seed stores by category to put under Seed, with their domains, or leave Seed empty; Vouched and Blocked start empty.

## 4. Rhythm

Ask for their timezone (IANA name; confirm the city if they give one), what to call them (`your name`; job titles use it), and whether reminders come from a messenger they design or arrive as the jobs write them (`voice on`; the messenger is designed in phase 5).

Then propose the jobs. The defaults are in each template's header under `skills/jobs/references/jobs/` (job name, time, days): Morning plan, Afternoon nudge, Evening check-in, Weekly recap and plan, and Daily price watch when price watch is on. Show them as one short table from the headers and let them strike or move any. Days is theirs to set, weekdays or every day; planning itself is weekday-based: `/nudge:plan --weekly` plans Monday to Friday, and a morning job that runs on a weekend plans that day with `--daily`.

`nudge:jobs` applies the jitter rule when it creates them, so the round defaults, and any round time they pick, get moved a few minutes earlier; say so.

## 5. The messenger

Skip when `voice on` is `no`.

Run `nudge:messenger`. It writes the messenger profile with them (voice, what gets them to read, what happens when something keeps slipping, motifs, examples) and saves it as a note on the board, so it needs the tracker, not the copy. Give it the settled `board name`, `board id`, `ticket prefix` and `messenger note`, and point it at the adapter file in the copy (`/tmp/nudge-setup/nudge/skills/board/references/adapters/<tracker>.md`, which has no placeholders) for the write. Its result line `Messenger saved: <name>` carries the name: record it as `messenger name`, or `voice on` = `no` if they chose to have no messenger after all.

## 6. The copy

1. Anything not settled takes its default from `references/placeholders.md`. Credentials stay blank unless the channel is Pushover.
2. Replace every placeholder in the copy: `grep -rn '~~\w' /tmp/nudge-setup/nudge` lists them; replace each with its settled value, in every file but `references/placeholders.md` and `CONNECTORS.md`, which stay tables of placeholders. Run the grep again: it must list nothing but `references/placeholders.md` and `CONNECTORS.md`.
3. Package: `cd /tmp/nudge-setup/nudge && zip -r /tmp/nudge.plugin . -x "*.DS_Store"`. Deliver `/tmp/nudge.plugin` with SendUserFile, or, without SendUserFile, copy it to the session's outputs folder.
4. Tell them to install it in place of the template, and that it's private to them.

## 7. The jobs

Load `nudge:jobs` and follow its Creating section for each job kept in phase 4, taking everything from the copy: its filled templates under `skills/jobs/references/jobs/` and the settled values. The tracker connector must be attached to this session; it is, if phase 1 worked.

If scheduling tools weren't available (Before you start, step 2), say which jobs are still to be created and that `nudge:jobs` creates them from any session that has the tools and the tracker connector.

## Ending

Say these first:

1. Until the personalized copy is installed, every run ends with "Not set up".
2. The jobs' approval mode: a run stops at its first write unless the task is on automatic approval, which they can turn on in the task's settings if their organization allows it. (`nudge:jobs` reported which mode each task got.)

Then sum up in a few lines: tracker and board, channel, messenger name, which jobs exist and when they run. The first check, once the copy is installed: fire a job by hand (`mcp__claude-code-remote__fire_trigger`, via ToolSearch) and read its run, or wait for the first one. Offer a first groom once they've installed the copy and opened a new chat: `/nudge:groom`; a short one is fine. No restating the plugin.
