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

獨立 v9 來源差異審查已核准褲腳歸因，但同 SHA 的全新純旁白讀者仍判敘事 HOLD：開場重問與型號限定打斷節奏，首賣日像研究註記，工人階級分析重複，音樂鉤子先被政治限定攔住，尾段從鞋帶、花卉、格紋到行銷像資料清單。後續 v11 來源差異對修訂稿 PASS，但真正只讀旁白的 v11 讀者 A 另指出第三章展會限定阻斷工廠→工作者的故事、第六章鞋帶政治與花卉客製缺少對照。本票續作只改非付費稿、逐鏡與作者來源註記；獨立收據不得由作者改判。

## Definition of done

- [x] 六章仍按年代推進，開場先給品牌與中心問題、工作段先見穿法、文化段回答音樂鉤子、末段以具體靴面與市場場景回到主題；逐句和逐鏡 ID 一對一。
- [ ] 新 SHA 的獨立來源差異、兩位全新純旁白盲讀及逐鏡預檢完成，才可向站主提劇本與逐鏡核准；正文 ≥480 秒另待核准後實際 TTS。

## Steps

- [x] 刪重問與硬插型號、把型號範圍放回展會段；首賣日限定為 B3 檔案未列。
- [x] 工作段去掉兩句重複分析，前章音樂問題由下章先回答，再交代政治分期。
- [x] 結尾保留 B2 八〇年代花卉客製，接 A1 大眾媒體與荷蘭店面、M1 1995 時尚靴；不寫客製造成商品設計或全球同步。
- [x] 同步逐鏡、來源界線、SHA 摘要；v9 PASS 與純旁白 HOLD 均標為綁舊 SHA 的歷史。
- [x] v11：把展會目的和下一步生產串起，首賣日／型號範圍壓成一句；以不同靴款切鏡到工作穿著，沒有追認首位買家或展會成交。
- [x] v11：把同時期鞋帶政治誤讀與另一群人花卉客製並置，再拉遠到媒體／荷蘭商店，不推彼此因果。
- [x] 新版 73 句／73 鏡同序、鏡型／連卡／名稱與來源界線機械檢查，v11 PASS 和盲讀 HOLD 標為綁舊 SHA 的歷史。
- [ ] 由協調者安排本版獨立覆核與兩位新讀者。

## How to verify

PowerShell 解析兩張表的 ID、類型、連卡與第 2–6 章純旁白字元；`git diff --check`、`npm run check:tasks`。真正正文秒數與插圖時間占比只能在核准後按實際配音和時間軸驗證。

## Notes

2026-10-22：v9 獨立 PASS 綁前版 script `F13F4327…07C2`、visual `6C20B067…46DD3`、source notes `E9DDAD4A…1681C7`；協調者另轉達一名真正冷讀者的敘事 HOLD。新稿 script `D73A820B0A426F8EDDE35F94718A9C440496D90867EB1AA1893B98D3E9B6BE99`、visual `98A8F2A59DEADBF81D323852D6D643985207D5DAC564D43A7AE0463B800E60CC`、source notes `95B272D6B1AF9A485419E704F9001E2180CC227919592B616159B45763F9C5EE`。73 句／73 鏡，62 shot／11 stats，最多兩連卡，第 2–6 章 67 句／2,211 字元。較原來 2,063 字多 148，但接近 C05 的 2,207 字／實測 484.74 秒，**不能據此宣稱 C07 達 480 秒**。沒有 C07 付費額度、劇本核准或實際 TTS。

2026-10-22 v11 續作：前版 script `93B90BCC…24FBFE`、visual `9E2A253A…B21F45`、notes `8232C640…A689` 有獨立來源 PASS，卻獲純旁白讀者 A 敘事 HOLD。現版改句 c070307–310、606–608，改鏡 c070307–311、606、608；展會只作待接單節點，花卉與鞋帶只作不同時地並置。新 script `624AF568EC2F85C2DF2536A307433A4EADF301EEAA095D8CD676A5418C2AB47B`、visual `4072D25873B8D4E86A5DE82AC35D532E4D490E0A2CAE11A00EAEFDF5F1D1FB96`、notes `3D14723D60EAF0E12657DC97E75C9B720D339C301925B4B2019B622A27D69FC2`。73 句／73 鏡，63 shot／10 stats、最多兩連卡；第 2–6 章 67 句／2,275 字元。`git diff --check` 通過；`npm run check:tasks` 因既存 policy-blocked `done` 留下的 open/done 重複任務檔而退出 1，本票未碰那些孤兒檔。新 SHA 尚無獨立來源 PASS 或兩位新盲讀，**實際 ≥480 秒未證**，無劇本、付費或上架授權。
