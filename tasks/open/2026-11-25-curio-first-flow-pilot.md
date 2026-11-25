---
id: 2026-11-25-curio-first-flow-pilot
title: Produce the first Google Flow hybrid-animated long episode for Curio Archive using the 2026-11-25 rules
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-25T01:16:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/explainer-series/FLOW-PRODUCTION-RULES.md
  - docs/videos/history-curiosity/CURIO-FLOW-CHECKLIST.md
---

# Produce the first Google Flow hybrid-animated long episode for 《奇聞檔案局》

## Why

Following the successful pilot of《原來如此事務所》P02 (`sothatswhy-p02-cloud-rain-flow`, 39 Flow
clips, 468 credits, 0 retakes, independent blind QA 9.03/10, 9 languages + Drive SHA-256 archive +
0 GitHub commits), the owner approved adopting the shared Flow rules for《奇聞檔案局》once P02
wraps up.

## Definition of done

- [ ] Select one high-potential《奇聞檔案局》episode with the owner and complete full-video
      3-reader blind script audit (all 3 >= 8.5, 0 problems) + `cli.mjs lint --file` (0 errors/warnings).
- [ ] Execute per `docs/videos/history-curiosity/CURIO-FLOW-CHECKLIST.md`:
      - 3.5-head `ada-canon-v2.png` + 70-yr-deceased historical char sheet in isolated Character Flow
        project; unmanned historical/artifact scenes (45%–65%) in isolated Unmanned project.
      - Archive two reusable text-free seal outros (`curio-outro-closed` & `curio-outro-open`) to
        `AI劇/奇聞檔案局/_共用/製作檔/`.
      - 40–48 Flow clips (<= 550–600 credits), single narrator Gemini `Sulafat` + 8-language pure
        MiniMax Voice-1 dubs, CPS anomaly audit, dual `loudnorm` + `ebur128` `-14 LUFS` check,
        9-language `heimao-left` thumbnails with right-side emblem/artifact.
- [ ] Pass independent 6-dimension blind master QA (each >= 7.5, avg >= 8.0, 0 blockers).
- [ ] Archive all production assets + `腳本定稿/` to Google Drive (`AI劇/奇聞檔案局/<分類>/<代碼>/製作檔/<slug>/`)
      with `SHA256SUMS` 0-difference verification (0 GitHub commits for episode script/media) and
      import to `/admin/videos` via `cli.mjs import`.
