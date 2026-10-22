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
- [x] 重開品牌回顧、母公司 2014 年 SEC 年報和閥專利；標記年份衝突與不能推出的因果。
- [x] 撰寫 `script.md`、`script-source-notes.md`、`visual-plan.md`／JSON。
- [x] 用獨立的機械檢查核對行 ID、字元估時、最長鏡、卡片連續數、圖片時間比、鉤子空檔與圖像提示詞禁項。
- [ ] 獨立覆核者從原件逐句檢查並留下與稿版雜湊綁定的 PASS／HOLD；作者不能代簽。

## How to verify

`Get-FileHash` 核對採用企劃及作者稿 SHA；解析 v2 的 61 行口播與 JSON 61 鏡一對一、行末 S 來源存在、句長換算鏡頭 ≤12 秒、插圖時間比例 ≥70%、最長連卡 ≤3、冷開場後片頭 5 秒與片尾 21 秒；計算真正設問的最大暫估空檔 ≤45 秒；`git diff --check`、`npm run check:tasks`。這些只核對草稿結構，不能代替 TTS、逐句事實審查、兩位盲讀或站主決定。

## Notes

v1 純旁白投影已收到兩位獨立讀者 HOLD，並由 `reviews/blind-narration-v1-coordinator.md` 記錄；作者依意見回修 v2，須以新版 SHA 重做獨立來源與敘事覆核。O10 口播只保留品牌回顧的 1989 比賽；較晚專利回溯的 1988 背包與水瓶組合、商標的 1988 first-use 聲稱留在筆記，後兩者不替同一場比賽定年。Fawcett 1990 申請的閥專利先明示為另一人的平行工程證據，沒有排定相對於 ThermoBak 首售的先後或採用；商品線按 1993→2006→2014 往前。2006 瓶類與 2014 CamelBak 毛銷售額 50%／37% 皆明示年度與分母，不寫現況或巡店單因果。所有生成圖僅規劃概念插圖，沒有商標、專利附圖或真人重建。詳細待審疑點在 `script-source-notes.md`。此票停在 `review`，由獨立覆核接手下一關。
