# Picking

Every reminder is built on something from your theme: a line someone in it would
say, a scene, a running joke. ntm picks that first, and the writer then writes
the message around it. A small script, the picker, does the picking by chance,
so your reminders draw on all of your theme instead of the same few favourites.

A theme kept in one Theme database, the way ntm builds themes today, doesn't use
the picker yet: ntm picks something from it that no recent reminder used.

## What gets picked

Each message gets one hook, the thing it's built on. When the hook has lines to
quote, one of them is picked too. Sometimes a speaker is added: a person from
your theme who says the whole message. When the hook is a person's own line,
that person says it.

## How the chances are weighted

Picture a hat full of slips of paper, each with a name on it, where some names
have more slips than others:

- A scene, or anything else with no lines to quote, gets a full share of slips.
  Something with lines gets fewer, closer to a full share the more lines it has,
  so a few lines aren't quoted over and over.
- Something used lately loses most of its slips, and gets them back over the
  next few days.
- Something kept for an occasion, such as an evening or a task that slipped, is
  only in the hat then. On a big win, the hat holds only what's kept for big
  wins, when your theme has any.
- Messages you acted on, or called keepers, give what they were built on more
  slips; ones you called stale, fewer.

Then one slip is drawn.

## Your themes

With more than one theme, ntm uses one a week, in turn, so each gets its week
before any comes back.

## The numbers

The formulas behind the slips are in the picker's reference,
`scripts/picker/README.md`.
