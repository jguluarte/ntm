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
NEXT_STEP="Put it back, or ask Justin to approve it in $EXPECTED/."

# How a line in a list in tests/expected/ becomes a name.
STRIP_COMMENT='s/#.*//'
TRIM_SPACES='s/^[[:space:]]+|[[:space:]]+$//g'
DROP_BLANK='/^$/d'

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

# The names a list in tests/expected/ holds, as a set: a name written
# twice counts once here, and list_names_each_once catches it.
names_listed_in() {
    names_written_in "$1" | sorted | uniq
}

# Every name written in a list in tests/expected/, in file order:
# without # comments, blank lines, and spaces around the name.
names_written_in() {
    local list="$REPO_ROOT/$1"
    if [[ ! -r $list ]]; then
        echo "$1 is missing." >&2
        return 1
    fi

    sed -E "$STRIP_COMMENT; $TRIM_SPACES; $DROP_BLANK" "$list"
}

# --- tests/expected/ itself ------------------------------------------

# Fails when a list in tests/expected/ is missing or names a name twice.
list_names_each_once() {
    local list=$1
    local written
    written=$(names_written_in "$list")
    lines_of "$written" | sorted | uniq --repeated |
        reject_name_changes "Listed more than once in $list:"
}

# Fails when tests/expected/plugin.json is missing, isn't JSON, or
# lists no values, since then no plugin.json test runs at all.
expected_plugin_json_has_fields() {
    local fields
    fields=$(expected_plugin_json_fields)
    if [[ -z $fields ]]; then
        echo "$EXPECTED_PLUGIN_JSON lists no values." >&2
        return 1
    fi
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

# Runs the lister, finds each name's file with the path function, and
# prints one finding per file whose name: line differs from the name.
misnamed() {
    local list_names=$1 path_of=$2
    local name
    while read -r name; do
        name_line_differs "$name" "$("$path_of" "$name")"
    done < <("$list_names")
}

# Prints how a file's frontmatter name: line differs from the name its
# folder or file gives it; prints nothing when they match.
name_line_differs() {
    local name=$1 path=$2
    local declared
    declared=$(frontmatter_name "$REPO_ROOT/$path")
    if [[ $declared == "$name" ]]; then
        return 0
    fi

    if [[ -z $declared ]]; then
        echo "$path has no name: line"

    else
        echo "$path has name: \"$declared\""
    fi
}

# Fails when plugin.json's value for one field isn't the one Justin
# expects.
plugin_json_matches() {
    local field=$1
    plugin_json_value_differs "$field" |
        reject_name_changes "Not the value in $EXPECTED_PLUGIN_JSON:"
}

# Prints how plugin.json's value for one field differs from the value
# Justin expects; prints nothing when they match.
plugin_json_value_differs() {
    local field=$1
    local actual expected
    if ! actual=$(json_field_value "$PLUGIN_JSON" "$field"); then
        echo "$PLUGIN_JSON is missing or isn't valid JSON"
        return 0
    fi

    expected=$(json_field_value "$EXPECTED_PLUGIN_JSON" "$field")
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
    LC_ALL=C sort
}

# A list held in a variable, back as lines; an empty list prints none.
lines_of() {
    if [[ -n $1 ]]; then
        printf '%s\n' "$1"
    fi
}

# Reads lines and runs a function on each one, such as a name's path.
each_line() {
    local line
    while read -r line; do "$1" "$line"; done
}

# The value a JSON file in the repo has for one field, as JSON; null
# when it has none. Fails when the file is missing or isn't JSON.
json_field_value() {
    local file=$1 field=$2
    jq --compact-output --arg field "$field" '.[$field]' "$REPO_ROOT/$file"
}

# The name: value in a markdown file's frontmatter, read the way YAML
# reads it: without quotes, a trailing # comment, or trailing spaces.
frontmatter_name() {
    awk '
        { sub(/\r$/, "") }
        /^---[[:space:]]*$/ { fences++; next }
        fences == 1 && /^name:/ {
            sub(/^name:[[:space:]]*/, "")
            sub(/[[:space:]]+#.*$/, "")
            sub(/[[:space:]]+$/, "")
            if (/^".*"$/ || /^\047.*\047$/)
                $0 = substr($0, 2, length($0) - 2)
            print
            exit
        }
    ' "$1"
}

# A test name bats shows as written. bats expands $, ` and \ in the
# names it's given, so each of those, and ", gets a backslash.
literal_test_name() {
    local name=$1
    name=${name//\\/\\\\}
    name=${name//\$/\\\$}
    name=${name//\`/\\\`}
    name=${name//\"/\\\"}
    printf '%s' "$name"
}
