---
id: 2026-11-12-curio-pool-wave30
title: 奇聞檔案局素材池第三十批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round10
claimed_at: 2026-11-12T03:29:42Z
created_at: 2026-11-12T03:29:40Z
completed_at: 2026-11-12T04:30:52Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第三十批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave30-20261112.json 與 reviews/wave30-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（W1–W4：U 著名 UFO 照片、名篇鬼故事的更早文本、P「這不可能」的名言、M 水的怪現象）先去重再實讀來源。
- [x] 四位非作者覆核（R301–R304）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T128）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 960→981；暫緩 N3125（只夠一章，要接 N981）。名篇鬼故事那 5 題覆核改放 F 軸。說明檔寫了「不得猜測網址」後，仍有一位研究代理試過一個推出來的網址（404，未當來源）：下一輪把這條移到說明檔開頭。
