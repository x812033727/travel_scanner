---
id: 2026-11-19-curio-pool-drop-the-13-minute
title: Curio pool: drop the 13-minute upper bound on long episodes
status: review
priority: P2
area: tools
owner: claude-fable-5-2
claimed_at: 2026-11-19T11:27:49Z
created_at: 2026-11-19T11:27:42Z
completed_at:
branch: claude/curio-pool-no-13-minute-cap
depends_on: []
scope:
  - tools/video/curio/pool
  - docs/videos/history-curiosity/pool
  - docs/videos/history-curiosity/README.md
  - apps/api/app/video_pools/data/pools.json
---

# Curio pool: drop the 13-minute upper bound on long episodes

## Why

站主 2026-11-19 更正奇聞檔案局的片長規則：「我是 8 分鐘以上而已，沒有一定要限制在 13 分鐘內」。
curio-episode skill 已在 PR #2180 改成「至少 8 分鐘、沒有上限」，但題庫工具
（`tools/video/curio/pool`）還寫死 `LONG_MAX = 13`：題卡的 `editorial.minutes` 超過 13 會丟錯，
題案的 `range_minutes` 上緣超過 13 也會被 `validateThemes` 擋下，產出的說明文字寫「8–13 分鐘」。

## Definition of done

- [x] 題案與題卡的片長只檢查下限 8 分鐘；14 分鐘以上的題案不再被擋，7 分鐘仍被擋。
- [x] 工具產出的說明文字與手寫的規則段落改成「至少 8 分鐘，看素材決定，不硬湊」。
- [x] 重產的文件除了那句說明與輸入檔雜湊以外沒有差異。

## Steps

- [x] `core.mjs` 拿掉 `LONG_MAX`，`validateEditorial` 只檢查正數與 lo ≤ hi。
- [x] `render.mjs` 的 `validateThemes`、THEMES.md 與 PRODUCIBLE.html 的說明文字。
- [x] `pool.test.mjs`：7 分鐘丟錯、14 與 20 分鐘通過。
- [x] `node tools/video/curio/pool/cli.mjs build` 重產。
- [x] 手寫文件：`pool/README.md`、`pool/VALIDATION.md`、系列 `README.md` 的〈長度（更新）〉。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs
node tools/video/curio/pool/cli.mjs check
npm run test:tools && npm run check:tasks
```

## Notes

- build 在這台機器要 5 分鐘以上，放背景跑。
- 重產後的差異：`THEMES.md` 與 `PRODUCIBLE.html` 各一句說明；`pool.json` 的 `inputs` 有 11 個雜湊變了
  （兩個工具檔，加上 9 個 `curio-*/video.json`，那 9 個是 main 上先前的 PR 改過但沒有重跑 build 留下的），
  題目內容與 `revision` 沒變，所以 `index.html`、`QUESTIONS.md` 等沒有差異；`manifest.json` 與後台資料包
  `apps/api/app/video_pools/data/pools.json` 的雜湊跟著變。
- 沒有動的地方：批次檔、覆核、`DEDUP.md`、`dedup-decisions.json` 與 `themes.json` 裡寫「超過 13 分鐘」的
  判斷是照當時規則留下的紀錄。其中因為超過 13 分鐘才暫緩、退回或轉 Shorts 的題，以及題案撤案條件裡
  「合計不得超過 13 分鐘」，要不要重新評估是編輯決定，這張票沒有處理。
- 品牌故事（`story-`）的 13 分鐘是站主另外定的，沒有動。
