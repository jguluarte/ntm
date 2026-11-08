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

# --- Skills: one folder skills/<name>/ with a SKILL.md per skill -----

@test "no skill exists that Justin didn't expect" {
    unexpected_names "$(skills_in_plugin)" "$(expected_skills)" |
        skill_paths | reject_name_changes "Not in $SKILLS_LIST:"
}

@test "every skill Justin expects exists" {
    missing_names "$(skills_in_plugin)" "$(expected_skills)" |
        skill_paths | reject_name_changes "Listed in $SKILLS_LIST, missing:"
}

@test "every SKILL.md's name: line matches its folder" {
    misnamed_skills | reject_name_changes "Renamed through name: lines:"
}

# --- Agents: one file agents/<name>.md per agent ---------------------

@test "no agent exists that Justin didn't expect" {
    unexpected_names "$(agents_in_plugin)" "$(expected_agents)" |
        agent_paths | reject_name_changes "Not in $AGENTS_LIST:"
}

@test "every agent Justin expects exists" {
    missing_names "$(agents_in_plugin)" "$(expected_agents)" |
        agent_paths | reject_name_changes "Listed in $AGENTS_LIST, missing:"
}

@test "every agent's name: line matches its file name" {
    misnamed_agents | reject_name_changes "Renamed through name: lines:"
}

# --- plugin.json: one test per value Justin expects ------------------

plugin_json_matches() {
    local field=$1
    plugin_json_value_differs "$field" |
        reject_name_changes "Not the value in $EXPECTED_PLUGIN_JSON:"
}

for field in $(expected_plugin_json_fields); do
    value=$(expected_plugin_json_value "$field")
    bats_test_function --description "$field is ${value//\"/\\\"}" \
        -- plugin_json_matches "$field"
done
