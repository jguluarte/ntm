# The picker

The picker draws a theme's picks, each a perspective and a reference, from its
options file, and works out the numbers it draws by.
`references/theme-files.md`, at the plugin's root, describes that file. It needs
Python 3 with PyYAML and jsonschema.

```
python3 pick_list.py draw --options <file> --count <number> [--seed <number>]
python3 recalculate.py start --options <file> <entry file>...
python3 recalculate.py adjust --options <file> --history <file> --since <date>
```

`draw` prints that many picks as a YAML list, in the order drawn, each item a
`perspective:` and a `reference:`. The same `--seed` draws the same picks.

`start` gives a new theme its first weights, speaker rate and checksums.
`adjust` moves the scores of each message's picks by its `verdict` and
`feedback`, for the history's lines sent on or after `--since`. Both print
`saved: <file>`.

A failure prints one `Picker FAILED:` or `Recalculation FAILED:` line on stderr
and exits 1.

`python3 picker.py pick --options <file> [--seed <number>]` prints one pick;
with `--chances`, each perspective's weight, score and chance instead.
