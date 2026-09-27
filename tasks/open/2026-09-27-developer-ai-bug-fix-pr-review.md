---
id: 2026-09-27-developer-ai-bug-fix-pr-review
title: Developer AI bug fix PR review video
status: in-progress
priority: P2
area: docs
owner: codex-video-review
claimed_at: 2026-09-27T16:32:36Z
created_at: 2026-09-27T15:26:33Z
completed_at:
branch: codex/ai-developer-videos
depends_on: []
scope:
  - docs/videos/ai-bug-fix-pr-review
---

# Developer AI bug fix PR review video

## Why

開發者篇第二支以同一份真實修補示範：舊測試全綠仍漏了非整除案例，AI 修補須依需求、實際差異與回歸驗收三關審查。

## Definition of done

- [x] `docs/videos/ai-bug-fix-pr-review/` 有企劃、完整口播與畫面資料、主張表，且示範與同題修補的實際差異和測試相符。
- [ ] 獨立查核通過，完成合成旁白、五語字幕、縮圖、成片與待上架包。

## Steps

- [x] 用舊碼與實際 Claude Code 修補，建立可重跑的三關審查示範。
- [x] `video.json` 避免把本地示範說成正式站事故或已合併的 PR；`lint` 零錯誤零警告。
- [ ] 獨立查核後跑後續媒體管線與品檢。

## How to verify

`node tools/video/cli.mjs lint --slug ai-bug-fix-pr-review`；交叉核對 `../ai-coding-tools-same-task/demo/claude.patch` 與 `acceptance.test.mjs`。

## Notes

2026-09-27：起始程式 2 個舊測試全過，但 100 分分三人只得 99；事後四類驗收在起始碼 1/4、修補後 4/4。片中單位統一為「分」。遠端審核及 TTS 尚未執行。
2026-09-28：獨立 verify-1.md 與兩支工具的原始修補、測試輸出已交叉核對；五語字幕經獨立交叉審稿，28 張字卡與縮圖已目視檢查。TTS、成片、品管、審核及上架包仍待完成。
2026-09-28：Gemini Sulafat 旁白完成，`check-audio` 133/133 句、零標記；改寫的七句已同步五語字幕並經獨立覆核，`lint` 零錯誤零警告，最終成片重組中。站主大綱核准、正式站審核、11 項品管與待上架包尚待完成。
2026-09-28：新版 1080p `final.mp4` 完成，18,255 影格、約 10:08、-14 LUFS；`checks.json` 全過且無問題。五語字幕已按最終時間軸重產。待站主大綱核准及正式站各審核關卡。
