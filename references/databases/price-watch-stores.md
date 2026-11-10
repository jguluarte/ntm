# Price watch stores

<!--
For the agent: the stores the user trusts or refuses for the price watch, for
every watched item. Its contents are the user's own to customize: ntm suggests
no stores, so setup creates this database from this template with empty lists,
apart from the Seed stores the user names then. Write the database without
these comments: they are for you, never for the user. Each store is one line
with its domain, the store's main site for the user's country.
-->

## Seed

<!--
Stores the user trusts as starting points for a full search, under a heading
for the kind of item they sell. Setup writes the ones the user names; change
them only when the user asks. A category looks like:

### Camping gear

- Ridgeline Outdoors (ridgeline.example)
- Trailhead Supply (trailhead.example)
-->

## Vouched

<!--
Stores the user vouched for, checked every day for any item they sell. Each
line has the date and the user's reason, if they gave one. A store they vouch
for comes off Blocked. A line looks like:

- Corner Hardware (cornerhardware.example): 2026-11-09, ships fast, real stock
-->

## Blocked

<!--
Stores the user never wants used, on their own site or as a seller on another.
A store they block comes off Vouched. A line looks like:

- Bargain Bin (bargainbin.example): 2026-11-09, shipped a scuffed return as new
-->
