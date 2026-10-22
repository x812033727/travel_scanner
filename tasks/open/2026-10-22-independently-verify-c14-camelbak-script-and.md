---
id: 2026-10-22-independently-verify-c14-camelbak-script-and
title: Independently verify C14 CamelBak script and visual claims
status: review
priority: P1
area: docs
owner: codex-root-c14-independent
claimed_at: 2026-10-22T17:09:39Z
created_at: 2026-10-22T17:09:24Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-script-visual-review.md
---

# Independently verify C14 CamelBak script and visual claims

## Why

C14 作者稿只帶作者來源註解。需要由另一人重讀原件、逐組檢查 67 句與逐鏡文字，尤其 1988／1989 的不同事件、平行咬合閥專利、2006 年瓶類與 2014 年毛銷售額分母。

## Definition of done

- [x] SHA 綁定的獨立來源與逐鏡文字判定，逐組說明可講與不可推的界線。
- [x] 區分來源 PASS、紙上畫面算術與仍待的雙盲、TTS、圖片及站主劇本關卡。
- [x] 收據與 PR 遠端版本已讀回。

## Steps

- [x] 直接重開地區品牌、母公司 SEC 年報與 Fawcett 專利，核對修改後 O10。
- [x] 對 67 個旁白與 67 個 JSON 鏡頭、後製卡作文字審查。
- [x] 提交、推送並讀回草稿 PR；head `7f25bf71db11a677386dfca653d78edcb70a6704`。

## How to verify

`Get-FileHash` 對四份作者稿；獨立解析 JSON 的 ID／鏡數／秒數；`git diff --check`、`gh pr view 1695 --json headRefOid,isDraft`。未採購媒體。

## Notes

本輪 USPTO 商標 PDF 逾時，未用作口播判定。C14 `test:docs-videos` 在此環境因缺 `pinyin-pro` 未過，不歸咎稿件也不宣稱該 gate 通過。
