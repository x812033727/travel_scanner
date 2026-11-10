---
id: 2026-10-20-curio-s57-r3-author
title: Repair S57 R2 narrative blind holds
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T23:03:24Z
created_at: 2026-10-20T23:03:21Z
completed_at: 2026-10-20T23:10:49Z
branch:
depends_on:
  - 2026-10-20-s57-r2-formal-narrative-merge-and
scope:
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/review/r3-author-fix.md
  - docs/videos/curio-s57/review/r3-author-diff.patch
---

# Repair S57 R2 narrative blind holds

## Why

S57 R2 正式雙盲敘事合併只有 9／13，四個必答題 HOLD：章末問題未由下章首句回答、兩個問句欠有來源的 payoff、湖行同義重述，以及五句物資清單打斷主線。原票另提醒開場過早說出分路與第七章名不像事件。完整依據見 `docs/videos/curio-s57/review/r2-merge/summary.md`。

## Definition of done

- [x] R3 讓各敘事問題有可核的直接承接，壓縮物資段並保留史料層級與 189 句主張對齊。
- [x] 凍結五份創作檔 SHA-256、完整 R2→R3 差異與作者修訂紀錄，交新一輪獨立覆核。
- [x] 保持 30–60 秒濃縮開場、至少 8 分鐘正文、5 秒片頭與 21 秒片尾規格，不自批 PASS 或執行付費媒體。

## Steps

- [x] 窄修四個共同 NO，並修 B 票開場／第七章名建議。
- [x] 同步改 `video.json`、`claims.md`、`brief.md`，重產 `script.md`。
- [x] 執行 lint、文件影片測試、任務板檢查與逐 ID 對齊，再凍結五檔 SHA。
- [x] 將凍結版通知主代理供新獨立史料與雙盲敘事重審。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s57 --json`：0 errors／0 warnings，189 句；`npm run test:docs-videos`：236 pass／0 fail；`npm run check:tasks`：exit 0，只有既有無關警告。Python 對讀 `claims.md` 與 `video.json`：189／189 同句；開場 45 秒，正文 2,697 漢字、按每分鐘 325 字約 8.30 分鐘。五檔 SHA-256 及完整差異見 `docs/videos/curio-s57/review/r3-author-fix.md` 與 `r3-author-diff.patch`。

## Notes

作者只更動 23 句口播、24 個場景 ID（含一個僅改章名）、14 個鏡頭提示詞、兩個章名與一個 loop payoff。新稿仍須 R3 史料／書面畫面獨立覆核及兩位新讀者盲評；不得沿用 R2 的來源 PASS 或 R2 舊讀者票核准 R3。
