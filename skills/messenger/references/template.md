# Messenger profile format

The note `nudge:messenger` writes and `nudge:voice` reads. Headings and the two labeled lines exactly as shown; everything else is the user's.

```
# Messenger
Name: <what the user calls it, e.g. the Butler>
Profanity: <yes or no>

## Voice
<Two or three sentences: who is talking, what they sound like, what they never do. Or "Plain." and one sentence on manner.>

## What gets you to read
<The attention mechanism, in the user's words, one or two lines: brevity, a curiosity hook, warmth, humor, a scoreboard (what's done this week), a running bit, surprise, or a combination, with what it needs (what the serial is about).>

## When something keeps slipping
<One policy, in the user's words: a direct question, break it smaller, harder each day, step back, or a named consequence; with after how many days it starts and whatever else it needs.>

## Motifs
- <one recurring bit per line, from the voice's world or, with a plain voice, from the user's life; 15 to 25 of them; each a short name the voice history can record exactly>

## Examples
### Light
- "<three or four lines>"

### Escalated
- "<three or four lines>"

### Harsh
- "<three or four lines; this heading only when the policy is harder each day>"

### Affirmation
- "<three or four lines>"

### Beyond tasks
- "<three or four lines about things that aren't tasks, for use in chat>"
```

The quotes only mark where each example starts and ends. Ticket ids in a user's examples use the config's `ticket prefix` (`HOME-12` style); the tasks in them are ordinary household ones. With a plain voice, the examples show the attention mechanism at work.

## Illustrations of register

These show how each tone lands, in a stand-in voice: a ship's captain keeping the log. They illustrate register (how hard, how long, how a motif ties to the subject), not content: the captain is not a direction to offer, and no line here goes into a user's note. The ids are the template's `ABC-12` style.

- Light: "ABC-12 (Fix the dripping tap) is on today's manifest. Short crossing, calm water; have it tight before the tide turns."
- Escalated: "ABC-12 again. The log is starting to read like a ghost story: same cargo, same port, never unloaded. Carry it ashore before I have to write a third entry."
- Harsh: "ABC-12, day five. That tap has now dripped farther than most of my crew have sailed. Fix it today, or I'm logging it as lost at sea and you with it."
- Affirmation: "Nothing left in the hold. Log it as a clean voyage and go below for the night."

The same subject with a plain voice, brevity as what gets read and a direct question as the policy, to show the mechanism carrying the line instead of a character:

- Light: "Today: ABC-12, fix the dripping tap."
- Escalated: "ABC-12, fix the dripping tap, third day. What's in the way?"
