---
id: 2026-11-03-zero-dialogue-ep2-batch
title: 零台詞四系列第 2–5 集（共 16 集）：產線與成片
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
  - docs/videos/wangjia-couple-e03
  - docs/videos/wangjia-couple-e04
  - docs/videos/wangjia-couple-e05
  - docs/videos/raccoon-mischief-e03
  - docs/videos/raccoon-mischief-e04
  - docs/videos/raccoon-mischief-e05
  - docs/videos/influencer-piglet-e03
  - docs/videos/influencer-piglet-e04
  - docs/videos/influencer-piglet-e05
  - docs/videos/shechu-hell-e03
  - docs/videos/shechu-hell-e04
  - docs/videos/shechu-hell-e05
---

# 零台詞四系列第 2 集（新髮型、吊燈、雪國、年度簡報）：產線與成片

## Why

站主 2026-11-03：四個系列的 EP1 做完後，每個系列繼續做下一集；照推薦直接決定、依序做完。

## Definition of done

- [x] 四集的 `video.json`、`brief.md`（lint 0 錯誤），由 `docs/videos/zero-dialogue-series-ideas/production/make_episode.py` 從各集 spec 產生。
- [x] 第 3–5 集 12 份 spec（`production/gen_specs.py` 產生，每份 lint 0 錯誤）。站主 2026-11-03：每系列 5 集、共 20 集。
- [ ] Colab 首格、H3 直式片段（`run_episode.sh`：一張一張跑、每張逾時強制重試）。
- [ ] 剪接成片（`edit.py`）、站主看過。

## How to verify

```bash
for s in wangjia-couple-e02 raccoon-mischief-e02 influencer-piglet-e02 shechu-hell-e02; do node tools/video/cli.mjs lint --file docs/videos/$s/video.json; done
```

## Notes

- 配樂沿用各系列 EP1 的那首（同系列聽起來一致，也不用再付）；音效沿用 EP1 的，加上每集 spec 的 `sfx_extra`（ffmpeg 合成）。
- 每一鏡一個主角，笑點那一格寫成角色本身在做（EP1 的教訓）。
- 第 2 集四支成片（2026-11-03）：新髮型 13.5 s（s05、s06 片段後半自己換景，剪短）、吊燈 17.2 s（s01 模型把吊燈畫成完好，裁掉天花板）、雪國 15.6 s（成品照片段 1 秒就換景，改用首格慢推；裁掉模型畫的雜誌名）、年度簡報 14.6 s。
- `edit.py` 會自動在片段中途的硬切換景之前剪掉（scene > 0.4）；鏡頭慢慢移走的那種偵測不到，要看片。
