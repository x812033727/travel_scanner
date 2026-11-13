---
id: 2026-11-12-curio-pool-wave32
title: 奇聞檔案局素材池第三十二批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round12
claimed_at: 2026-11-12T06:03:39Z
created_at: 2026-11-12T06:03:38Z
completed_at: 2026-11-12T06:53:32Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十二批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave32-20261112.json 與 reviews/wave32-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（Y1–Y4：U 古代外星器物、G 清代筆記裡被揭穿的鬼、P 當眾考驗的日月食預報、M 火山目擊紀錄）先去重再實讀來源。
- [x] 四位非作者覆核（R321–R324）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T130）、更新 selection 與 README，跑語意近鄰；順手把 wave27–31 批次說明的覆核連結改指各自的檔。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 994→1008；待查 N3284、N3285（各 6–8 分鐘 chapter，分別建議接 N142、M27）、N3342（缺 Tedeschi 1669 年報告）。這一批仍有三次拼網址（兩位研究代理、一位覆核者），都已從公開連結重讀或未使用，記在覆核紀錄 rule1_record。江戶時代的鬼故事原文（耳嚢、甲子夜話）在國文研與 archive.org 都讀不到，之後要找 G 軸日本題得先找可讀的翻刻本。
