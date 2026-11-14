def reminder_occasions: ["morning", "afternoon", "evening", "weekly"];

def big_win: "big_win";

def task_occasions: ["slipped", "done", big_win];

def every_occasion: reminder_occasions + task_occasions;

def a_hook: "hook";

def a_speaker: "speaker";

def nothing_picked: "none";

def default_weight: 1;

def default_score: 0;

def default_speaker_rate: 0.5;

def fully_rested: 1;

def seconds_in_a_day: 86400;

def time_format: "%Y-%m-%d %H:%M";

def code_fence: "```";

def shown_decimals: 2;

def flags($args): $args.named + {themes: $args.positional};

def named_inputs: reduce inputs as $input ({}; . + $input);

def unknown_occasions: . - every_occasion;

def reminders_named: . - task_occasions;

def checked_occasions:
    if unknown_occasions != [] then
        error("unknown occasion: \(unknown_occasions | join(", "))")
    elif (reminders_named | length) > 1 then
        error("more than one reminder: \(reminders_named | join(", "))")
    else .
    end;

def trimmed: sub("^\\s+"; "") | sub("\\s+$"; "");

def occasions_from_flag:
    split(",") | map(trimmed | select(. != "")) | checked_occasions;

def when_list: [.when // empty] | flatten;

def unknown_when: when_list - every_occasion;

def first_unknown_when(whens):
    first(whens | select(unknown_when != [])) // null;

def unknown_when_error:
    "\(.owner) has an unknown when: \(unknown_when | join(", "))";

def known_whens(whens):
    first_unknown_when(whens) as $unknown
    | if $unknown == null then . else error($unknown | unknown_when_error) end;

def allows($occasions): . == [] or any(.[]; IN($occasions[]));

def fits($occasions):
    when_list as $when
    | ($when - task_occasions | allows($occasions)) as $reminder_fits
    | ($when - reminder_occasions | allows($occasions)) as $what_happened_fits
    | $reminder_fits and $what_happened_fits;

# --now and sent are both the user's local time; reading both as UTC keeps
# the days between them right.
def parsed_time: strptime(time_format) | mktime;

def now_time:
    . as $text
    | try parsed_time catch error("--now takes YYYY-MM-DD HH:MM, not \($text)");

def sent_time: try (.sent | parsed_time) catch null;

def days_since($now):
    if . == null then null
    else ([$now - ., 0] | max) / seconds_in_a_day
    end;

def rest($half_life; $days):
    if $half_life == null or $days == null then fully_rested
    else fully_rested - pow(2; -$days / $half_life)
    end;

def message($flags; $history):
    {
        occasions: ($flags.occasions | occasions_from_flag),
        now: ($flags.now | now_time),
        theme_history: [$history[] | select(.theme == $flags.theme)]
    };

def latest_use_time: map(sent_time | values) | max;

def days_since_used($id; $message):
    $message.theme_history
    | map(select(.hook == $id or .speaker == $id))
    | latest_use_time | days_since($message.now);

def days_since_drawn($line; $message):
    $message.theme_history
    | map(select(.line_drawn == $line))
    | latest_use_time | days_since($message.now);

def well_formed_pool:
    (.gives | type) == "array" and (.entries | type) == "object";

def broken_pools:
    .pools | to_entries[] | select(.value | well_formed_pool | not) | .key;

def first_broken_pool: first(broken_pools) // null;

def entry_whens:
    .pools | to_entries[] | .key as $kind
    | .value.entries | to_entries[]
    | {owner: "\($kind)/\(.key)", when: (.value // {} | .when)};

def checked_options:
    if (.pools | type) != "object" then error("the options file has no pools")
    elif first_broken_pool != null then
        error("pool \(first_broken_pool) needs gives and entries")
    else known_whens(entry_whens)
    end;

def holds_an_entry: test("\\S") and (startswith(code_fence) | not);

def history_entry:
    .key as $index
    | .value
    | try fromjson catch error("history line \($index + 1) isn't JSON");

def history_entries:
    split("\n") | to_entries
    | map(select(.value | holds_an_entry) | history_entry);

def message_inputs($flags):
    named_inputs as $files
    | {
        options: ($files.options | checked_options),
        message: message($flags; $files.history | history_entries),
        entries: $files.entries
    };

def candidate($id; $entry; $pool; $message):
    {
        id: $id,
        when: ($entry | when_list),
        person: (a_speaker | IN($pool.gives[])),
        weight: ($entry.weight // default_weight),
        score: ($entry.score // default_score),
        rest: rest($pool.half_life_days; days_since_used($id; $message)),
        speaker_rate: ($pool.speaker_rate // default_speaker_rate)
    };

def entries_giving($gives; $options; $message):
    [
        $options.pools | to_entries[] | .key as $kind | .value as $pool
        | select($gives | IN($pool.gives[]))
        | $pool.entries | to_entries[]
        | candidate("\($kind)/\(.key)"; .value // {}; $pool; $message)
    ];

def effective_weight($rest): .weight * pow(2; .score) * $rest;

def total_effective_weight: map(.effective_weight) | add // 0;

def weighed:
    map(.effective_weight = effective_weight(.rest))
    | if total_effective_weight > 0 then .
    else map(.effective_weight = effective_weight(fully_rested))
    end;

def kept_for_big_wins: any(.when[]; . == big_win);

def without_when: .when == [];

def big_win_hooks:
    map(select(kept_for_big_wins)) as $kept
    | if $kept != [] then {candidates: $kept, fallback: false}
    else {candidates: map(select(without_when)), fallback: true}
    end;

def hook_candidates($options; $message):
    entries_giving(a_hook; $options; $message)
    | map(select(fits($message.occasions)))
    | if big_win | IN($message.occasions[]) then big_win_hooks
    else {candidates: ., fallback: false}
    end
    | .candidates |= weighed;

def speaker_candidates($options; $message):
    entries_giving(a_speaker; $options; $message)
    | map(select(fits($message.occasions)))
    | weighed;

def line_candidate($line; $bend):
    {line: $line, bend: $bend, weight: default_weight, score: default_score};

def riff_whens($hook):
    (.riffs // [])[] | {owner: "a riff of \($hook)", when};

def text_line($hook):
    if type == "string" then .
    else error("\($hook) has a line that isn't text: \(tojson)")
    end;

def line_candidates($hook; $half_life; $message):
    known_whens(riff_whens($hook))
    | [(.lines // [])[] | line_candidate(text_line($hook); null)]
    + [
        (.riffs // [])[] | select(fits($message.occasions))
        | line_candidate(.line | text_line($hook); .bend)
    ]
    | map(.rest = rest($half_life; days_since_drawn(.line; $message)))
    | weighed;

def park_miller_modulus: 2147483647;

def park_miller_multiplier: 48271;

# The Park-Miller generator: one seed gives the same numbers on any machine.
def park_miller($state; $count):
    [
        foreach range($count) as $_ ($state;
            . * park_miller_multiplier % park_miller_modulus)
    ];

def first_state($seed): $seed % (park_miller_modulus - 1) + 1;

# Its first numbers follow a small seed closely, so it skips two.
def numbers_skipped: 2;

def random_numbers($seed; $count):
    park_miller(first_state($seed); numbers_skipped + $count)
    | .[numbers_skipped:]
    | map(. / park_miller_modulus);

def draw($random):
    total_effective_weight as $total
    | first(
        foreach .[] as $candidate (0;
            . + $candidate.effective_weight;
            select(. > $random * $total) | $candidate)
    ) // null;

def with_chances:
    total_effective_weight as $total
    | map(.chance = if $total > 0 then .effective_weight / $total else 0 end);

def speaker_for($hook; $speakers; $speaker_draw; $speaker_kept):
    ($speakers | draw($speaker_draw)) as $drawn
    | if $hook.person then $hook.id
    elif $drawn != null and $speaker_kept < $drawn.speaker_rate then $drawn.id
    else nothing_picked
    end;

def rounded:
    pow(10; shown_decimals) as $scale
    | . * $scale | round / $scale;

def shown: if type == "number" then rounded else . end;

def table($columns):
    ($columns | @tsv),
    (.[] | . as $row | [$columns[] | $row[.] | shown] | @tsv);

def candidate_columns:
    ["gives", "chance", "effective_weight", "weight", "score", "rest", "id"];

def line_columns: ["chance", "rest", "line"];

def hook_rows: with_chances | map(.gives = a_hook);

def speaker_rows:
    with_chances | map(.chance *= .speaker_rate | .gives = a_speaker);

def hook_chances($hooks; $speakers):
    ($hooks | hook_rows) + ($speakers | speaker_rows)
    | table(candidate_columns);

def drawable_hooks($occasions):
    ($occasions | join(",")) as $named
    | if . == [] then
        error("no hook fits \($named), and every entry has a when")
    elif total_effective_weight == 0 then
        error("every hook that fits \($named) weighs 0")
    else .
    end;

def hook_pick($hooks; $speakers; $seed):
    random_numbers($seed; 3) as [$hook_draw, $speaker_draw, $speaker_kept]
    | ($hooks | draw($hook_draw)) as $hook
    | speaker_for($hook; $speakers; $speaker_draw; $speaker_kept) as $speaker
    | "hook: \($hook.id)", "speaker: \($speaker)";

def fallback_note($fallback; $occasions):
    if $fallback then
        "fallback: no hook fits \($occasions);"
        + " drew from the entries without when"
    else empty
    end;

def hook($flags):
    message_inputs($flags) as {$options, $message}
    | hook_candidates($options; $message) as {$candidates, $fallback}
    | speaker_candidates($options; $message) as $speakers
    | ($flags.seed | tonumber) as $seed
    | (
        if $flags.chances then hook_chances($candidates; $speakers)
        else
            $candidates | drawable_hooks($message.occasions)
            | hook_pick(.; $speakers; $seed)
        end
    ),
    fallback_note($fallback; $flags.occasions);

def entry_for($slug; $not_found):
    if (. // {}) | has($slug) then .[$slug] // {} else error($not_found) end;

def kind_and_slug:
    split("/") as $parts
    | if ($parts | length) == 2 and all($parts[]; . != "") then $parts
    else error("--hook takes <kind>/<slug>, not \(.)")
    end;

def hook_option($options; $hook):
    ($hook | kind_and_slug) as [$kind, $slug]
    | $options.pools[$kind].entries
    | entry_for($slug; "\($hook) isn't in the options file");

def hook_entry($entries; $hook):
    ($hook | kind_and_slug) as [$kind, $slug]
    | $entries[$kind]
    | entry_for($slug; "\($hook) isn't in the entry file");

def line_pick($seed):
    random_numbers($seed; 1) as [$line_draw]
    | draw($line_draw) as $drawn
    | if $drawn == null then "line: \(nothing_picked)"
    else "line: \($drawn.line)", ($drawn.bend // empty | "bend: \(.)")
    end;

def line($flags):
    message_inputs($flags) as {$options, $message, $entries}
    | (hook_option($options; $flags.hook) | .line_half_life_days) as $half_life
    | hook_entry($entries; $flags.hook)
    | line_candidates($flags.hook; $half_life; $message)
    | if $flags.chances then with_chances | table(line_columns)
    else line_pick($flags.seed | tonumber)
    end;

def next_theme($this_week):
    (index($this_week) // -1) as $this_weeks_place
    | .[($this_weeks_place + 1) % length];

def theme($flags):
    "theme: \($flags.themes | next_theme($flags.this_week))";

def report(answer):
    try answer catch ("Picker FAILED: \(.)\n" | halt_error(1));
