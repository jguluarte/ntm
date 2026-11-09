# Your own backend

How setup's todo list step finds a backend with someone who doesn't want Linear,
and describes it with them against the backend contract. Only this path reads
this file. The description it produces is the backend's guide: the build writes
it into `ntm-user:backend` as that user's calls.

## Finding one

Read `contract.md`, beside this file, first. Its What the backend needs to have
is what every choice is held to.

Ask what they keep tasks in today, or what they'd like to. Each time you suggest
something, offer the two ways that always work:

- **Built inside Claude:** a todo list kept in a Claude Doc or an artifact that
  holds the data, made with them here.
- **An existing tool:** an app they use or like, reached through a Claude
  connector.

Search with them: ToolSearch for connectors already attached, and the web for a
tool's Claude connector and what it can do. Hold each option up to the contract
in a line or two, gaps included. Keep looking until they're content with one.
Then connect it: on the Connectors tab in Claude's settings when it isn't there
yet, and ToolSearch again before going on.

## Describing it

Walk the contract with them, heading by heading, in its order. For each
operation, name the tool and the parameters that carry it out. Read the tool's
schema from the ToolSearch result rather than guessing: which date field is the
planned date, how results paginate, whether labels add or replace, whether a
comment can be edited in place. Where a choice is theirs (which date field,
which grouping is a project), propose one and let them react.

Once they name the tool for `ping`, run it right away. A pass: say in a line
that the list answers. Anything else: fix it with them, and don't go on until it
passes. Try other reads by hand where it's cheap. Writes other than the setup
operations wait for `/ntm:self-test`.

Say which of the gaps under What the backend needs to have the backend has. For
no date field, or no way to tell open from closed, look with them for something
that covers it: a field or status they can repurpose, a label, or a different
place to keep the list, such as one built inside Claude. Carry on once it's
covered. With no documents, each database lives in the description of an open
task titled with the database's title, as Databases says; tell them.

Keep the description for the build: one short paragraph per contract heading, in
their words where they gave them.
