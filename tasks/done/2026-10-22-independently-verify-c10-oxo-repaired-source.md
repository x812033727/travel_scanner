---
id: 2026-10-22-independently-verify-c10-oxo-repaired-source
title: Independently verify C10 OXO repaired source and visuals v3
status: done
priority: P1
area: docs
owner: codex-c10-source-v3
claimed_at: 2026-10-22T15:10:12Z
created_at: 2026-10-22T15:10:06Z
completed_at: 2026-10-22T15:14:42Z
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v3.md
---

# Independently verify C10 OXO repaired source and visuals v3

## Why

作者為解除 C10 OXO 旁白盲讀 HOLD，改動了零售試用的結果、2000 年 Moore 回憶與第六章回收；前次來源 PASS 綁舊稿 SHA，不適用新版。需要不參與撰稿的代理核對新句和鏡頭，以及完整的 80 ID 對應與提示詞界線。

## Definition of done

- [x] 留下綁定四份目前檔案 SHA 的獨立 PASS／HOLD 收據，逐一交代改動 ID、直接來源、畫面與剩餘關卡。

## Steps

- [x] 比對前次收據與作者修訂，重讀 OXO 2017、Cooper Hewitt、MoMA、2000 年採訪等來源。
- [x] 核對 80 個 ID、71 張插圖與 9 張後製卡、提示詞禁名及閱讀版一致性。
- [x] 提交收據並更新草稿 PR 狀態，保留另一組盲讀關卡。

## How to verify

`Get-FileHash` 綁定四份檔案；PowerShell 比對 `3539fa3f9` 與現稿逐 ID 差異，再解析稿／JSON／閱讀版，得各 80 個唯一且同序 ID、71 `shot`、9 `stats`、最長連卡 2、JSON 與閱讀版零列不符、71 條 `prompt` 加 `visual_contract` 禁名零命中。`npm run check:tasks` 的結果另記在 Notes。

## Notes

收據：`docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v3.md`。本次 PASS 限來源與文字畫面方向；兩位新版盲讀、實測正文長度與插圖時間占比、生成畫面、站主稿件／逐鏡及整支費用核准仍獨立待驗。無付費生成或上架。`git diff --check` 通過。`npm run check:tasks` 退出碼 1，當時的兩項錯誤是工作樹另有未追蹤的 `tasks/open/2026-10-22-blindly-review-c10-oxo-narration-v2.md` 與 `tasks/open/2026-10-22-independently-recheck-c10-oxo-corrected-source.md`，其 ID 已在 `tasks/done/`；其餘輸出為過期認領與既有範圍重疊警告。`npm run tasks -- done` 已寫出本完成票，但因 open 副本仍被占用而退出碼 1，留下第三份未追蹤重複 open 副本；三份均未刪除、未提交。
