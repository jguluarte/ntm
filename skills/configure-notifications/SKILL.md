---
name: configure-notifications
description: Sets up or changes how ntm's reminders reach the user, in chat: the channel (Pushover, or the scheduled task's own push), the Pushover keys with one test push, and anything about how they want to be notified. Run from neurodivergent-task-manager:configure, or when the user says "set up notifications", "change my Pushover keys", "switch to Pushover", "use Claude's push instead" or "notify me differently".
---

# neurodivergent-task-manager:configure-notifications

Settles Notifications in `ntm:settings` with the user and returns its text.
A short chat: the channel, the keys if Pushover, one test push, one question.
This skill never writes a file.

## Usage

```
/neurodivergent-task-manager:configure-notifications
```

## Before you start

Load `ntm:settings` by name and read Notifications. If it won't load,
nothing is configured yet; carry on. If its Channel line is filled, this is a
re-run: show the current channel, whether the two keys are present (never print
a key in full; the last four characters are enough), and anything written under
the section. Then ask what to change and settle only that.

## The channel

Two channels; offer both in a line each:

- **`pushover`:** a push to their phone from inside the run, through the
  Pushover app. Needs a Pushover app token and user key, which are written into
  `ntm`. Say plainly that the plugin must then stay private. The reliable
  channel, and the only one a chat request ("ping me") can use.
- **`claude-push`:** the scheduled task's own completion push carries the
  reminder. Nothing to set up here;
  `/neurodivergent-task-manager:configure-schedule` turns it on per
  job when it creates them. Best effort: it fires when a run finishes, and a
  chat request can't use it.

Record the channel.

## Pushover keys

With `claude-push`, skip to How you want to be notified.

Ask for the two: the user key is on the Pushover dashboard after signing in; the
app token comes from an application they register there (any name, "ntm" works).
Don't echo either back in chat once given.

Then one test push, with the keys for this call only, so the test doesn't depend
on anything being installed yet. Load `neurodivergent-task-manager:notify` and
run:

```
/neurodivergent-task-manager:notify --title "ntm test" --message "If you can read this, ntm can reach you." --app-token <app token> --user-key <user key>
```

- `Sent: ntm test`: ask them to say "got it" when it arrives, and wait. If
  nothing arrives, the keys were accepted and the push is on Pushover's side:
  have them check the app is installed and signed in with the same account as
  the user key, then send once more.
- `Notify FAILED: <why>`: show the why (an invalid token or user key is named in
  it), ask for the corrected key, and run the test again.

The keys are settled once they've said "got it".

## How you want to be notified

Ask: "anything about how you want to be notified?" Give the kind of thing that
fits in one breath: quiet hours, a different app token per reminder (named by
the kind's default title, whatever the job is called: "Morning reminder uses
token …", "Weekly planning uses token …"), a priority for a certain reminder.
Capture their answer as written, under the section.
`neurodivergent-task-manager:notify` follows it word
for word. "Nothing" leaves it blank.

## Returning the section

Write Notifications in exactly these line shapes, the ones the
`ntm:settings` template uses. The two key lines are left blank with
`claude-push`; the free text follows the lines, as they said it:

```
## Notifications

- Channel: <pushover | claude-push>
- Pushover app token: <token, or blank>
- Pushover user key: <key, or blank>

<anything about how you want to be notified, as written; or nothing>
```

Show it with the keys masked to their last four characters and let them react;
the text you hand on carries the full keys. Then:

- Run from `neurodivergent-task-manager:configure`: return the section to the
  caller, which packages
  once at the end.
- Run directly: load `neurodivergent-task-manager:settings` and follow its
  Regenerating
  `ntm.plugin` section with the section text you produced.
