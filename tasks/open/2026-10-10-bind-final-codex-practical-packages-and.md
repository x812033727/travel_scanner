---
id: 2026-10-10-bind-final-codex-practical-packages-and
title: Bind final Codex practical packages and pilot delivery evidence
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-practical-delivery
claimed_at: 2026-10-10T18:22:02Z
created_at: 2026-10-10T18:21:23Z
completed_at:
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - docs/videos/codex-practical-series/README.md
  - docs/videos/codex-practical-series/STATUS.md
  - docs/videos/codex-practical-series/VALIDATION.md
  - docs/videos/codex-practical-series/evidence
---

# Bind final Codex practical packages and pilot delivery evidence

## Why

首批獨立跟做修正會產生新版教材與媒體；交付索引必須指到真正的最新版，並把技術測試、原生App素材、學習驗收與發布狀態分開，避免讀者使用歷史包。

## Definition of done

- [ ] 最新18教材ZIP的manifest與兩次重建hash一致，README與validation指向同一版本。
- [ ] 第01課CLI稿件、音訊、畫面、字幕／成片或未通過關卡有來源綁定與明確狀態。
- [ ] App待拍、站主跟做、上傳／公開及已知Windows檢查問題保留可接續紀錄。

## Steps

- [ ] 從本次follow-along修正讀回最新build與測試收據，再更新索引。
- [ ] 核對本機媒體與review-pull的hash，不從單一成功exit推斷其他關卡。
- [ ] 最終stage canonical LF，檢查任務與diff，隨draft PR結案；不合併／部署。

## How to verify

核對evidence/packages.json與實際18ZIP SHA-256；重建對照及course／source／docs-videos輸出見VALIDATION。媒體看本片PRODUCTION-STATE與evidence/lesson-01-media.json；再跑 `node tools/tasks.mjs check`、`git diff --cached --check`。

## Notes

2026-10-11：主課程規格已結案，後續ZIP根目錄／提示檔位置修正由各自窄scope票處理。本票只收束交付索引及證據，不修改已凍結教材邏輯。原生App API目前不可用，不能以CLI或Edge網站素材替代。draft PR保留審查，不開auto-merge或執行YouTube發布。
