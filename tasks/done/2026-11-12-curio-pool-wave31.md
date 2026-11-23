---
id: 2026-11-12-curio-pool-wave31
title: 奇聞檔案局素材池第三十一批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round11
claimed_at: 2026-11-12T05:01:24Z
created_at: 2026-11-12T05:01:22Z
completed_at: 2026-11-12T05:54:37Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十一批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave31-20261112.json 與 reviews/wave31-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（X1–X4：U 實驗室物證、G 臺灣與華南鬼故事、M 化石被讀成怪物、L 只存在紙上的東西）先去重再實讀來源。
- [x] 四位非作者覆核（R311–R314）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T129）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 981→994；暫緩 N3224（要站主同意把 N409 從 Shorts 改回長片）、N3243、N3265（現存信仰界線）；待查 N3203、N3204、N3223、N3246。規定放到說明檔開頭後，仍有兩次拼網址（一次 404 未用；一次隨即從搜尋結果重讀，以搜尋結果為準）。素材池 CLI 搜尋這一批對 grep 找得到的詞也回空，研究與覆核都只靠 grep。
