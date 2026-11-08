#!/usr/bin/env bats
# The user-facing names are a contract: the skills, the agents, and
# plugin.json's name and displayName. tests/expected/ holds the contract.
# These tests fail when the plugin no longer matches it, to tell whoever made
# the change that it needs their user's explicit involvement.

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

# The contract lists one name per line, with # comments.
expected_skills() { grep '^[^#]' tests/expected/skills.txt; }
expected_agents() { grep '^[^#]' tests/expected/agents.txt; }

# The lines coming in that aren't lines of the file $1.
not_in() {
    grep -vxF -f "$1"
}

# Passes when no names come in. Otherwise the contract changed: names them.
expect_none() {
    local names
    names=$(paste -s -d ' ' -)
    [ -z "$names" ] && return 0
    contract_changed "$1: $names."
}

expect_plugin_field() {
    local expected actual
    expected=$(jq -r ".$1" tests/expected/plugin.json)
    actual=$(jq -r ".$1" .claude-plugin/plugin.json)
    [ "$actual" = "$expected" ] && return 0
    contract_changed "plugin.json $1 changed from \"$expected\" to \"$actual\"."
}

# Says what differs and what to do, and fails.
contract_changed() {
    echo "$1"
    echo "That changes the user-facing names contract in tests/expected/."
    echo "Put it back, or get your user's explicit approval for the change."
    return 1
}

@test "user-facing names: no skill added" {
    find_skills | not_in <(expected_skills) | expect_none "Skills added"
}

@test "user-facing names: no skill removed" {
    expected_skills | not_in <(find_skills) | expect_none "Skills removed"
}

@test "user-facing names: no agent added" {
    find_agents | not_in <(expected_agents) | expect_none "Agents added"
}

@test "user-facing names: no agent removed" {
    expected_agents | not_in <(find_agents) | expect_none "Agents removed"
}

@test "user-facing names: plugin.json name unchanged" {
    expect_plugin_field name
}

@test "user-facing names: plugin.json displayName unchanged" {
    expect_plugin_field displayName
}
