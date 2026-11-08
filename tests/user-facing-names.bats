#!/usr/bin/env bats
#
# User-facing names change only with Justin's explicit yes.
#
# These tests compare the names the plugin has with the names Justin
# expects, which live in tests/expected/. A rename fails here until he
# updates that folder himself; a hook in his own Claude Code settings
# blocks every Claude session from editing it. See
# tests/expected/README.md.

load support/names

# --- tests/expected/: readable, so the tests below compare something -

@test "$SKILLS_LIST lists each skill once" {
    list_names_each_once "$SKILLS_LIST"
}

@test "$AGENTS_LIST lists each agent once" {
    list_names_each_once "$AGENTS_LIST"
}

@test "$EXPECTED_PLUGIN_JSON lists at least one value" {
    expected_plugin_json_has_fields
}

# --- Skills: one folder skills/<name>/ with a SKILL.md per skill -----

@test "no skill exists that Justin didn't expect" {
    unexpected_names "$(skills_in_plugin)" "$(expected_skills)" |
        each_line skill_path | reject_name_changes "Not in $SKILLS_LIST:"
}

@test "every skill Justin expects exists" {
    missing_names "$(skills_in_plugin)" "$(expected_skills)" |
        each_line skill_path |
        reject_name_changes "Listed in $SKILLS_LIST, missing:"
}

@test "every SKILL.md's name: line matches its folder" {
    misnamed skills_in_plugin skill_path |
        reject_name_changes "Renamed through name: lines:"
}

# --- Agents: one file agents/<name>.md per agent ---------------------

@test "no agent exists that Justin didn't expect" {
    unexpected_names "$(agents_in_plugin)" "$(expected_agents)" |
        each_line agent_path | reject_name_changes "Not in $AGENTS_LIST:"
}

@test "every agent Justin expects exists" {
    missing_names "$(agents_in_plugin)" "$(expected_agents)" |
        each_line agent_path |
        reject_name_changes "Listed in $AGENTS_LIST, missing:"
}

@test "every agent's name: line matches its file name" {
    misnamed agents_in_plugin agent_path |
        reject_name_changes "Renamed through name: lines:"
}

# --- plugin.json: one test per value Justin expects ------------------

# A broken expected file adds no tests here and stays quiet; the test
# that it lists at least one value says what's wrong with it, once.
add_plugin_json_tests() {
    local field value description
    while read -r field; do
        value=$(json_field_value "$EXPECTED_PLUGIN_JSON" "$field")
        description=$(literal_test_name "$field is $value")
        bats_test_function --description "$description" \
            -- plugin_json_matches "$field"
    done < <(expected_plugin_json_fields 2>/dev/null)
}

add_plugin_json_tests
