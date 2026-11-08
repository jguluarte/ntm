#!/usr/bin/env bats
# The user-facing names are a contract: the skills, the agents, and the
# plugin.json fields in tests/expected/plugin.json. tests/expected/ holds it.
# A test fails when the plugin no longer matches the contract, to tell
# whoever changed it that the change needs their user's explicit involvement.

# Paths are from the repo root.
setup() {
    cd "$BATS_TEST_DIRNAME/.."
}

# A skill is a folder skills/<name>/ with a SKILL.md.
find_skills() {
    ls skills/*/SKILL.md | cut -d / -f 2
}

# An agent is a file agents/<name>.md.
find_agents() {
    basename -s .md agents/*.md
}

# The contract's names for $1 (skills or agents): one per line, and #
# starts a comment.
contract_names() {
    grep '^[^#]' "tests/expected/$1.txt"
}

# Prints the lines from the pipe that aren't a whole line of the file $1.
# The tests pass a command's output as that file with <(command).
not_in() {
    grep -vxF -f "$1"
}

# The value of field $1 in the JSON file $2, as JSON. A missing field is null.
field() {
    jq --arg name "$1" '.[$name]' "$2"
}

# Each field in the contract's plugin.json whose value in the plugin's
# plugin.json differs, one per line.
changed_plugin_fields() {
    local name expected actual
    for name in $(jq -r 'keys[]' tests/expected/plugin.json); do
        expected=$(field "$name" tests/expected/plugin.json)
        actual=$(field "$name" .claude-plugin/plugin.json)
        [ "$actual" = "$expected" ] || echo "$name: was $expected, now $actual"
    done
}

# Reads lines from the pipe. Passes when there are none. Otherwise prints
# $1 and the lines, and fails: the contract changed.
expect_none() {
    local found
    found=$(cat)
    [ -z "$found" ] && return 0
    echo "$1:"
    echo "$found"
    contract_changed
}

# Says what a contract change needs, and fails.
contract_changed() {
    echo "That changes the user-facing names contract in tests/expected/,"
    echo "which needs your user's explicit involvement. Put it back, or stop"
    echo "and get their approval. Don't edit tests/expected/ yourself."
    return 1
}

@test "names contract: no skill added" {
    find_skills | not_in <(contract_names skills) | expect_none "Skills added"
}

@test "names contract: no skill removed" {
    contract_names skills | not_in <(find_skills) | expect_none "Skills removed"
}

@test "names contract: no agent added" {
    find_agents | not_in <(contract_names agents) | expect_none "Agents added"
}

@test "names contract: no agent removed" {
    contract_names agents | not_in <(find_agents) | expect_none "Agents removed"
}

@test "names contract: no plugin.json field changed" {
    changed_plugin_fields | expect_none "plugin.json fields changed"
}
