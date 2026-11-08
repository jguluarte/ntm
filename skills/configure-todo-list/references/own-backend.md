# Your own backend

How `ntm:configure-todo-list` sets up a backend other than Linear, which the
user describes. Statuses, Labels, Databases and Returning the sections are
sections of that skill.

Backend is the name they give. Walk the contract with them in order: What the
backend needs to have, Todo list, Status classes, each operation under
Operations, Databases, Setup operations, Writing. For each operation, name the
tool and the parameters that carry it out. Read the tool's schema from the
ToolSearch result rather than guessing: which date field is the planned date,
how results paginate, whether labels add or replace, whether a comment can be
edited in place. Where a choice is theirs (which date field, which grouping is a
project), propose one and let them react. Try a read by hand where it's cheap.
The setup operations run in Statuses, Labels and Databases as described; every
other write waits for `/ntm:self-test`.

The contract names the survivable gaps (no estimate field, no blocked-by
relation, no labels on groups, no documents) and the two fatal ones (no date
field, no way to tell open from closed). Say which the backend has. A fatal one
ends here: `Configure-todo-list FAILED: <backend> has no <thing>`. With no
documents, each database lives in the description of an open task titled with
the database's title, as the contract's Databases section says; tell them.

What you settle goes under Todo list as prose, in their words, below its lines
(see Returning the sections): one short paragraph per contract heading.
Statuses, Labels and Databases then go through the setup operations as they
described them; the status mapping they gave is the Status classes paragraph.
