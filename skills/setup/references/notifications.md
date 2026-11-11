# Notifications

How setup's Notifications step gets each channel ready: the Pushover keys and
one test push, or nothing at all for the AI app's own push.

## Pushover

### The keys

They need the Pushover app on their phone, signed in. Their user key is on their
Pushover dashboard once they sign in at pushover.net. The app token comes from
an application they create there; any name works, such as ntm.

### The test push

Send one push as Send in `notify/pushover.md` says, with the keys they gave,
titled `ntm test`, with the message `If you can read this, ntm can reach you.`

When it returns `Sent:`, ask them to say when it arrives. When it returns
`Notify FAILED:`, show them the why, which names the key Pushover turned down,
and ask for that key again before you send once more.

## The AI app's own push

Nothing to set up now. Create the jobs turns push notifications on for each job,
and the push shows the job's final reply. They need the AI app on their phone,
with its notifications allowed.
