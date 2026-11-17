from pathlib import Path

SCORING = Path(__file__).parent
OPTIONS = SCORING / "Scoring-options.yaml"
MESSAGE_HISTORY = SCORING / "Scoring-message-history.jsonl"
BLANK_MESSAGE_HISTORY = SCORING / "Blank-message-history.jsonl"
MESSAGE_HISTORY_WITHOUT_PICKS = SCORING / "Without-picks-message-history.jsonl"
MESSAGE_HISTORY_NOT_THERE = SCORING / "Not-there-message-history.jsonl"
