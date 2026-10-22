---
id: 2026-10-22-independently-recheck-c10-oxo-corrected-source
title: Independently recheck C10 OXO corrected source and visual prompts
status: done
priority: P1
area: docs
owner: codex-c10-delta-review
claimed_at: 2026-10-22T14:45:36Z
created_at: 2026-10-22T14:44:57Z
completed_at: 2026-10-22T14:47:22Z
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v2.md
---

# Independently recheck C10 OXO corrected source and visual prompts

## Why

原獨立逐句與逐鏡來源審查對 c100308 和八條圖片提示詞設 HOLD。作者已定點修訂；需要另一位審查者綁定新版 SHA，逐項重新判定，不能沿用舊稿 PASS。

## Definition of done

- [x] 產出綁定新版 SHA 的獨立差異覆核，判定原 HOLD、其餘未改 ID 的繼承範圍與後續關卡。

## Steps

- [x] 直接重讀採訪與館方圖錄，核 c100308 旁白及概念圖。
- [x] 核對 80 個對應 ID，掃描所有圖片提示詞與共通契約，留下 PASS 收據。

## How to verify

`Get-FileHash` 取得四份新稿 SHA；`git show HEAD` 確認差異；PowerShell 解析 script／JSON 得 80／80 唯一且順序相同、71 shot／9 stats，對 shot.prompt 和 visual_contract 的禁名掃描為零。

## Notes

收據：`docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v2.md`。本次 PASS 僅來源和文字畫面方向；兩位盲讀、實測時長、依秒數插圖占比、站主審稿和整支費用仍是後續關卡。未付費。
