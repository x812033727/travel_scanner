---
id: 2026-09-28-video-story-check-audio-batching
title: 旁白檢查跨場景合併 Jev 呼叫
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:31:12Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# 旁白檢查跨場景合併 Jev 呼叫

## Why

旁白檢查（`tools/video/tts/check.mjs`）把聽起來跟稿子不一樣的句子交給 Jev 判斷，現在是**一個場景呼叫一次**。投影片影片一支約 30 個場景沒問題；品牌故事一支有 85–100 個鏡頭場景（`docs/videos/STORY.md`），每天兩支就可能用掉一兩百次，而 Jev 的每日次數（預設 200）是全站共用的，新聞與景點審核也在用。

一次呼叫最多可以帶 40 句（`MAX_JUDGE_LINES`），所以把不同場景待判的句子合併送，呼叫次數可以降到原本的一小部分。

## Definition of done

- [ ] 待判的句子跨場景合併，每次最多 `MAX_JUDGE_LINES` 句；判斷結果仍寫回各自的句子，旗標檔格式不變。
- [ ] 90 個場景、每個場景 1 句待判的測試案例，Jev 呼叫次數是 3，不是 90。
- [ ] 投影片影片與有角色對白的漫劇，檢查結果與現在相同。

## Steps

- [ ] 改寫送 Jev 的迴圈：先收集全部待判的句子，再分批。
- [ ] 測試：呼叫次數、結果對應、部分批次失敗時已判的結果保留。

## How to verify

```bash
node --test tools/video/tts
npm run test:tools
```

## Notes

- 伺服器端的 `JudgeIn` 上限也是 40 句，兩邊要一致。
- 這張票不改 Jev 的每日次數；那是後台設定，上線時由站主或部署的人調（`STORY.md` §上限與成本）。
