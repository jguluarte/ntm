# The names the plugin has, the names Justin expects, and how they compare.

REPO="$BATS_TEST_DIRNAME/.."
EXPECTED="$REPO/tests/expected"

actual_skills() {
    find "$REPO/skills" -mindepth 2 -maxdepth 2 -name SKILL.md \
        | xargs -n 1 dirname | xargs -n 1 basename | sort
}

actual_agents() {
    find "$REPO/agents" -maxdepth 1 -name '*.md' \
        | xargs -n 1 basename | sed 's/\.md$//' | sort
}

expected_skills() { names_in "$EXPECTED/skills.txt"; }
expected_agents() { names_in "$EXPECTED/agents.txt"; }

# A list file: one name per line; blank lines and # comments are skipped.
names_in() {
    grep -v -e '^#' -e '^$' "$1" | sort
}

none_unexpected() {
    fail_if_any "Not expected" "$(comm -13 <($1) <($2))"
}

none_missing() {
    fail_if_any "Expected but missing" "$(comm -23 <($1) <($2))"
}

fail_if_any() {
    local heading=$1 names=$2
    [ -z "$names" ] && return 0
    echo "$heading:"
    echo "$names"
    echo "Put it back, or ask Justin to approve it in tests/expected/."
    return 1
}

plugin_field_as_expected() {
    local field=$1 expected actual
    expected=$(jq -r ".$field" "$EXPECTED/plugin.json")
    actual=$(jq -r ".$field" "$REPO/.claude-plugin/plugin.json")
    [ "$actual" = "$expected" ] && return 0
    echo "plugin.json $field is \"$actual\"; Justin expects \"$expected\"."
    echo "Put it back, or ask Justin to approve it in tests/expected/."
    return 1
}
