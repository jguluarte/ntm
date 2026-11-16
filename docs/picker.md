# The picker's classes

For one message, the picker reads a theme's options file and the message's type,
such as `evening,slipped`, and draws the option the message is built on, its
hook. It draws twice: a group of options, then an option in that group, each by
a chance that comes from weights and scores. It prints `hook: scenes/dawn` for
`ntm:style`, or, with `--chances`, the chances it draws from.

## The classes

| Class         | What it is                           | What it owns                                                |
| ------------- | ------------------------------------ | ----------------------------------------------------------- |
| `Theme`       | The options file, read and checked   | Its groups, and a lottery of those that can be drawn        |
| `OptionGroup` | A pool whose `roles` include `hook`  | Its weight, score, options, and a lottery of those that fit |
| `Option`      | An entry in a pool, as `scenes/dawn` | Its weight and score, and the types it fits                 |
| `Lottery`     | The candidates for one draw          | Its candidates, their names and chances, and the draw       |
| `MessageType` | A message's type, as `morning,done`  | Its reminder type and task outcomes, and the big-win rule   |
| `Picker`      | One run of the `hook` subcommand     | The theme, message type and seed, and what it prints        |

## One draw, top to bottom

```python
def pick_hook(self):
    with self._reporting_failures():
        generator = random.Random(self.seed)
        group = self.theme.lottery_for(self.message_type).draw(generator)
        option = group.lottery_for(self.message_type).draw(generator)
        return f"hook: {option.name}"
```

The theme's lottery holds each group with a fitting option that weighs more than
0; the first draw picks one. The group's lottery holds its fitting options; the
second draw picks the hook. Both apply the big-win rule: on a big win with no
option kept for it, they draw as for a finished task. `chances_table` prints the
same two lotteries, headed `group`, `option` and `chance in group`.

## What a test reads like

```python
def test_an_entry_fits_only_the_reminder_types_its_type_names(self):
    theme = Theme(fixtures.EVERY_TYPE)
    message_type = MessageType("weekly")
    [scenes] = theme.lottery_for(message_type).candidates
    lottery = scenes.lottery_for(message_type)

    expected = ["scenes/any_time", "scenes/morning_or_weekly"]
    self.assertEqual(expected, lottery.names)


def test_a_type_that_isnt_a_valid_combination_fails_naming_it(self):
    args = make_picker_args(fixtures.EVEN, type="morning,evening")

    with self.assertRaises(SystemExit) as exited:
        Picker.from_args(args)

    why = "more than one reminder type: evening, morning"
    expected = f"Picker FAILED: InvalidMessageType: {why}"
    self.assertEqual(expected, exited.exception.code)
```

## When the picker can't draw

| Name                 | Raised when                               | Message                                         |
| -------------------- | ----------------------------------------- | ----------------------------------------------- |
| `InvalidTheme`       | The file breaks the schema or has no hook | `$.pools: no pool gives a hook`                 |
| `InvalidMessageType` | The type has an unknown word              | `not a reminder type or task outcome: night`    |
|                      | The type has two reminder types           | `more than one reminder type: evening, morning` |
| `MissingOption`      | No option fits, after the big-win rule    | `no option fits morning,big_win`                |
| `MissingWeight`      | Every option that fits weighs 0           | `every option that fits big_win weighs 0`       |

Invalid means an input is wrong. Missing means the inputs are fine, but there is
nothing to draw.

## Words that are the file's

`pools`, `entries`, `roles`, `type`, `weight` and `score` are the options file's
keys: a group is read from a pool, an option from an entry. `hook` is the role
an option is drawn for, as in `roles: [hook, speaker]`, and the `hook`
subcommand and the printed `hook:` line name it.
