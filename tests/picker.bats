#!/usr/bin/env bats

# bats sets BATS_TEST_DIRNAME to this file's folder.
setup() {
    cd "$BATS_TEST_DIRNAME/.."
}

now='2026-11-13 20:45'

hooks_without_when=(
    characters/detective shared_lines/any_time scenes/stakeout
)

detective_lines=(
    'The answer was on the table.'
    'Nobody leaves this room until I have finished.'
    'Every lie leaves a crumb.'
)

pick() {
    bash scripts/picker/pick "$@"
}

pick_from() {
    local theme=$1 mode=$2 occasions=$3
    shift 3
    pick "$mode" --options "tests/picker/$theme-options.yaml" \
        --history tests/picker/history.jsonl --theme "$theme" \
        --occasions "$occasions" --now "$now" "$@"
}

draw_line() {
    local entry_file=$1 hook=$2 occasions=$3
    shift 3
    pick_from Casebook line "$occasions" --hook "$hook" \
        --entries "tests/picker/$entry_file" "$@"
}

column_of() {
    awk -F '\t' -v column="$1" -v id="$2" -v gives="${3-}" '
        NR == 1 { for (at = 1; at <= NF; at++) number[$at] = at }
        $NF == id && (gives == "" || $1 == gives) { print $(number[column]) }'
}

hook_candidates() {
    pick_from Casebook hook "$1" --chances |
        awk -F '\t' '$1 == "hook" { print $NF }'
}

hook_value() {
    pick_from Casebook hook "$3" --chances | column_of "$1" "$2" hook
}

speaker_value() {
    pick_from Casebook hook "$3" --chances | column_of "$1" "$2" speaker
}

line_candidates() {
    draw_line Casebook-characters.yaml "$1" "$2" --chances |
        awk -F '\t' 'NR > 1 { print $NF }'
}

line_value() {
    draw_line Casebook-characters.yaml "$2" "$3" --chances |
        column_of "$1" "$4"
}

picks_for_seeds() {
    local seed
    for seed in 1 2 3 4 5; do
        pick_from Casebook hook evening --seed "$seed"
    done
}

expect() {
    [ "$1" = "$2" ] && return 0
    echo "expected: $1"
    echo "actual:   $2"
    return 1
}

expect_set() {
    local actual expected
    actual=$(sort)
    expected=$(printf '%s\n' "$@" | sort)
    [ "$actual" = "$expected" ] && return 0
    echo "unexpected: $(only_in "$actual" "$expected")"
    echo "missing: $(only_in "$expected" "$actual")"
    return 1
}

only_in() {
    comm -23 <(echo "$1") <(echo "$2") | paste -sd '|' -
}

expect_one_of() {
    local picked=$1
    shift
    printf '%s\n' "$@" | grep -qxF -- "$picked" && return 0
    echo "expected one of: $*"
    echo "actual: $picked"
    return 1
}

expect_failure() {
    expect 1 "$status"
    expect "Picker FAILED: $1" "$output"
}

@test "when: morning fits the entries without when" {
    hook_candidates morning | expect_set "${hooks_without_when[@]}"
}

@test "when: afternoon fits the entries without when" {
    hook_candidates afternoon | expect_set "${hooks_without_when[@]}"
}

@test "when: evening adds the entries kept for evening" {
    hook_candidates evening |
        expect_set "${hooks_without_when[@]}" shared_lines/evenings
}

@test "when: weekly adds the entries kept for weekly" {
    hook_candidates weekly |
        expect_set "${hooks_without_when[@]}" shared_lines/evenings
}

@test "when: a slip adds the entries kept for a slip, on any reminder" {
    hook_candidates morning,slipped |
        expect_set "${hooks_without_when[@]}" characters/inspector
}

@test "when: a task done adds the entries kept for a task done" {
    hook_candidates morning,done |
        expect_set "${hooks_without_when[@]}" shared_lines/case_closed
}

@test "when: an evening with a slip adds the entries kept for either or both" {
    hook_candidates evening,slipped | expect_set "${hooks_without_when[@]}" \
        shared_lines/evenings characters/inspector shared_lines/cold_trail
}

@test "when: an entry for an evening with a slip is out on an evening without" {
    expect 0 "$(hook_candidates evening | grep -cx shared_lines/cold_trail)"
}

@test "when: a big win draws only from the entries kept for big wins" {
    hook_candidates evening,big_win | expect_set shared_lines/big_win
}

@test "hook: a pick names exactly one hook, from the entries that fit" {
    run pick_from Casebook hook morning --seed 7
    expect 1 "$(grep -c '^hook: ' <<< "$output")"
    expect_one_of "$(sed -n 's/^hook: //p' <<< "$output")" \
        "${hooks_without_when[@]}"
}

@test "hook: the same seed picks the same hook and speaker" {
    expect "$(picks_for_seeds)" "$(picks_for_seeds)"
}

@test "fallback: with no hook fitting, it draws from the entries without when" {
    expect "hook: characters/narrator" \
        "$(pick_from Solo hook evening,big_win | grep '^hook: ')"
}

@test "fallback: a hook drawn without its occasions says so" {
    expect "fallback: no hook fits evening,big_win; drew from the entries \
without when" "$(pick_from Solo hook evening,big_win | grep '^fallback: ')"
}

@test "fallback: with no entry without when either, it fails in one line" {
    cat > "$BATS_TEST_TMPDIR/options.yaml" << 'YAML'
pools:
  scenes:
    gives: [hook]
    entries:
      dusk:
        when: evening
YAML
    run pick hook --options "$BATS_TEST_TMPDIR/options.yaml" \
        --history tests/picker/history.jsonl --theme Dusk \
        --occasions morning --now "$now"
    expect_failure "no hook fits morning, and every entry has a when"
}

@test "rest: an entry used one half-life ago rests at half" {
    expect 0.5 "$(hook_value rest characters/detective evening)"
}

@test "rest: another theme's picks don't rest an entry" {
    expect 1 "$(hook_value rest shared_lines/any_time evening)"
}

@test "rest: a pool without half_life_days never rests its entries" {
    expect 1 "$(hook_value rest scenes/stakeout evening)"
}

@test "score: a score of 1 doubles an entry's weight" {
    expect 0.5 \
        "$(hook_value effective_weight shared_lines/case_closed evening,done)"
}

@test "defaults: an entry without numbers weighs 1" {
    expect 1 "$(hook_value effective_weight scenes/stakeout evening)"
}

@test "defaults: a speaker pool without speaker_rate names one half the time" {
    expect 0.5 "$(speaker_value chance characters/detective evening)"
}

@test "speaker: a pool's speaker_rate is its chance of naming a speaker" {
    expect 0 "$(pick_from Solo hook evening --chances |
        column_of chance characters/narrator speaker)"
}

@test "speaker: a person's line is spoken by that person, whatever the rate" {
    expect "speaker: characters/narrator" \
        "$(pick_from Solo hook evening | grep '^speaker: ')"
}

@test "line: lines and riffs without when fit any occasion" {
    line_candidates characters/detective evening |
        expect_set "${detective_lines[@]}"
}

@test "line: a riff with when fits only its occasions" {
    line_candidates characters/detective evening,done |
        expect_set "${detective_lines[@]}" 'File it under closed.'
}

@test "line: a line drawn one half-life ago rests at half" {
    expect 0.5 "$(line_value rest characters/detective evening \
        'The answer was on the table.')"
}

@test "line: an entry without line_half_life_days never rests its lines" {
    expect 1 "$(line_value rest characters/inspector slipped \
        'Where were you that night?')"
}

@test "line: a riff's bend comes with its line" {
    expect "line: Where were you that night?
bend: Ask the slipped task where it was on the day it was planned." \
        "$(draw_line Casebook-characters.yaml characters/inspector slipped)"
}

@test "line: an entry without lines draws none" {
    expect "line: none" \
        "$(draw_line Casebook-scenes.yaml scenes/stakeout evening)"
}

@test "theme: the next theme follows this week's" {
    expect "theme: Harbor" "$(pick theme --this-week Casebook Casebook Harbor)"
}

@test "theme: the first theme follows the last" {
    expect "theme: Casebook" "$(pick theme --this-week Harbor Casebook Harbor)"
}

@test "theme: a single theme follows itself" {
    expect "theme: Casebook" "$(pick theme --this-week Casebook Casebook)"
}

@test "malformed: an options file that isn't YAML fails in one line" {
    echo 'pools: [unclosed' > "$BATS_TEST_TMPDIR/options.yaml"
    run pick hook --options "$BATS_TEST_TMPDIR/options.yaml" \
        --history tests/picker/history.jsonl --theme Casebook --now "$now"
    expect_failure "$BATS_TEST_TMPDIR/options.yaml isn't YAML"
}

@test "malformed: a history that isn't JSON lines fails in one line" {
    echo '{"sent": "2026-11-13 08:45",' > "$BATS_TEST_TMPDIR/history.jsonl"
    run pick hook --options tests/picker/Casebook-options.yaml \
        --history "$BATS_TEST_TMPDIR/history.jsonl" --theme Casebook \
        --now "$now"
    expect_failure "$BATS_TEST_TMPDIR/history.jsonl isn't JSON lines"
}

@test "malformed: an unknown occasion fails in one line" {
    run pick_from Casebook hook mornin
    expect_failure "unknown occasion: mornin"
}

@test "malformed: a message of two reminders fails in one line" {
    run pick_from Casebook hook morning,evening
    expect_failure "more than one reminder: morning, evening"
}
