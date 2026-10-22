---
id: 2026-10-22-independently-audit-c12-pyrex-script-and
title: Independently audit C12 Pyrex script and visual plan
status: done
priority: P1
area: docs
owner: codex-c12-source-review
claimed_at: 2026-10-22T14:56:24Z
created_at: 2026-10-22T14:56:09Z
completed_at: 2026-10-22T15:01:25Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-script-source-review.md
---

# Independently audit C12 Pyrex script and visual plan

## Why

C12 的企劃已採用，但 80 句新逐字稿和 80 鏡方向不能沿用 Treatment 的來源 PASS。另一位查核者必須按這一版雜湊重開來源並留下可供作者改稿的逐 ID 收據。

## Definition of done

- [x] SHA 綁定的獨立來源與逐鏡收據寫入指定 review 路徑。
- [x] 80 句與 80 鏡逐項標示 PASS／HOLD，列出可直接開啟的原始來源、修訂 ID 和未通過的製作關卡。

## Steps

- [x] 重開 S1–S7 原始頁或記錄活頁存取障礙，獨立核對 80 句。
- [x] 對位 80 鏡並檢查身份、文字、假史料、圖片時間比與片頭片尾。
- [x] 留下 HOLD 與作者可執行的改稿建議，不更動作者逐字稿。

## How to verify

`Get-FileHash ... -Algorithm SHA256` 核對 Treatment、矩陣、劇本、逐鏡雜湊；逐 ID 核讀 `script.md`、`visual-plan.md` 與上述來源；`npm run check:tasks` 檢查任務協定。收據在 `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-script-source-review.md`。

## Notes

本版結論 HOLD：H04 年距、T03 擬似廣告引文；I07 須限縮家廚紀錄措辭；O12 畫面把「破碎」畫成「缺角」。O07、I03、I13、E02、E03 的查核／剪輯語不宜念進旁白。S3 原站活頁本次超時／Cloudflare challenge，只取得原站搜尋索引的完整問答，已用 S2、S6 交叉核對。兩位盲讀、念法、付費配音、圖片與站主稿件審核尚未完成。
