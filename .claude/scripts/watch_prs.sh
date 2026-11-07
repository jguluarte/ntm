#!/bin/bash
# watch_prs.sh <since, ISO 8601 UTC>
# Waits up to 9 minutes for the owner's new comments on any open, non-draft
# pull request in jguluarte/ntm. Prints them under "pr <number>" headers and
# exits; prints "none" when nothing came. The first output line is always
# "next-since: <timestamp>", the value to pass on the next call. Comments an
# agent posted carry the marker below and are skipped.
SINCE=$1
REPO=jguluarte/ntm
OWNER=jguluarte
MARK='<!-- ntm-agent -->'
END=$((SECONDS + 540))
NEXT=$SINCE
KEEP="select(.user.login == \"$OWNER\" and (.body | contains(\"$MARK\") | not))"
while [ $SECONDS -lt $END ]; do
  START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  PRS=$(gh api "repos/$REPO/pulls?state=open" \
    --jq '.[] | select(.draft | not) | .number' 2>/dev/null)
  OUT=""
  for PR in $PRS; do
    ONE=$(
      gh api "repos/$REPO/issues/$PR/comments?since=$SINCE" --jq \
        ".[] | $KEEP | \"conversation comment \(.id) at \(.created_at) \(.html_url)\n\(.body)\n---\"" 2>/dev/null
      gh api "repos/$REPO/pulls/$PR/comments?since=$SINCE" --jq \
        ".[] | $KEEP | \"line comment \(.id) on \(.path):\(.line // .original_line) reply-to \(.in_reply_to_id // \"none\") at \(.created_at) \(.html_url)\n\(.body)\n---\"" 2>/dev/null
      gh api "repos/$REPO/pulls/$PR/reviews" --jq \
        ".[] | select(.user.login == \"$OWNER\" and .submitted_at > \"$SINCE\" and .body != \"\" and (.body | contains(\"$MARK\") | not)) | \"review \(.id) \(.state) at \(.submitted_at) \(.html_url)\n\(.body)\n---\"" 2>/dev/null
    )
    if [ -n "$ONE" ]; then
      OUT="$OUT"$'\n'"pr $PR"$'\n'"$ONE"
    fi
  done
  NEXT=$START
  if [ -n "$OUT" ]; then
    echo "next-since: $NEXT"
    echo "$OUT"
    exit 0
  fi
  sleep 60
done
echo "next-since: $NEXT"
echo none
