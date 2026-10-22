---
id: 2026-10-22-price-c10-oxo-local-pilot
title: Price C10 OXO local pilot before paid calls
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-c10-quote
claimed_at: 2026-10-22T16:56:45Z
created_at: 2026-10-22T16:56:32Z
completed_at:
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/production-quote.md
---

# Price C10 OXO local pilot before paid calls

## Why

站主已核准 C10 劇本與逐鏡方向；下一個付費關卡需先把整支最大張數、每張重試、旁白與配樂、已知單價和 US$25 停線報清楚。舊集費用仍有未能歸因部分，不能直接開跑。

## Definition of done

- [x] 有綁定已核准稿件 SHA 的整支非付費報價、已知媒體項上界與未拆價項。
- [x] 明列站主費用決定與帳本、TTS 實測、按秒畫面比例等前置停線。

## Steps

- [x] 讀回 80 句／71 插圖／9 字卡、最長連卡、23 個長插圖鏡與旁白字元數。
- [x] 重新核對 MiniMax image-01、API-vlm 及 Google Lyria 3.5 官方價。
- [x] 計算 94 張、282 次請求與可見費用上界。

## How to verify

對當前 `visual-plan.json` 與 `script.md` 重新統計句／鏡與長句；`Get-FileHash` 確認核准版；`git diff --cached --check`。公開價格連結及取價日已寫入 `production-quote.md`。

## Notes

本票只交非付費報價，沒有取得 C10 整支費用核准。US$3.957 僅是 282 次圖片＋評審與一首配樂的公開價上界；旁白、轉錄、模型、稅費與不確定帳單仍併入 US$25。C03–C06 費用歸因及本集硬停線路由須在付款前讀回，不能因稿件核准就付款。
