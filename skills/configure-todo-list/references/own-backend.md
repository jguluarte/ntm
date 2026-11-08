# Your own backend

Walk `references/CONTRACT.md` under `ntm:conventions` with them, heading by
heading, in its order. For each operation, name the tool and the parameters that
carry it out. Once they name the tool for `ping`, confirm the connector as the
skill says. Read the tool's schema from the ToolSearch result rather than
guessing: which date field is the planned date, how results paginate, whether
labels add or replace, whether a comment can be edited in place. Where a choice
is theirs (which date field, which grouping is a project), propose one and let
them react. Try a read by hand where it's cheap. Writes other than the setup
operations wait for `/ntm:self-test`.

The contract names the survivable gaps (no estimate field, no blocked-by
relation, no labels on groups, no documents) and the two fatal ones (no date
field, no way to tell open from closed). Say which the backend has. A fatal one
ends here: `Configure-todo-list FAILED: <backend> has no <thing>`. With no
documents, each database lives in the description of an open task titled with
the database's title, as the contract's Databases section says; tell them.
