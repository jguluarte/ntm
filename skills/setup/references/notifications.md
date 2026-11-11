# Notifications setup

The Pushover keys and the one test push, for setup's Notifications step when the
user picks Pushover.

## The keys

Ask for the two: the user key is on the Pushover dashboard after signing in; the
app token comes from an application they register there (any name, "ntm" works).
Don't echo either back in chat once given.

Say plainly that the keys go into their user plugin, so it must stay private.

## The test push

Read `notify/pushover.md`, beside this file, and send one push as its Sending
says, with their keys in place of its placeholders:

| Field   | Value                                    |
| ------- | ---------------------------------------- |
| Title   | ntm test                                 |
| Message | If you can read this, ntm can reach you. |

### `Sent: ntm test`

Ask them to say "got it" when it arrives, and wait. If nothing arrives, the keys
were accepted and the push is on Pushover's side: have them check the app is
installed and signed in with the same account as the user key, then send once
more.

### `Notify FAILED: <why>`

Show the why, ask for the corrected key, and send the test again.

## Saving the keys

Once they've said "got it", the keys go into `ntm-user:notify`, in place of the
placeholders.
