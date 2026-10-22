---
id: 2026-10-22-write-c14-camelbak-source-bound-script
title: Write C14 CamelBak source-bound script and visual plan
status: review
priority: P1
area: docs
owner: codex-c14-script
claimed_at: 2026-10-22T16:57:02Z
created_at: 2026-10-22T16:56:48Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/script.md
  - docs/videos/story-everyday-camelbak-c14/script-source-notes.md
  - docs/videos/story-everyday-camelbak-c14/visual-plan.md
  - docs/videos/story-everyday-camelbak-c14/visual-plan.json
  - docs/videos/story-everyday-camelbak-c14/reviews/2026-10-23-author-script-receipt.md
  - docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v6-coordinator.md
  - docs/videos/story-everyday-camelbak-c14/reviews/2026-10-23-author-v7-script-receipt.md
  - docs/videos/story-everyday-camelbak-c14/reviews/2026-10-23-author-v8-n10-delta-receipt.md
  - docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v8-coordinator.md
---

# Write C14 CamelBak source-bound script and visual plan

## Why

站主採用 C14 CamelBak 的修訂 Treatment（SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`）及來源矩陣（SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`）後，需要一版供獨立逐句查核的非付費口播稿與逐鏡方向。這張票只管作者稿；站主採用企劃不等於核准稿、圖片或上架。

## Definition of done

- [x] 六章繁中逐字稿逐句綁來源與主張，含濃縮開場、5 秒片頭、片尾三句及 21 秒 v4 片尾／連結位。
- [x] `loops` 與具體鉤子平均約 30–45 秒，紙上正文字數估算超過 480 秒並清楚標為未實測。
- [x] 每鏡畫面、行 ID、秒數與後製字卡可機械核對；插圖規劃時間至少 70%、連卡不超過三張。
- [x] 作者收據綁定本稿檔案 SHA，交另一位代理做來源審核與雙讀者盲評；不自判 PASS。
- [ ] 獨立逐句來源審核、敘事盲評、站主稿／分鏡採用、TTS 實測與付費前報價各走後續關卡，本票不得自行視作完成。

## Steps

- [x] 核對採用收據與 Treatment／矩陣雜湊，不改兩份已採用企劃。
- [x] 重開品牌回顧、母公司 2014 年 SEC 年報、1998 口器與 2005 水瓶專利、2003 寄送報導、2006 展場報導與 2007 公司新聞稿；標記年份衝突與不能推出的因果。
- [x] 撰寫 `script.md`、`script-source-notes.md`、`visual-plan.md`／JSON。
- [x] 用獨立的機械檢查核對行 ID、字元估時、最長鏡、卡片連續數、圖片時間比、鉤子空檔與圖像提示詞禁項。
- [x] 獨立覆核者從原件逐句檢查並留下與稿版雜湊綁定的 PASS／HOLD；作者不能代簽。v7 全稿覆核唯一 N10 HOLD，由另一位審查者於 v8 精確 SHA 窄修覆核 PASS；這不代替成圖、TTS 或站主採用。

## How to verify

`Get-FileHash` 核對採用企劃及作者稿 SHA；解析 v8 的 70 行口播與 JSON 70 鏡一對一、行末 S 來源存在、句長換算鏡頭 ≤12 秒、插圖時間比例 ≥70%、最長連卡 ≤3、冷開場後片頭 5 秒與片尾 21 秒；只把新「鉤」算作設問／揭露，不能把「回收鉤」再算成新鉤，並計算最大暫估空檔 ≤45 秒；`git diff --check`、`npm run check:tasks`。這些只核對草稿結構，不能代替 TTS、逐句事實審查、兩位盲讀或站主決定。

## Notes

v1、v2 的純旁白投影各收兩位獨立讀者 HOLD，詳見兩份 `blind-narration-*-coordinator.md`；v2 逐句來源 PASS 與 v3 I01 字卡 PASS 都只綁舊檔案 SHA。v4、v5 獨立逐句與逐鏡覆核均為 HOLD。v6 O02 來源／逐鏡窄修獨立 PASS；74 行 v6 純旁白兩位讀者一 HOLD、一 PASS，精確投影 SHA、分歧和限度記於 `reviews/blind-narration-v6-coordinator.md`。v7 縮短重複咬合機制、明確同一專利 1998 送件／2000 授權、以 2003 背水場合接兩年後水瓶文件、收緊通路段並立即揭露 2012／2014 比例；`reviews/independent-v7-source-visual-review.md` 只在 N10 HOLD，因「水只在喝時才靠近嘴邊」超出 S2 肩上管與 S11 咬合閥證據。v8 只將 N10 改為人控制水何時從出口流出，沿用左右分屏概念鏡頭，重算 N10 紙上秒數，其他 69 行口播及鏡頭內容不改。新 SHA 須獨立 N10 聲畫重查及兩位新純旁白讀者。專利文件對文件引用不推量產 SKU 每個零件；2003 寄送不當首軍用或水瓶動機；1988 背景和商標 first-use 不替品牌回憶定年；2014 毛銷售額占比不是現況或巡店單因果。所有圖像只規劃概念插圖。詳見 `script-source-notes.md`。此票停在 `review`，由獨立覆核接手下一關。

## 2026-10-23 v8 審查交接點

`reviews/independent-v8-n10-delta-review.md` 由非作者審查者按 v8 四檔精確 SHA 對 N10 聲畫窄修判 **PASS**，與 v7 全稿來源／文字逐鏡覆核的其餘 69 行相接。兩位未讀 v8 的純旁白讀者各自只讀 70 行投影（SHA-256 `87598ADA8FAC2AE4FC35F620056FCE395017E4780165CA07B35667861A86757C`），均判 **PASS**，具體與可選潤飾見 `reviews/blind-narration-v8-coordinator.md`。目前可交站主審稿與分鏡方向；**尚非站主採用、TTS 正文 ≥480 秒、生成圖驗收、付費或上架授權**。本票維持 `review`，不更動已受審的四份作者稿。
