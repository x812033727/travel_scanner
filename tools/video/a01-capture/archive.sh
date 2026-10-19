#!/usr/bin/env bash
# Sent over plink stdin; stdout is a binary tar stream, never terminal text.
set -euo pipefail
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml --profile video exec -T video-worker bash -se <<'WORKER'
set -euo pipefail
slug=story-rolling-suitcase-v2
work=/var/lib/mokaair/video-work
docs=/opt/mokaair
audit="$work/$slug/story/recheck-audit"
lexicon="$docs/docs/videos/$slug/story-lexicon"
reject_linked_ancestors() {
  local path="$1"
  while [[ "$path" != / ]]; do
    if [[ -L "$path" ]]; then
      printf 'linked capture source path: %s\n' "$path" >&2
      return 1
    fi
    path="${path%/*}"
    [[ -n "$path" ]] || path=/
  done
}
reject_linked_ancestors "$audit"
reject_linked_ancestors "$lexicon"
test -d "$audit"
test ! -L "$audit"
test -z "$(find "$audit" -type l -print -quit)"
test -z "$(find "$audit" -type f ! -name '*.json' -print -quit)"
test -z "$(find "$audit" ! -type d ! -type f -print -quit)"
count=$(find "$audit" -mindepth 1 -maxdepth 1 -type d | wc -l)
test "$count" -ge 104
test -d "$lexicon"
test ! -L "$lexicon"
test -f "$lexicon/current.json"
test ! -L "$lexicon/current.json"
test -d "$lexicon/events"
test -d "$lexicon/versions"
test ! -L "$lexicon/events"
test ! -L "$lexicon/versions"
test -z "$(find "$lexicon" -type l -print -quit)"
test -z "$(find "$lexicon" ! -type d ! -type f -print -quit)"
test -z "$(find "$lexicon" -type f ! -name '*.json' -print -quit)"
docs_files=("docs/videos/lexicon.json" "docs/videos/$slug/video.json"
  "docs/videos/$slug/series.json" "docs/videos/$slug/claims.md"
  "docs/videos/$slug/script.md" "docs/videos/$slug/story-lexicon")
if test -f "$docs/docs/videos/$slug/verify-1.md"; then
  docs_files+=("docs/videos/$slug/verify-1.md")
fi
work_files=("$slug/auto.json" "$slug/review/narrative.json"
  "$slug/story/recheck-audit")
for chapter in hook origin idea engine turn now; do
  work_files+=("$slug/story/chapters/$chapter.json")
done
if test -f "$work/$slug/story/reviews/script-review.json"; then
  work_files+=("$slug/story/reviews/script-review.json")
fi
for file in "${docs_files[@]}"; do
  reject_linked_ancestors "$docs/$file"
  if [[ "$file" == "docs/videos/$slug/story-lexicon" ]]; then
    test -d "$docs/$file"
  else
    test -f "$docs/$file"
  fi
  test ! -L "$docs/$file"
done
for file in "${work_files[@]}"; do
  reject_linked_ancestors "$work/$file"
  test -e "$work/$file" && test ! -L "$work/$file"
done
receipts=()
if test -d "$work/$slug/manual-revisions"; then
  reject_linked_ancestors "$work/$slug/manual-revisions"
  test -z "$(find "$work/$slug/manual-revisions" -type l -print -quit)"
  while IFS= read -r -d '' receipt; do receipts+=("$receipt"); done < <(
    find "$work/$slug/manual-revisions" -mindepth 2 -maxdepth 2 -type f \
      -name installation-receipt.json -printf "$slug/manual-revisions/%P\0")
fi
tar -cf - -C "$docs" "${docs_files[@]}" -C "$work" "${work_files[@]}" "${receipts[@]}"
WORKER
