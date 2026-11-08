---
name: configure-notifications
description: >-
    Sets up or changes how ntm's reminders reach the user, in chat: the channel
    (Pushover, or the scheduled task's own push), the Pushover keys with one
    test push, and anything about how they want to be notified. Run from
    ntm:configure, or when the user says "set up notifications", "change my
    Pushover keys", "switch to Pushover", "use Claude's push instead" or "notify
    me differently".
---

# ntm:configure-notifications

Settles Notifications in `ntm-user:settings` with the user and returns the
section's text: the channel, the keys and one test push if Pushover, then one
open question. This skill never writes a file.

## Usage

```
/ntm:configure-notifications
```

## Before you start

Load `ntm-user:settings` by name and read Notifications. If it won't load,
nothing is configured yet; carry on.

If the Channel line is filled, this is a re-run. Show the channel, whether each
key is there, and anything written under the section, then ask what to change
and settle only that. Wherever you show a key, mask it to its last four
characters.

## The channel

Offer both, a line each:

- **`pushover`:** a push to their phone from inside the run, through the
  Pushover app. Reliable, and the only channel a chat request ("ping me") can
  use. The keys are written into `ntm-user`, so say plainly that the plugin must
  then stay private.
- **`claude-push`:** the scheduled task's own push when a run finishes carries
  the reminder. Best effort, and a chat request can't use it. Nothing to set up
  here: `/ntm:configure-schedule` turns it on for each job it creates.

Record their pick. With `claude-push`, skip to How you want to be notified.

## Pushover keys

Ask for both:

- User key: on the Pushover dashboard, after signing in.
- App token: from an application they register there (any name; "ntm" works).

Don't repeat either back in chat.

### Test push

Load `ntm:notify` and send one test with the keys passed in, so it works before
anything is installed:

```
/ntm:notify --title "ntm test"
    --message "If you can read this, ntm can reach you."
    --app-token <app token> --user-key <user key>
```

On `Sent: ntm test`, ask them to say "got it" when it arrives, and wait; their
"got it" settles the keys. If it doesn't arrive, Pushover accepted the keys:
have them check the app is installed and signed in to the same account as the
user key, then send once more.

On `Notify FAILED: <why>`, show the why (it names a bad token or user key), ask
for the corrected key, and test again.

## How you want to be notified

Ask: "anything about how you want to be notified?" Give examples that fit in one
breath: quiet hours, a priority for one reminder, a different app token for one
reminder. Name a reminder by its kind's default title, whatever the job is
called ("Morning reminder uses token …"). Write their answer under the section
as they said it; `ntm:notify` follows it as written. "Nothing" leaves it blank.

## Returning the section

Use the line shapes `ntm-user:settings` uses. With `claude-push` the key lines
are blank; their answer goes below the lines:

```
## Notifications

- Channel: <pushover | claude-push>
- Pushover app token: <token, or blank>
- Pushover user key: <key, or blank>

<anything about how you want to be notified, as written; or nothing>
```

Show it with the keys masked and let them react; the text you hand on has the
full keys. Then:

- Run from `ntm:configure`: return the section; the wizard packages once at the
  end.
- Run directly: load `ntm:settings` and follow its Regenerating
  `ntm-user.plugin` section with this section.
