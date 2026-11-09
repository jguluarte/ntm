# Databases

Setup's databases step. Confirms the names of the databases the user's features
need, and says where each lives. It creates none: Settings was created when the
todo list was saved, and Style when the persona was. Every other database is
created by the skill that keeps it, the first time it writes.

## The names

Show the names in one short list, each with what it holds in a few words. Only
the ones they need. Settings and Style are already made, so show them as done,
under the names they have:

- `Settings`: their settings. Everyone. Already made.
- `Style`: their persona's Profile. When they built a persona. Already made.
- `Message history`: what reminders have said, so they don't repeat. When they
  built a persona.
- `Paused dates`: the days nothing gets planned automatically. Task management.
- `Task review log`: how they work and how they estimate, from each review. Task
  management.
- `Price watch stores`: the stores they vouched for or blocked. Price watch. In
  the same line, say they can name a few stores they trust, by category with
  their domains; record them for the build, as the Seed list for the database's
  first write.

A plain "ok" keeps every name. For the databases still to be created, record any
other name they give, such as a document they already keep under another title,
for the build, which writes where each document lives into `ntm-user:backend`.

## Where they live

On Linear, say in a line or two: each database is its own Linear document,
titled with its name, in the todo list's team, Linear's base location; the price
watch stores sit in the documents of the project that carries $price-watch.

On their own backend, work out where each lives from what they described for
Databases in `backends/contract.md`: a document found by its title, or, with no
documents, a task titled with the database's name. Tell them in a line.
