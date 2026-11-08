#!/usr/bin/env bats
# User-facing names change only with Justin's yes. These tests compare the
# names the plugin has with the names he expects in tests/expected/, which
# only he edits. See tests/README.md.

load support/names

@test "no skill exists that Justin didn't expect" {
    none_unexpected expected_skills actual_skills
}

@test "every skill Justin expects exists" {
    none_missing expected_skills actual_skills
}

@test "no agent exists that Justin didn't expect" {
    none_unexpected expected_agents actual_agents
}

@test "every agent Justin expects exists" {
    none_missing expected_agents actual_agents
}

@test "plugin.json name is what Justin expects" {
    plugin_field_as_expected name
}

@test "plugin.json displayName is what Justin expects" {
    plugin_field_as_expected displayName
}
