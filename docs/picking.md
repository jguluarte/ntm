# Picking

Every reminder is built on something from your theme: a line someone in it would
say, a scene, a running joke. ntm picks that first, and the writer then writes
the message around it. A small script, the picker, does the picking by chance,
so your reminders draw on all of your theme instead of the same few favourites.

## What gets picked

Each message gets one hook, the thing it's built on. When the hook has lines to
quote, one of them is picked too. Sometimes a speaker is added: a person from
your theme who says the whole message. When the hook is a person's own line,
that person says it.

## How the chances are weighted

Picture a hat full of slips of paper, each with a name on it, where some names
have more slips than others:

- Something with more lines to it gets more slips.
- Something used lately loses most of its slips, and gets them back over the
  next few days.
- Something kept for an occasion, such as an evening or a task that slipped, is
  only in the hat then. On a big win, only what's kept for big wins is.
- Messages you acted on, or called keepers, give what they were built on more
  slips; ones you called stale, fewer.

Then one slip is drawn.

## Your themes

With more than one theme, ntm uses one a week, in turn, so each gets its week
before any comes back.

## The numbers

The formulas behind the slips are in the picker's reference,
`scripts/picker/README.md`.
