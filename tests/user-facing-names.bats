#!/usr/bin/env bats
# The user-facing names are a contract: the skills, the agents, and the
# plugin.json settings in tests/expected/plugin.json. tests/expected/ holds
# it. A test fails when the plugin no longer matches the contract, to tell
# whoever changed it that the change needs their user's explicit involvement.

# bats sets BATS_TEST_DIRNAME to this file's folder. Paths are from the repo
# root.
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

# Each plugin.json setting the contract fixes, one "<key> <value>" per line.
# Values are JSON, so a string keeps its quotes.
expected_plugin_settings() {
    jq -r 'to_entries[] | "\(.key) \(.value|tojson)"' tests/expected/plugin.json
}

# The plugin's value for setting $1, as JSON. A missing setting is null.
get_plugin_setting() {
    jq -c --arg key "$1" '.[$key]' .claude-plugin/plugin.json
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
    echo "ERROR: agent changed a contract without user consent."
    echo "Put it back, or get your user's explicit approval for the change."
    echo "Don't edit tests/expected/ yourself."
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

@test "names contract: no plugin.json setting changed" {
    local key expected actual

    while read -r key expected; do
        actual=$(get_plugin_setting "$key")
        [ "$actual" = "$expected" ] || echo "$key: was $expected, now $actual"
    done < <(expected_plugin_settings) | expect_none "plugin.json changed"
}
