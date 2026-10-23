---
id: 2026-10-23-independently-review-rewritten-c16-bialetti-script
title: Independently review rewritten C16 Bialetti script and visuals
status: done
priority: P2
area: docs
owner: codex-c16-v2-independent
claimed_at: 2026-10-23T04:24:44Z
created_at: 2026-10-23T04:24:40Z
completed_at: 2026-10-23T04:27:37Z
branch: codex/brand-story-bialetti-c16-final-audit
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/independent-script-v2-review.md
---

# Independently review rewritten C16 Bialetti script and visuals

## Why

PR #1704 把先前已查核的 85 句劇本大幅改為 81 句。舊版逐句 PASS 及兩位舊版盲讀 HOLD 都不能裁定新版來源或配鏡；需要一份綁新四檔 bytes 的非作者獨立收據。

## Definition of done

- [x] 逐句核讀 81 句及同 ID 的 Markdown／JSON 配鏡，綁定作者精確 head 與四份 SHA-256，留下 PASS 或精確 HOLD 收據。
- [x] 對採用企劃的一手來源重讀關鍵頁面，保留 M16／M17 未解界線。

## Steps

- [x] 機械核對 ID 唯一性、順序、逐欄配對、插圖／字卡數與設定。
- [x] 獨立讀六章旁白和每鏡提示詞，定位需作者修改的句與畫。

## How to verify

`Get-FileHash docs/videos/story-everyday-bialetti-c16/{script.md,script-source-notes.md,visual-plan.md,visual-plan.json} -Algorithm SHA256`；用 PowerShell `ConvertFrom-Json` 對照 81 筆 JSON 與 `script.md`、`visual-plan.md` 的 81 個 ID，並逐欄比較分鏡表與 JSON。詳見 `docs/videos/story-everyday-bialetti-c16/reviews/independent-script-v2-review.md`。

## Notes

作者 head `a7303b2fa6feeaa374625f0b4629837b96ceb454`：80/81 句來源與 80/81 配鏡文字 PASS，`c160601` 旁白及畫面把 1957 雜誌廣告具體說成被收進「檔案盒」；館藏頁沒有這項保存過程。請作者只修這句、來源註記和成對配鏡後做新雜湊差異重核。ADI 完整 PDF 與米蘭基金會原站本輪逾時；發行者官方 PDF 索引及基金會發布的 Google Arts 館藏頁提供關鍵文字，收據明列可讀性。此審查不包含盲讀、實際 TTS、付費、站主核准或發布。

作者後續 head `b98f47e3d391b1e5b8d8b44f593c96ab9c57fdc5` 已只改 `c160601` 旁白與成對配鏡，來源註記同步收窄為可查館藏記錄。重新開啟基金會發布的館藏頁並檢查四檔新雜湊、81/81 ID 和 MD／JSON 逐欄一致後，差異 PASS，整體 81/81 句與 81/81 配鏡文字 PASS；精確新雜湊與限制見同一收據最末節。兩名新版盲讀、TTS 實測、站主核准及付費仍屬後續關卡。
