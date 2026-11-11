# Notifications setup

Setup's notifications step, a short chat: the channel, the Pushover keys with
one test push, then how they want to be notified.

## The channel

Strongly suggest Pushover: reminders arrive in a separate app on their phone or
computer, which their phone's focus settings can treat differently from
everything else. It's also the only channel a chat request ("ping me") can use.
It needs a Pushover user key and app token, which the build writes into their
plugin; say plainly that the plugin must then stay private. Its channel value is
`pushover`.

Otherwise, the AI app's own push: the scheduled task's completion push carries
the reminder. Nothing to set up here; `ntm:schedules` turns it on for each job
it creates. Best effort: it fires when a run finishes, and a chat request can't
use it. Its channel value is `claude-push`.

Hold the channel for the build, which writes it into `ntm-user:notify`.

## Pushover keys

With `claude-push`, skip to How you want to be notified.

Ask for the two: the user key is on the Pushover dashboard after signing in; the
app token comes from an application they register there (any name, "ntm" works).
Don't echo either back in chat once given.

Then one test push, with the keys given for this call, since nothing is
installed yet. Read `notify.md` and send it as its Pushover section says, as if
called with:

```
--title "ntm test"
--message "If you can read this, ntm can reach you."
--app-token <app token> --user-key <user key>
```

- `Sent: ntm test`: ask them to say "got it" when it arrives, and wait. If
  nothing arrives, the keys were accepted and the push is on Pushover's side:
  have them check the app is installed and signed in with the same account as
  the user key, then send once more.
- `Notify FAILED: <why>`: show the why (an invalid token or user key is named in
  it), ask for the corrected key, and run the test again.

The keys are settled once they've said "got it". Hold them for the build, which
writes them into `ntm-user:notify`; they never go in the `%Settings` document.

## How you want to be notified

Ask: "anything about how you want to be notified?" Give the kind of thing that
fits in one breath: quiet hours, a priority for a certain reminder. Capture
their answer as written; `ntm-user:notify` follows it word for word.

## Saving the area

Save without asking, unless they'd rather save each piece: write their answer
under Notifications in the `%Settings` document, with the backend reference the
todo list step followed. "Nothing" leaves the section out. Show what you saved
and the channel, with any key masked to its last four characters, and let them
react.
