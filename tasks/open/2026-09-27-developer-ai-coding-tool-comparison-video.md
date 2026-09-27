---
id: 2026-09-27-developer-ai-coding-tool-comparison-video
title: Developer AI coding tool comparison video
status: in-progress
priority: P2
area: docs
owner: codex-video-review
claimed_at: 2026-09-27T16:32:22Z
created_at: 2026-09-27T15:25:28Z
completed_at:
branch: codex/ai-developer-videos
depends_on: []
scope:
  - docs/videos/ai-coding-tools-same-task
  - docs/videos/lexicon.json
---

# Developer AI coding tool comparison video

## Why

四支 AI 影片的開發者篇需要可重跑的同題實測；影片只能說明本機真的跑出的結果，不能把登入失敗或工具估算成本寫成性能排名。

## Definition of done

- [x] `docs/videos/ai-coding-tools-same-task/` 有企劃、完整口播與畫面資料、主張表，以及可重跑的同題起點、事後驗收與兩份實際差異。
- [ ] 獨立查核通過，完成合成旁白、五語字幕、縮圖、成片與待上架包。

## Steps

- [x] 三支 CLI 使用相同起點與提示，逐一記錄執行結果與失敗原因。
- [x] `video.json` 寫明不能解釋成排名的限制，`lint` 零錯誤零警告。
- [ ] 獨立查核後跑後續媒體管線與品檢。

## How to verify

`node tools/video/cli.mjs lint --slug ai-coding-tools-same-task`；`node --test docs/videos/ai-coding-tools-same-task/demo/fare.test.mjs`。兩份工具修補的事後測試與 CLI 原始紀錄在 repo 外工作區。

## Notes

2026-09-27：Claude Code 2.1.270 與 Codex CLI 0.158.0-alpha.2.1 各修好同題，事後驗收皆 4/4；Gemini CLI 0.61.0 在登入階段因 `IneligibleTierError: UNSUPPORTED_CLIENT` 未啟動。完整證據見 `comparison.md`，原始媒體與 JSON/JSONL 只放 repo 外。Claude 輸出的美元數字是工具估算，不是實際訂閱扣款。遠端審核及 TTS 尚未執行。
2026-09-28：獨立 verify-1.md、verify-2.md 完成；Google 官方棄用公告與本機登入錯誤重新核對，影片明示 Gemini 未進入程式能力比較。五語字幕經獨立交叉審稿，28 張字卡與縮圖已目視檢查，TTS 正在進行。原始 CLI 輸出只在 repo 外；畫面為實際輸出的視覺化。
2026-09-28：Gemini Sulafat 旁白完成，`check-audio` 131/131 句、零標記；改寫的八句已同步五語字幕並經獨立覆核，`lint` 零錯誤零警告，最終成片重組中。站主大綱核准、正式站審核、11 項品管與待上架包尚待完成。
2026-09-28：新版 1080p `final.mp4` 完成，18,899 影格、約 10:30、-14 LUFS；`checks.json` 全過且無問題。五語字幕已按最終時間軸重產。待站主大綱核准及正式站各審核關卡。
