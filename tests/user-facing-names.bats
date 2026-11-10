#!/usr/bin/env bats

# bats sets BATS_TEST_DIRNAME to this file's folder.
setup() {
    cd "$BATS_TEST_DIRNAME/.."
}

find_skills() {
    ls skills/*/SKILL.md | cut -d / -f 2
}

find_agents() {
    # Exclude agents/README.md: it's the folder's documentation, not an agent.
    basename -s .md agents/*.md | grep -vx README
}

load_file() {
    grep '^[^#]' "tests/expected/$1.txt"
}

not_in() {
    grep -vxF -f "$1"
}

settings_in() {
    jq -r 'to_entries[] | "\(.key) \(.value|tojson)"' "$1"
}

expected_settings() {
    settings_in tests/expected/plugin.json
}

find_settings() {
    settings_in .claude-plugin/plugin.json
}

expect_none() {
    local found
    found=$(cat)

    [ -z "$found" ] && return 0

    echo "$1:"
    echo "$found"
    contract_changed
}

contract_changed() {
    echo "ERROR: a user-facing name changed."
    echo "Meant: update tests/expected/ in this PR and say so. Not: put it back."
    return 1
}

@test "names contract: no skill added" {
    find_skills | not_in <(load_file skills) | expect_none "Skills added"
}

@test "names contract: no skill removed" {
    load_file skills | not_in <(find_skills) | expect_none "Skills removed"
}

@test "names contract: no agent added" {
    find_agents | not_in <(load_file agents) | expect_none "Agents added"
}

@test "names contract: no agent removed" {
    load_file agents | not_in <(find_agents) | expect_none "Agents removed"
}

@test "names contract: no plugin.json setting changed" {
    expected_settings | not_in <(find_settings) | expect_none "Settings differ"
}
