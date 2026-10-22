---
id: 2026-10-22-independently-verify-c10-oxo-retail-payoff
title: Independently verify C10 OXO retail payoff source delta v4
status: done
priority: P1
area: docs
owner: codex-c10-source-v4
claimed_at: 2026-10-22T15:40:13Z
created_at: 2026-10-22T15:39:28Z
completed_at: 2026-10-22T15:43:52Z
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v4.md
---

# Independently verify C10 OXO retail payoff source delta v4

## Why

作者為處理 C10 OXO v3 盲讀 HOLD，將零售試用與結尾縮窄至來源可證的範圍。v3 來源 PASS 綁舊 SHA；需另一名未參與修稿者直接比對 v4 的每個改動句與鏡頭，尤其展示延伸、非關節炎顧客和零售結果。

## Definition of done

- [x] 留下綁定 v4 四份檔案 SHA、逐 ID 判定的獨立來源與文字畫面 PASS／HOLD 收據。

## Steps

- [x] 重讀 OXO 2017 回顧、2000 年 Moore／Farber 採訪、Cooper Hewitt 與 MoMA，核對 12 句旁白。
- [x] 核對 4 個改動鏡頭、80 ID 對應、禁名與銷售因果界線。
- [x] 交付收據，不更動作者稿、視覺方案或付費資產。

## How to verify

比對 `c8f14e5db` 與現稿逐 ID 差異；PowerShell 解析三份稿／視覺文件，確認各 80 個唯一同序 ID、71 `shot`、9 `stats`、最長連卡 2、JSON／閱讀版零列不符及圖片提示詞禁名零命中。`Get-FileHash` 重算四份 SHA，`git diff --cached --check` 檢查提交。

## Notes

收據：`docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v4.md`。本次僅來源與逐鏡文字提案 PASS；兩名新旁白盲讀、時長、圖片時間占比、站主稿件／逐鏡及費用核准仍獨立待驗。無付費呼叫或上架。`npm run check:tasks` exit 1，原因是四張**先前** done/open 重複任務票（v2/v3 盲讀及兩張舊來源覆核）；`npm run tasks -- done` 已寫入本檔，但 exit 1，因 open 副本仍在，故又留下本票的 open ghost。政策阻擋刪除，未繞過或納入提交。
