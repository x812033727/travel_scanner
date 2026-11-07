#!/usr/bin/env bash
# bk-files.sh BRANCH : like bk-media.sh, but backs up exactly the files listed NUL-separated on stdin (paths under ~/mokaair-work/videos)
# on transfer/BRANCH, built in a throwaway bare repo that is deleted after the push. Files over 95 MB are split.
set -u
BR=$1; shift
V=$HOME/mokaair-work/videos
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad
G=$S/bk-$BR.git
rm -rf "${G:?}"; git init -q --bare "$G"
export GIT_DIR=$G
idx=$G/index; export GIT_INDEX_FILE=$idx
n=0; bytes=0; parts=0
LIST=$(mktemp); cat > "$LIST"; for d in once; do
  while IFS= read -r -d '' f; do
    rel=${f#$V/}
    sz=$(stat -c %s "$f")
    if [ "$sz" -gt 95000000 ]; then
      tmp=$S/bk-split; mkdir -p "$tmp"; rm -f "${tmp:?}"/*
      split -b 90m -d -a 2 "$f" "$tmp/p"
      for p in "$tmp"/p*; do
        h=$(git hash-object -w "$p"); printf '100644 %s\t%s\n' "$h" "$rel.part${p##*/p}" | git update-index --add --index-info
        parts=$((parts+1))
      done
      rm -f "${tmp:?}"/*
    else
      h=$(git hash-object -w "$f"); printf '100644 %s\t%s\n' "$h" "$rel" | git update-index --add --index-info
    fi
    n=$((n+1)); bytes=$((bytes+sz))
  done < "$LIST"
done
readme=$(mktemp)
cat > "$readme" <<EOF
# 種田娶妻打天下 work-folder backup: $*

Made $(date -u +%F) from ~/mokaair-work/videos. $n files, $((bytes/1000000)) MB.
Restore: copy each folder back to ~/mokaair-work/videos/. A file named X.part00, X.part01 ... is one file over 95 MB
split for GitHub: \`cat X.part* > X\`.
Left out (the tools rebuild them free): clips/ (stage-clips.sh), segments-v4/ (dub.sh), review/, cut/*.mp4 (asm.sh;
the published cut is also on the site).
EOF
h=$(git hash-object -w "$readme"); printf '100644 %s\t%s\n' "$h" "README-backup.md" | git update-index --add --index-info; rm -f "$readme"
T=$(git write-tree)
C=$(printf 'zhong-tian work-folder backup %s: %s\n\n%s files, %s MB, %s split parts.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018EYovKNmSMKVnfFFMhZJH2\n' "$(date -u +%F)" "$*" "$n" "$((bytes/1000000))" "$parts" | git commit-tree "$T")
ok=0
for w in 2 4 8 16 0; do
  if git push -q https://github.com/x812033727/travel_scanner "$C:refs/heads/transfer/$BR" 2>&1; then ok=1; break; fi
  [ "$w" = 0 ] || sleep "$w"
done
got=$(git ls-remote https://github.com/x812033727/travel_scanner "refs/heads/transfer/$BR" | cut -f1)
unset GIT_DIR GIT_INDEX_FILE
rm -rf "${G:?}"
if [ "$ok" = 1 ] && [ "$got" = "$C" ]; then echo "OK transfer/$BR $C $n files $((bytes/1000000)) MB parts=$parts"; else echo "FAIL transfer/$BR (pushed=$ok remote=$got local=$C)"; fi
