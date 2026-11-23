#!/usr/bin/env bash
# Retired on 2026-11-10: video backups no longer go to git branches. The owner: every file of a
# production goes to Google Drive, AI劇/<名稱>/<集數>/製作檔/, copied by the session that made it.
# Use docs/videos/ai-drama-drive/todrive.sh (docs/videos/AI-DRAMA-DRIVE.md). The old script is in
# the git history of this file.
cat >&2 <<'MSG'
tobranch.sh: retired 2026-11-10 — video backups go to Google Drive, not to branches.
  use:   docs/videos/ai-drama-drive/todrive.sh <工作資料夾> "videobackup:AI劇/<名稱>/<集數>/製作檔/<工作資料夾名>"
  rules: docs/videos/AI-DRAMA-DRIVE.md
MSG
exit 2
