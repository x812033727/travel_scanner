---
id: 2026-11-11-curio-pool-wave26
title: 奇聞檔案局素材池第二十六批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round6
claimed_at: 2026-11-11T23:16:10Z
created_at: 2026-11-11T23:16:08Z
completed_at: 2026-11-12T00:14:39Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第二十六批

## Why

站主 2026-11-11：「繼續擴充奇聞跟原來如此素材池」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave26-20261112.json 與 reviews/wave26-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（K1–K4：U、M、P、G 四個最少的軸）先去重再實讀來源。
- [x] 四位非作者覆核（R261–R264）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T120、T121，T37 與 T06 加章）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 874→894；暫緩 N2845、N2865、N2806（只撐得起一章，要接的兄弟題是單集，得先壓短既有單集，等站主決定；站主 2026-11-12 說 N2845、N2865 先暫緩）；待查 N2804、N2846。研究進行中若有人重建素材池，`cli.mjs search` 會回 Index is stale 而不出結果：重建後立刻跑 `cli.mjs index`，不然研究代理只能 grep。語意近鄰要先 `pip install tokenizers onnxruntime numpy`。U 軸的起點題（飛船潮、火星訊號、鬼火箭等）幾乎都已在池裡，下一批 U 要換方向。
