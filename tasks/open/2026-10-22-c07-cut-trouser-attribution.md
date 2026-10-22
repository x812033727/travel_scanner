---
id: 2026-10-22-c07-cut-trouser-attribution
title: Correct C07 cut trouser attribution
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T13:46:12Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Correct C07 cut trouser attribution

## Why

C07 v8 獨立來源差異審查指出，Crucq A1 寫早期 skinhead 青年的牛仔褲腳被裁短，沒有寫反摺。上一版旁白、畫面與來源說明把反摺歸給 A1；結尾另有同一遺漏。只修這組精確歸因，不改其他已查核句。

## Definition of done

- [x] 現行稿件、逐鏡與來源註記都以 A1 可直接支持的裁短牛仔褲腳描述，不再把反摺歸給 A1；77 句／77 鏡、64 插圖／13 卡維持。
- [ ] 另一代理依新 SHA 重核窄修與相鄰脈絡；此項屬獨立後續關卡，不由作者自認通過。

## Steps

- [x] 對齊 script c070102、404、612，visual c070102–103、404、612，及來源說明。
- [x] 把 v8 HOLD 與本版新 SHA 寫入審查摘要，保留 v8 收據為歷史。
- [ ] 協調者安排獨立 delta 重核、兩位純旁白盲讀與逐鏡預檢。

## How to verify

PowerShell 逐句與逐鏡 ID 比對、計算 shot／stats 與連續卡、檢查現行稿件無「反摺」、重算三檔 SHA；`git diff --check`。正文時長須核准後實際 TTS 測量。

## Notes

2026-10-22：v8 收據綁上一版 script `44C2EB2F…C9B8B3`、visual `7EDFD94E…7FFCF`、source notes `FDD04EB7…F484A`，對本版不能移用。補查 c070612 後，把這個結尾旁白與畫面一起改成「裁短」，避免殘留同一 A1 歸因錯誤。新 SHA：script `F13F4327C2A26C08EB64DF89C416A9AB628ACDCC98A17592D0B946C0F2BE07C2`、visual `6C20B067444DCEF920570771D56F0EB8F0AB763E974D86816D4136BB2AB46DD3`、source notes `E9DDAD4A6E8BCE656622083A4D91E9E405A90EAED9C8FF279A0E98A8381681C7`；尚無本版獨立 PASS、站主劇本核准或付費授權。機械核對 77/77 ID、64 shot／13 stats、最多兩連卡，正文 69 句／2,283 字元，三個現行檔案均無「反摺」。`git diff --check` PASS；`npm run check:tasks` 因既存 done/open 重複票 FAIL，未碰政策封鎖的重複票。
