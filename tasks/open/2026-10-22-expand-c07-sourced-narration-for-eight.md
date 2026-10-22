---
id: 2026-10-22-expand-c07-sourced-narration-for-eight
title: Expand C07 sourced narration for eight-minute body
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T12:37:52Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Expand C07 sourced narration for eight-minute body

## Why

C07 第 2–6 章舊稿 69 句／2,063 字。相同製作路線的 C05 71 句／2,207 字實測 484.74 秒，C06 86 句／2,646 字實測 505.94 秒；C07 在買圖前可能達不到正文至少 480 秒的關卡。須用已可讀的來源增加故事資訊，不能靠停頓、片頭或空話撐長度。

## Definition of done

- [x] 六章因果順序、77 個 ID 與逐鏡一對一保持；第 2–6 章比原來的 2,063 字多 507 個有來源的旁白字元，逐鏡同步。
- [ ] 本版獨立來源差異查核、兩位真正盲讀、視覺重檢完成後，才可向站主提劇本與逐鏡核准；正文 ≥480 秒仍待核准後真實 TTS 實測。

## Steps

- [x] 直接讀 B2、B3、M1、A1，限定公司回顧、館方描述與研究詮釋各自能說到的範圍。
- [x] 補德國年長女性市場、海外廣告與 Griggs 製鞋經驗；補早期青年文化交會及九〇年代混搭、行銷選擇。
- [x] 同步逐鏡、來源邊界與 SHA 綁定摘要；舊 PASS 標成歷史判定。
- [ ] 交由不同代理依新 SHA 做獨立查核與兩位純旁白盲讀，再由站主審核。

## How to verify

PowerShell 逐句欄計字、腳本與逐鏡 ID/類型比對、最多連續資料卡、`git diff --check`；`npm run check:tasks`。正文秒數及插圖播放時間必須以核准後真實 TTS／時間軸證明，不靠字數推定。

## Notes

2026-10-22：作者版 script SHA `3158FB75A446C9DBA70ABFB8070736D1F83EEF06568C8386291E592DA5C7025F`，visual SHA `DD80C703D62A277DB70D3B69F5CAAE0B03F95240B65C098652053B54E2931FC2`，source notes SHA `574EE8DE924A1A731E818ABD0BA0A1EC70305C9B83D2F937B53838F5F87AE53F`。第 2–6 章 69 句／2,509 字，比舊稿 +446；全稿 77 句／77 鏡、64 插圖／13 字卡、最長兩張連卡。舊版 v5 來源、讀者 1 收據與視覺差異 PASS 均綁舊 SHA，不可沿用；讀者 2 舊版口頭 PASS 待另存。四張政策封鎖的未追蹤重複票不是本票產物，不碰。

2026-10-22：前版 `3158FB75…025F` 的獨立 v6 來源／視覺差異覆核 PASS，後續純旁白盲讀仍 HOLD：開場籠統、出廠與零售及工作用途重複、加勒比音樂先提後解釋、ska／rocksteady／Two Tone 無白話脈絡、結尾抽象。按此重新寫稿並對鏡：script SHA `8E6FD3C990A88A9780F5C26A7B4A9A251B09B109732031C3291471DA2095D47A`、visual SHA `811ED1C8E73082172E03CB991B5E856675BA88559FD75490D48AD64B77C8B3B3`、source notes SHA `AF4CDECE32943DC1B8146E112B7595A1D9A4945FC8B9301A55B55E6B7370C5C6`。本版第 2–6 章 69 句／2,570 字，比最初 2,063 字多 507；全稿 77 句／77 鏡、64 插圖／13 字卡、最多兩張連卡。已移除旁白的 Two Tone，新增公司回顧的園藝用途與八〇年代花卉裝飾、館藏 1995 年格紋款，來源種類和日期界線見 source notes。前版所有 PASS 均為歷史；本版仍須獨立來源差異查核、兩位新純旁白盲讀及視覺預檢。未做付費 TTS／買圖，480 秒仍待真實實測。

2026-10-22 最後逐鏡校對：c070303 的型號揭示由本句旁白負責，日期拆解由 c070306 後製卡負責；不讓影像模型生成字，也不錯稱「下一鏡字卡」。script SHA 不變；final visual SHA `81496D08D679B32314BC5C588EAE49DF9B69261AF5F4E78D1ADE73225E8D4CB1`，取代上一段的 visual SHA；審查仍待全新 SHA 覆核。
