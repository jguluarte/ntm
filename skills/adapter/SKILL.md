---
name: adapter
description: Drafts an adapter for the user's tracker with them, mapping each operation the board rules name onto the tracker's connector, then verifies it with a smoke test on their real board. Run from nudge:setup, or when the user says "write an adapter for <tracker>", "use <tracker> instead", "test my adapter" or "switch trackers".
---

# nudge:adapter

An adapter is one file per tracker under `skills/board/references/adapters/`, saying which connector calls carry out each operation the board rules name. `CONTRACT.md` in that folder lists what it must cover, under headings every adapter keeps. `linear.md` (tested) and `claude-docs.md` are the examples: copy their shape.

This skill writes that file with the user and tests it. `nudge:setup` runs it in phase 1 for any tracker but Linear and the Claude Doc; on its own it works in a copy of the installed plugin, as setup's Before you start says, never in the install.

## Usage

```
/nudge:adapter <tracker>
/nudge:adapter <tracker> --test
```

`--test` skips Drafting and runs the Smoke test on the adapter the copy already has. If `<tracker>.md` exists already and the user didn't say, offer to test it instead of redrafting.

## Drafting

1. **The connector.** Find the tracker's tools with ToolSearch (`+<tracker>` as the query) and tell the user, in one line, which tools are there. None: ask them to connect the tracker and come back, and stop.
2. **The board.** Ask what holds their tickets (a project, space, list, or the whole account) and pick it with the tracker's list call. Settle `board name`, `board id` and `ticket prefix` as CONTRACT's Board section says.
3. **The contract, section by section.** Walk CONTRACT in order: What the tracker needs to have, Board, Status classes, each operation in the table, Notes, Setup operations, Writing. For each operation, name the tool and the parameters that carry it out, reading the tool's schema (it comes with the ToolSearch result) rather than guessing: the date field that becomes the planned date, how results paginate, whether labels add or replace, whether a comment can be edited in place. Where a choice is theirs (which date field, which grouping is a project), propose one and let them react.
4. **The gaps.** CONTRACT names the survivable ones (no estimate field, no blocked-by relation, no labels on groups, no documents) and the fatal ones (no date field, no way to tell open from closed). Say in the file, and to the user, which the tracker has. A fatal one ends here: `Adapter FAILED at drafting: <tracker> has no <thing>`. With no documents, notes live in pinned tickets, as CONTRACT's Notes section says.
5. **The file.** Write `<tracker>.md` with CONTRACT's headings, the file stem being the tracker's name in lowercase (`jira.md`, `todoist.md`). The line under its title is `**Untested.** Drafted against the <tracker> connector on <date>; no smoke test has run.`
6. **The config.** `tracker` is the file's stem, without `.md`. Run from setup, hand it back with `board name`, `board id` and `ticket prefix`; setup writes them in its phase 6. Run on its own, write the four into the copy's `config.md`.

## Smoke test

Against the user's real board, with the calls the adapter names, loaded by ToolSearch. Compute `TODAY` as the board rules' Dates section says, in the user's timezone (ask if it isn't settled yet). The test uses one throwaway ticket, titled `nudge adapter test <TODAY>`, and one throwaway note, titled `nudge adapter test`.

Run the steps in order. Each ends with one line, `<step>: pass (<call>)` or `<step>: FAIL (<call>): <why>`. Stop at the first failure, fix the adapter's line for that operation (re-read the tool's schema; try the call by hand until it works), and rerun from that step.

1. `ping`: the board named by `board name` comes back.
2. `create ticket`: the throwaway, with a one-line description. Keep its id.
3. `read ticket`: the id returns the title and description.
4. `set planned date` to `TODAY`, then `clear planned date`: a `read ticket` after each shows the date, then none.
5. `set status` to done, then back to a plannable status if the tracker allows it. If it doesn't, leave it done and say so.
6. `add labels`, then `remove labels`, with the `no-autoschedule label`, when the board has that label. If it doesn't, skip the step and say so.
7. `write note` on the throwaway note, then `read note` returns the same content. Then remove the note; if the tracker can't delete one, leave it and say so.
8. `write comment` on the throwaway, `read comments` returns it, `update comment` changes it in place (or as the adapter says it can't).
9. `update ticket`: change the title; `read ticket` shows it.
10. `fetch open` and `fetch closed`: the throwaway shows up in the one its status puts it in, with the standard fields filled.
11. Delete or cancel the throwaway ticket.

A call that fails for a tracker reason (a timeout, a server error) gets one retry, as the board rules say; a second failure is the step's failure.

When every step passes, change the line under the file's title to `Tested on <TODAY> against <tracker>.`

## Result

End with one line:

- `Adapter OK: <file>, tested <TODAY>`
- `Adapter FAILED at <step>: <why>`

Then one line more: the file lives in their personalized copy, so after any change to it they re-package the copy (setup's The copy phase) and install it again. Switching trackers on a copy that is already set up also means redoing setup's phase 1 for the statuses and labels, through the new adapter's Setup operations.
