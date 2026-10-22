---
id: 2026-10-22-refine-c07-cold-read-payoff
title: Refine C07 cold-read narrative and payoff
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T13:52:56Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Refine C07 cold-read narrative and payoff

## Why

獨立 v9 來源差異審查已核准褲腳歸因，但同 SHA 的全新純旁白讀者仍判敘事 HOLD：開場重問與型號限定打斷節奏，首賣日像研究註記，工人階級分析重複，音樂鉤子先被政治限定攔住，尾段從鞋帶、花卉、格紋到行銷像資料清單。此票只改非付費稿、逐鏡與作者來源註記；獨立收據不得由作者改判。

## Definition of done

- [x] 六章仍按年代推進，開場先給品牌與中心問題、工作段先見穿法、文化段回答音樂鉤子、末段以具體靴面與市場場景回到主題；逐句和逐鏡 ID 一對一。
- [ ] 新 SHA 的獨立來源差異、兩位全新純旁白盲讀及逐鏡預檢完成，才可向站主提劇本與逐鏡核准；正文 ≥480 秒另待核准後實際 TTS。

## Steps

- [x] 刪重問與硬插型號、把型號範圍放回展會段；首賣日限定為 B3 檔案未列。
- [x] 工作段去掉兩句重複分析，前章音樂問題由下章先回答，再交代政治分期。
- [x] 結尾保留 B2 八〇年代花卉客製，接 A1 大眾媒體與荷蘭店面、M1 1995 時尚靴；不寫客製造成商品設計或全球同步。
- [x] 同步逐鏡、來源界線、SHA 摘要；v9 PASS 與純旁白 HOLD 均標為綁舊 SHA 的歷史。
- [ ] 由協調者安排本版獨立覆核與兩位新讀者。

## How to verify

PowerShell 解析兩張表的 ID、類型、連卡與第 2–6 章純旁白字元；`git diff --check`、`npm run check:tasks`。真正正文秒數與插圖時間占比只能在核准後按實際配音和時間軸驗證。

## Notes

2026-10-22：v9 獨立 PASS 綁前版 script `F13F4327…07C2`、visual `6C20B067…46DD3`、source notes `E9DDAD4A…1681C7`；協調者另轉達一名真正冷讀者的敘事 HOLD。新稿 script `D73A820B0A426F8EDDE35F94718A9C440496D90867EB1AA1893B98D3E9B6BE99`、visual `98A8F2A59DEADBF81D323852D6D643985207D5DAC564D43A7AE0463B800E60CC`、source notes `95B272D6B1AF9A485419E704F9001E2180CC227919592B616159B45763F9C5EE`。73 句／73 鏡，62 shot／11 stats，最多兩連卡，第 2–6 章 67 句／2,211 字元。較原來 2,063 字多 148，但接近 C05 的 2,207 字／實測 484.74 秒，**不能據此宣稱 C07 達 480 秒**。沒有 C07 付費額度、劇本核准或實際 TTS。
