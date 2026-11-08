# The domain behind tests/user-facing-names.bats: the names the plugin
# has, the names Justin expects, and how the two compare.
#
# A list of names is one name per line, sorted the same way every time,
# so two lists compare line by line.

REPO_ROOT="$(cd "$BATS_TEST_DIRNAME/.." && pwd)"

EXPECTED="tests/expected"
SKILLS_LIST="$EXPECTED/skills.txt"
AGENTS_LIST="$EXPECTED/agents.txt"
EXPECTED_PLUGIN_JSON="$EXPECTED/plugin.json"
PLUGIN_JSON=".claude-plugin/plugin.json"

SKILL_FILE="SKILL.md"
AGENT_SUFFIX=".md"
COMMENT_OR_BLANK='^[[:space:]]*(#|$)'
NEXT_STEP="Put it back, or ask Justin to approve it in $EXPECTED/."

# --- What the plugin has ---------------------------------------------

# One name per skill: each folder skills/<name>/ that has a SKILL.md.
skills_in_plugin() {
    local skill_file
    for skill_file in "$REPO_ROOT"/skills/*/"$SKILL_FILE"; do
        [[ -f $skill_file ]] || continue
        basename "$(dirname "$skill_file")"
    done | sorted
}

# One name per agent: each file agents/<name>.md.
agents_in_plugin() {
    local agent_file
    for agent_file in "$REPO_ROOT"/agents/*"$AGENT_SUFFIX"; do
        [[ -f $agent_file ]] || continue
        basename "$agent_file" "$AGENT_SUFFIX"
    done | sorted
}

# The value plugin.json has for one field, as JSON; null when it has none.
plugin_json_value() {
    jq --compact-output --arg field "$1" '.[$field]' "$REPO_ROOT/$PLUGIN_JSON"
}

# --- What Justin expects ---------------------------------------------

expected_skills() {
    names_listed_in "$SKILLS_LIST"
}

expected_agents() {
    names_listed_in "$AGENTS_LIST"
}

# The fields in tests/expected/plugin.json, one per line, in file order.
expected_plugin_json_fields() {
    jq --raw-output 'keys_unsorted[]' "$REPO_ROOT/$EXPECTED_PLUGIN_JSON"
}

# The value Justin expects for one plugin.json field, as JSON.
expected_plugin_json_value() {
    local file="$REPO_ROOT/$EXPECTED_PLUGIN_JSON"
    jq --compact-output --arg field "$1" '.[$field]' "$file"
}

# The names a list in tests/expected/ holds: one per line, without
# its # comments and blank lines.
names_listed_in() {
    local list="$REPO_ROOT/$1"
    if [[ ! -r $list ]]; then
        echo "$1 is missing." >&2
        return 1
    fi

    grep -Ev "$COMMENT_OR_BLANK" "$list" | sed 's/[[:space:]]//g' | sorted
}

# --- Comparing the two -----------------------------------------------

# Names the plugin has that Justin doesn't expect.
unexpected_names() {
    local found=$1 expected=$2
    LC_ALL=C comm -23 <(lines_of "$found") <(lines_of "$expected")
}

# Names Justin expects that the plugin doesn't have.
missing_names() {
    local found=$1 expected=$2
    LC_ALL=C comm -13 <(lines_of "$found") <(lines_of "$expected")
}

# Skills whose SKILL.md name: line differs from the folder, one line each.
misnamed_skills() {
    local skill
    while read -r skill; do
        name_line_differs "$skill" "$(skill_path "$skill")"
    done < <(skills_in_plugin)
}

# Agents whose name: line differs from the file name, one line each.
misnamed_agents() {
    local agent
    while read -r agent; do
        name_line_differs "$agent" "$(agent_path "$agent")"
    done < <(agents_in_plugin)
}

# Prints "<path> has name: <other>" when the file's frontmatter name:
# line isn't the name its folder or file gives it.
name_line_differs() {
    local name=$1 path=$2
    local declared
    declared=$(frontmatter_name "$REPO_ROOT/$path")
    if [[ $declared != "$name" ]]; then
        echo "$path has name: $declared"
    fi
}

# Prints how plugin.json's value for one field differs from the value
# Justin expects; prints nothing when they match.
plugin_json_value_differs() {
    local field=$1
    local actual expected
    actual=$(plugin_json_value "$field")
    expected=$(expected_plugin_json_value "$field")
    if [[ $actual == "$expected" ]]; then
        return 0
    fi

    if [[ $actual == null ]]; then
        echo "$PLUGIN_JSON has no $field; expected $expected"

    else
        echo "$PLUGIN_JSON has $field $actual, not $expected"
    fi
}

# --- Where a name lives ----------------------------------------------

skill_path() {
    echo "skills/$1/$SKILL_FILE"
}

agent_path() {
    echo "agents/$1$AGENT_SUFFIX"
}

# Reads names, one per line, and prints the path of each skill.
skill_paths() {
    local skill
    while read -r skill; do skill_path "$skill"; done
}

# Reads names, one per line, and prints the path of each agent.
agent_paths() {
    local agent
    while read -r agent; do agent_path "$agent"; done
}

# --- Failing a test --------------------------------------------------

# Reads changed names, one path or finding per line. When there are
# any, prints the heading, each line, and what to do next, and fails.
reject_name_changes() {
    local heading=$1
    local changes
    changes=$(cat)
    if [[ -z $changes ]]; then
        return 0
    fi

    {
        echo "$heading"
        lines_of "$changes" | sed 's/^/    /'
        echo
        echo "$NEXT_STEP"
    } >&2
    return 1
}

# --- Plumbing --------------------------------------------------------

# The same byte order everywhere, so comm can compare two lists.
sorted() {
    LC_ALL=C sort --unique
}

# A list held in a variable, back as lines; an empty list prints none.
lines_of() {
    if [[ -n $1 ]]; then
        printf '%s\n' "$1"
    fi
}

# The name: value in a markdown file's frontmatter.
frontmatter_name() {
    awk '
        /^---$/ { fences++; next }
        fences == 1 && /^name:/ { sub(/^name:[[:space:]]*/, ""); print; exit }
    ' "$1"
}
