def reminder_occasions: ["morning", "afternoon", "evening", "weekly"];

def task_occasions: ["slipped", "done", "big_win"];

def occasions:
    (split(",") | map(select(. != ""))) as $named
    | ($named - reminder_occasions - task_occasions) as $unknown
    | ($named - task_occasions) as $reminders
    | if $unknown != [] then error("unknown occasion: \($unknown | join(", "))")
      elif ($reminders | length) > 1
      then error("more than one reminder: \($reminders | join(", "))")
      else $named
      end;

def when_list: [.when // empty] | flatten;

def allows($occasions): . == [] or any(.[]; IN($occasions[]));

def fits($occasions):
    when_list as $when
    | ($when - task_occasions | allows($occasions)) as $reminder_fits
    | ($when - reminder_occasions | allows($occasions)) as $tasks_fit
    | $reminder_fits and $tasks_fit;

def timestamp:
    . as $text
    | try (strptime("%Y-%m-%d %H:%M") | mktime)
      catch error("\($text) isn't a YYYY-MM-DD HH:MM time");

def days_since($now):
    if . == null then null else ([$now - ., 0] | max) / 86400 end;

def rest($half_life; $days):
    if $half_life == null or $days == null then 1
    else 1 - pow(2; -$days / $half_life)
    end;

def message($history; $flags):
    {
        occasions: ($flags.occasions | occasions),
        now: ($flags.now | timestamp),
        recent: [$history[] | select(.theme == $flags.theme)]
    };

def last_sent: map(.sent | timestamp) | max;

def days_since_used($id; $message):
    $message.recent
    | map(select(.hook == $id or .speaker == $id))
    | last_sent | days_since($message.now);

def days_since_drawn($line; $message):
    $message.recent
    | map(select(.line_drawn == $line))
    | last_sent | days_since($message.now);

def well_formed_pool:
    (.gives | type) == "array" and (.entries | type) == "object";

def broken_pools:
    .pools | objects | to_entries[]
    | select(.value | well_formed_pool | not) | .key;

def checked_options:
    [broken_pools][0] as $broken
    | if (.pools | type) != "object" then error("the options file has no pools")
      elif $broken != null then error("pool \($broken) needs gives and entries")
      else .
      end;

def listed($slug; $missing):
    if (. // {}) | has($slug) then .[$slug] // {} else error($missing) end;

def entries_giving($role; $options; $message):
    [
        $options.pools | to_entries[] | .key as $kind | .value as $pool
        | select($role | IN($pool.gives[]))
        | $pool.entries | to_entries[]
        | "\($kind)/\(.key)" as $id
        | (.value // {}) as $entry
        | {
            entry: $id,
            when: ($entry | when_list),
            weight: ($entry.weight // 1),
            score: ($entry.score // 0),
            rest: rest($pool.half_life_days; days_since_used($id; $message)),
            speaker_rate: ($pool.speaker_rate // 0.5)
        }
        | .effective = .weight * pow(2; .score) * .rest
    ];

def big_win_only($occasions):
    def kept_for_big_wins: any(.when[]; . == "big_win");
    if "big_win" | IN($occasions[]) then map(select(kept_for_big_wins))
    else .
    end;

def hooks_for($options; $message):
    entries_giving("hook"; $options; $message) as $all
    | ($all | map(select(fits($message.occasions)))
        | big_win_only($message.occasions)) as $fitting
    | if $fitting != [] then {candidates: $fitting, fallback: false}
      else {candidates: ($all | map(select(.when == []))), fallback: true}
      end;

def speakers_for($options; $message):
    entries_giving("speaker"; $options; $message)
    | map(select(fits($message.occasions)));

def line_candidates($entry; $half_life; $message):
    [($entry.lines // [])[] | {line: .}]
    + [($entry.riffs // [])[] | select(fits($message.occasions)) | {line, bend}]
    | map(
        .rest = rest($half_life; days_since_drawn(.line; $message))
        | .effective = .rest
    );

# The Park-Miller generator: one seed gives the same numbers on any machine.
# Its first numbers follow a small seed closely, so it skips two.
def random_numbers($seed; $count):
    2147483647 as $modulus
    | [
        foreach range($count + 2) as $_ ($seed % ($modulus - 1) + 1;
            . * 48271 % $modulus;
            . / $modulus)
    ]
    | .[2:];

def draw($random):
    (map(.effective) | add // 0) as $total
    | first(
        foreach .[] as $candidate (0;
            . + $candidate.effective;
            select(. > $random * $total) | $candidate)
    ) // null;

def chances:
    (map(.effective) | add) as $total
    | map(.chance = if $total > 0 then .effective / $total else 0 end);

def speaker_for($hook; $speakers; $numbers):
    ($speakers | draw($numbers[1])) as $drawn
    | ($drawn != null and $numbers[2] < $drawn.speaker_rate) as $kept
    | if any($speakers[]; .entry == $hook.entry) then $hook.entry
      elif $kept then $drawn.entry
      else "none"
      end;

def rounded: . * 100 | round / 100;

def shown: if type == "number" then rounded else . end;

def table($columns):
    ($columns | @tsv),
    (.[] | . as $row | [$columns[] | $row[.] | shown] | @tsv);

def hook_columns:
    ["draw", "chance", "effective", "weight", "score", "rest", "entry"];

def line_columns: ["chance", "rest", "line"];

def hook_chances($hooks; $speakers):
    ($hooks | chances | map(.draw = "hook"))
    + ($speakers | chances | map(.chance *= .speaker_rate | .draw = "speaker"))
    | table(hook_columns);

def hook_pick($hooks; $speakers; $flags):
    random_numbers($flags.seed | tonumber; 3) as $numbers
    | ($hooks | draw($numbers[0])) as $hook
    | if $hook == null
      then error("no hook fits \($flags.occasions), and every entry has a when")
      else
          "hook: \($hook.entry)",
          "speaker: \(speaker_for($hook; $speakers; $numbers))"
      end;

def fallback_note($fallback; $flags):
    if $fallback
    then "fallback: no hook fits \($flags.occasions);"
        + " drew from the entries without when"
    else empty
    end;

def hook($files; $flags):
    ($files[0] | checked_options) as $options
    | message($files[1]; $flags) as $message
    | hooks_for($options; $message) as $hooks
    | speakers_for($options; $message) as $speakers
    | if $flags.chances then hook_chances($hooks.candidates; $speakers)
      else hook_pick($hooks.candidates; $speakers; $flags)
      end,
      fallback_note($hooks.fallback; $flags);

def line_chances($lines):
    $lines | chances | table(line_columns);

def line_pick($lines; $flags):
    ($lines | draw(random_numbers($flags.seed | tonumber; 1)[0])) as $drawn
    | if $drawn == null then "line: none"
      else "line: \($drawn.line)", ($drawn.bend // empty | "bend: \(.)")
      end;

def line($files; $flags):
    ($files[0] | checked_options) as $options
    | message($files[1]; $flags) as $message
    | ($flags.hook | split("/")) as [$kind, $slug]
    | ($options.pools[$kind].entries
        | listed($slug; "\($flags.hook) isn't in the options file")) as $option
    | ($files[2][$kind]
        | listed($slug; "\($flags.hook) isn't in the entry file")) as $entry
    | line_candidates($entry; $option.line_half_life_days; $message) as $lines
    | if $flags.chances then line_chances($lines)
      else line_pick($lines; $flags)
      end;

def report(answer):
    try answer catch ("Picker FAILED: \(.)\n" | halt_error(1));
