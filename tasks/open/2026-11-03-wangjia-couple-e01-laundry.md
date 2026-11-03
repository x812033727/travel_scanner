---
id: 2026-11-03-wangjia-couple-e01-laundry
title: 汪家夫妻 EP1〈幫忙曬衣服〉15 秒零台詞短劇：分鏡、評分審核
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T11:00:02Z
created_at: 2026-11-03T11:00:01Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/wangjia-couple-e01
  - docs/videos/wangjia-couple
---

# 汪家夫妻 EP1〈幫忙曬衣服〉15 秒零台詞短劇：分鏡、評分審核

## Why

站主看了參考爆紅片（寫實 AI 擬人化狗夫妻、13 秒、零台詞）後選了〈幫忙曬衣服〉（排序：曬衣服 > 打電動 > 蛋糕）。

## Definition of done

- [x] `docs/videos/wangjia-couple-e01/`：video.json、brief.md、storyboard.md（第 2 版）。
- [x] 三個點子與參考片一起盲評校準（`comedy-review/calibration-20261103/`）。
- [x] 站主看第 2 版分鏡（2026-11-03「好」），系列定為零台詞（`docs/videos/wangjia-couple/README.md`）。
- [x] 劇本關卡送審（2026-11-03）；Colab 配對完成，餘額 255.66 CU。
- [ ] 站主核准劇本 → 伺服器 `look` 畫兩個角色的設定圖（Qwen 首格的參照圖）。
- [ ] Colab：首格、三鏡小樣（直式 736×1312），站主看過再做其餘四鏡。
- [ ] 剪接、`shorts import`、八語標題說明。

## How to verify

```bash
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/wangjia-couple-e01/video.json --route hailuo --hailuo-model h3 --markdown
```

## Notes

- lint 唯一的錯是「需要 3 個章節」：漫劇產線照 YouTube 長片章節規則，15 秒的片子做不到，所以這支不走 `assemble`，走 Colab → ffmpeg → `shorts import`（storyboard.md §製作路線）。
- 參考片在文字盲評只拿 44，評分門檻因此從 80 調到 70，並寫明文字評審只做排名與診斷。
