# Notifications

## Pushover

### The keys

They need the Pushover app on their phone, signed in. Their user key is on their
Pushover dashboard once they sign in at pushover.net. The app token comes from
an application they create there; any name works, such as ntm.

### The test push

Send one push as Send and Result in `notify/pushover.md` say, with the keys they
gave, titled `ntm test`, with the message
`If you can read this, ntm can reach you.`

When it returns `Sent:`, ask them to say when it arrives. When it returns
`Notify FAILED:`, show them why, and ask for the key again.

## The AI app's own push

Nothing to set up: the Create the jobs step turns push notifications on for each
job, and the push shows the job's final reply. They need the AI app on their
phone, with its notifications allowed.
