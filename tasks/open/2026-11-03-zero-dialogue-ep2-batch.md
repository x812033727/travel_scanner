---
id: 2026-11-03-zero-dialogue-ep2-batch
title: 零台詞四系列第 2 集（新髮型、吊燈、雪國、年度簡報）：產線與成片
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T15:34:37Z
created_at: 2026-11-03T15:34:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/wangjia-couple-e02
  - docs/videos/raccoon-mischief-e02
  - docs/videos/influencer-piglet-e02
  - docs/videos/shechu-hell-e02
  - docs/videos/zero-dialogue-series-ideas/production
---

# 零台詞四系列第 2 集（新髮型、吊燈、雪國、年度簡報）：產線與成片

## Why

站主 2026-11-03：四個系列的 EP1 做完後，每個系列繼續做下一集；照推薦直接決定、依序做完。

## Definition of done

- [x] 四集的 `video.json`、`brief.md`（lint 0 錯誤），由 `docs/videos/zero-dialogue-series-ideas/production/make_episode.py` 從各集 spec 產生。
- [ ] Colab 首格、H3 直式片段（`run_episode.sh`：一張一張跑、每張逾時強制重試）。
- [ ] 剪接成片（`edit.py`）、站主看過。

## How to verify

```bash
for s in wangjia-couple-e02 raccoon-mischief-e02 influencer-piglet-e02 shechu-hell-e02; do node tools/video/cli.mjs lint --file docs/videos/$s/video.json; done
```

## Notes

- 配樂沿用各系列 EP1 的那首（同系列聽起來一致，也不用再付）；音效沿用 EP1 的，加上每集 spec 的 `sfx_extra`（ffmpeg 合成）。
- 每一鏡一個主角，笑點那一格寫成角色本身在做（EP1 的教訓）。
