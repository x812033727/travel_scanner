---
id: 2026-10-22-correct-c07-floral-method-and-museum
title: Correct C07 floral method and museum production year
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T14:17:28Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Correct C07 floral method and museum production year

## Why

獨立 [v10 來源差異審查](../../docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v10.md) 對前版稿件判兩處 HOLD：B2 只記八〇年代花卉客製，沒有證據說用畫筆或手繪；M1 所標 1995 是館藏靴的製造年，舊旁白與字卡卻像在說博物館當年記錄它。本票限 C07 這兩處的非付費窄修，不改獨立審查收據。

## Definition of done

- [x] c070606–607 旁白及畫面只描述品牌回顧的花卉客製，不指定工法。
- [x] c070609 旁白及卡片明說館藏靴製於 1995 年，不推入藏或記錄日期，也不推花卉客製造成格紋商品。
- [x] 來源註記、審查摘要與 SHA 更新；腳本／逐鏡 ID 與卡片結構保持一致。
- [ ] 新 SHA 的獨立來源差異覆核、兩位全新純旁白盲讀及逐鏡預檢，交協調者安排後才能提站主審稿。

## Steps

- [x] 對照 v10 收據的 B2、M1 限定，僅修 3 個 ID 及共同來源說明。
- [x] 以機械檢查核對 73 句／73 鏡、卡片連續數、正文字元與三檔雜湊。
- [ ] 協調者安排另一人對新 SHA 差異重查及兩位新讀者盲讀。

## How to verify

PowerShell 正規式解析 `script.md`／`visual-plan.md` 的 ID、`shot`／`stats` 與最長連卡；`Get-FileHash -Algorithm SHA256` 算三檔；`git diff --check`。這只證明結構，不代替獨立查核、真正盲讀或實際 TTS 秒數。

## Notes

2026-10-22：改 c070606–607 的畫筆／手繪敘述為 B2 可支持的素面八孔靴與完成花卉裝飾；逐鏡移除手、工具及工法。c070609 改為倫敦博物館收藏一雙**製於 1995 年**的格紋靴，卡片同標製造年。來源註記寫明 B2 未給方法、M1 未給博物館記錄或入藏年份。新三檔 SHA 與結構詳見 `reviews/script-review-summary.md`；v10 HOLD 綁舊 SHA，不可當成本版 PASS。正文 67 句／2,223 字元，與 C05 2,207 字／實測 484.74 秒接近，C07 **未經 TTS 實測達 480 秒**；未授權付費製作。
