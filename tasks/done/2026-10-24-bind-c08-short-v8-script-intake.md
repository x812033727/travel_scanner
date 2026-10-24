---
id: 2026-10-24-bind-c08-short-v8-script-intake
title: Bind approved C08 short-v8 script intake without backend writes
status: done
priority: P1
area: tools
owner: codex-c08-short-script-intake
claimed_at: 2026-10-24T08:26:59Z
created_at: 2026-10-24T08:26:51Z
completed_at: 2026-10-24T08:33:32Z
branch: codex/c08-short-v8-script-intake-20261024
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json
  - docs/videos/brand-stories-everyday-reversals-20261020/reviews/c08-short-v8-script-intake-20261024.md
  - tools/video/review/script-intake.mjs
  - tools/video/review/script-intake.test.mjs
---

# Bind approved C08 short-v8 script intake without backend writes

## Why

C08 的 20 集企劃已採用站主核准的 36 句 short-v8，但後台劇本核准清單和匯入工具仍指舊 84 句。若直接改正式站集數列，進度查詢會改按新 slug 找卡，舊 approved 卡不再計入；必須先把新稿的非付費審稿入口與雜湊守門做完，再安排正式站同列乾跑和新的 pending 卡審核。

## Definition of done

- [x] 本機 dry-run 只讀出 C08 short-v8 36 句及精確核准投影 SHA；舊 84 句檔案與後台歷史卡保留。
- [x] 近似 slug、改稿／改來源、壞章序／ID 和正式站仍是舊 slug 時，工具在任何寫入前拒絕。
- [x] 交接收據記載正式站唯讀現值、同列乾跑與新 pending 卡的安全順序，沒有正式站寫入。

## Steps

- [x] 更新 `approved-scripts.json`，只將 C08 入口改綁 v8 36 句投影。
- [x] 在 `script-intake.mjs` 加精確 C08 slug、雙 SHA、六章條列與 canonical 旁白比對守門；補本機正反測試。
- [x] 由非作者唯讀重核稿件投影與守門；保存驗證和正式站交接收據。

## How to verify

`node tools/video/review/script-intake.mjs --id C08`；`node --test tools/video/review/script-intake.test.mjs`；`npm run check:tasks`；`git diff --check`。不使用 `--apply`。

## Notes

站主核准 C08 v8 原件 SHA `040d9a49...`，頂層投影 SHA `07cc18d1...`；36/36 可見旁白與 canonical `video.json` 同序。主協作者對正式站唯讀 GET：系列 paused、第 8 列舊 slug/planned、舊 84 句卡 approved、新 slug project 404；尚未正式站 import dry-run 或任何寫入。詳見 `docs/videos/brand-stories-everyday-reversals-20261020/reviews/c08-short-v8-script-intake-20261024.md`。

非作者代理對核准原件、投影與當時程式守門給 PASS；後續依其低優先建議追加嚴格條列與新舊卡並存測試。主協作者 `/root` 於 2026-10-24 08:40 UTC 唯讀重核 PR #1823 最終 diff，判無 blocker，獨立重跑 `script-intake.test.mjs` 11／11、`--id C08` 本機 36 句乾跑及 diff check，均 PASS。未進行正式站乾跑。更廣的七份 review test 組合在 Windows 逾 90 秒無結果後中止，不能稱全套通過；CI 須驗最終 head。
