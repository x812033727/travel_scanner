---
id: 2026-10-24-c20-zippo-v5r2-visual-review
title: Resolve C20 Zippo script and visual blind-review holds
status: done
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T02:56:27Z
created_at: 2026-10-24T02:55:46Z
completed_at: 2026-10-24T06:59:53Z
branch: codex/c20-zippo-v5r2-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20
---

# Resolve C20 Zippo script and visual blind-review holds

## Why

C20 v5r2 已刪英國寄件路線，v5r3 已刪日期碼支線。v5r3 的獨立來源／配鏡覆核通過，但兩份新版盲讀均指出修理段落重複，第二位也指出 Double Arc 產品支線。v5r4 直接剪去 17 句，讓專利、英國送修、美國保證及結論相接；此版須重新獨立審查，且紙上正文低於 480 秒，製作時長關卡維持 HOLD。

## Definition of done

- [x] v5r4 的 42 句與 42 鏡逐項對齊；現行旁白沒有日期碼或 Double Arc 段落，舊版投影與審查鎖定保留作歷史證據。
- [x] 非作者逐句來源／配鏡覆核綁定新版確切檔案雜湊；兩位只讀旁白讀者各自在讀其他材料前鎖定 13 題判定。A 的 `no_toc=No`、B 的 12 題皆 Yes；沒有共同否決題。
- [x] 已在草稿 PR #1808 寫明 PASS／HOLD、低於 480 秒的紙上時長，以及未完成的站主劇本核准、付費、實測配音、匯入及上架界線，沒有冒稱本機試片完成。

## Steps

- [x] 沿用既有 v5r2 本機修稿；不重寫已改過的 59 句。
- [x] `c200401` 文字分鏡與 JSON 同步縮小到日期碼，重算視覺檔雜湊；旁白投影保留原 SHA。
- [x] 鎖定 v5r2 獨立來源／配鏡 PASS 與兩份 `no_detour=No` 盲讀，沒有將任何舊結論轉移到 v5r3。
- [x] v5r3 改九句及其配鏡，重生純旁白投影；59/59 機械配對與紙上正文 2,180 單位已核對。
- [x] v5r3 獨立來源／配鏡覆核已 PASS；兩份盲讀均判 `no_recap=No`，其中一份也判 `no_detour=No`，舊結論不轉移。
- [x] v5r4 刪除 17 個指定 ID、重分六章、重生投影；42/42 機械配對通過，紙上正文 1,431 單位記為時長 HOLD。
- [x] v5r4 獨立來源／配鏡 42／42 PASS；兩位獨立旁白盲讀均已鎖定，沒有共同否決題，但 A 保留 `no_toc=No` 的剪輯提醒。製作時長 HOLD 不由盲讀解除。
- [x] 跑機械配對、`npm run check:tasks` 與 `git diff --check`。
- [x] 推送草稿 PR #1808；目前製作時長 HOLD，暫不提站主核稿或付費。

## How to verify

- `Get-FileHash` 核對 v5r4 作者五檔與旁白投影；機械比對 42 個 ID、原文、來源標籤、畫面類型、MD／JSON 提示詞。
- 逐項讀原發行者來源，查核鉸鏈、外觀、內膽及各地維修條款的歸屬；獨立查核收據須記錄 HOLD。
- 兩份新盲讀只開 `reviews/narration-v5r4-only.txt`，SHA-256 `F98F3D6E84CCF831FFBBF5BCED3712283F0ABC3558B8444FC982C835098F2225`，13 題各有 ID 與句子依據。v5r2／v5r3 投影及鎖定保留，不能沿用其結論。
- `npm run check:tasks`、`git diff --check` 與草稿 PR CI。

## Notes

- 舊分支曾重現已在主分支移除的廣範圍保全任務，造成 claim 衝突；先將 C20 分支變基到最新 `origin/main`，再以本票正常 claim，沒有使用 `--force`。
- v5r4 正文 1,431 個 UTF-16 紙上單位約 343.4 秒，只是估算，距 480 秒紙上門檻約差 136.6 秒；不得灌水補長。實際正文配音、插圖時間占比均未量測。站主目前只採用 C20 企劃，未核准 v5r4 劇本或付費試片。
- v5r4 作者收據已更正 `visual-plan.md` 過期頁尾為 42／38／4；非作者以更正後 SHA-256 `2B8381352032E3001D1C4DB04505D2CBB80285EE6FEF8E743ACB00B2062BDAAF` 重新覆核。詳見 `reviews/source-visual-v5r4-20261024.md` 與兩份 `blind-v5r4-reader-*-lock.md`。
