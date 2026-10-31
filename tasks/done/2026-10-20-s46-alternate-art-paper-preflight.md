---
id: 2026-10-20-s46-alternate-art-paper-preflight
title: Independently preflight S46 alternate three-scene art pilot
status: done
priority: P2
area: docs
owner: codex-s46-art-preflight
claimed_at: 2026-10-20T22:45:06Z
created_at: 2026-10-20T22:45:03Z
completed_at: 2026-10-20T22:46:25Z
branch: codex/curio-preproduction-s46-s56-20261020
depends_on: []
scope:
  - docs/videos/curio-s46/review/r14-alternate-art-paper-preflight.md
---

# Independently preflight S46 alternate three-scene art pilot

## Why

S46 R14 的兩輪三景原圖只有 1/3 KEEP，舊付費插圖方案已 STOP。額度恢復前先獨立核兩句新候選提示詞的史料邊界、可檢查畫面和整集累計花費，避免直接重跑舊方案。

## Definition of done

- [x] 書面預檢記錄來源、兩個主物件的原圖必要條件、新三景停損與含既花費用的整集上限；明示尚未買新圖或解除 STOP。

## Steps

- [x] 對固定 Blackwell 自傳 P06/P13、claims、兩輪原圖收據及實際第二輪三張 1280×720 JPG。
- [x] 計算 110 景、既花 US$0.081、可能重新付費圖像與配樂的累計上限，寫出新版 3/3 小樣規則。

## How to verify

`sha256sum docs/videos/curio-s46/{claims.md,video.json,script.md}`、`sha256sum /workspace/.video-work/curio-s46/keyframes/bkw00{2,6,7}-1.jpg /workspace/.video-work/curio-s46/media/ledger.json`；`git diff --check`、`npm run check:tasks`。所有結論見 [書面預檢](../../docs/videos/curio-s46/review/r14-alternate-art-paper-preflight.md)。

## Notes

舊圖 `bkw006` 精確 prompt 未動，可按相同 SHA 重新核後沿用；`bkw002` 的封口信封與 `bkw007` 接在床頭的卡片各須真正 PASS，故新版先期門檻訂 3/3。這是文字方案，尚未寫入 `video.json`、動用圖片／judge／音樂額度或取得站台核准。新圖評審與配樂月額度現皆 0，預期 UTC 2026-11-01 重置後仍要現查。新精確版上限**提案**累計 US$4.62，原版 US$4.54 不自動移轉。
