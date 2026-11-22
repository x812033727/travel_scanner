# Independent Fact-Check & Redline Audit (Final) — `curio-w27-marugame-seimen` (N9105)

**Auditor**: Independent Fact-Checker & Redline Auditor (read-only research subagent, verified on locked facts v5/v6)
**Date**: 2026-11-22
**Result**: **VERDICT: PASS**

## 1. All Round 1 & Round 2 Defects Resolved (100% PASS)
- **Revenue vs. profit separation**: `s01.chapter` (`年賣千億日圓？`), `m007` (`年營收衝上一千三百七十二億日圓`), `m008` (`獲利更是中央廚房主要對手九倍以上`), `m081` (`賣三百三十億日圓、利益二十四億`), `m082` (`利益兩百二十億日圓、贏逾九倍`), `m083`–`m084`, `thumbnail.data.headline` (`丸龜製麵狂賣千億？`), `youtube.title` (`年賣1372億日圓？`), `brief.md` all cleanly separate revenue from business profit.
- **Explicit JPY currency (`日圓`)**: Present on `m007`, `m045` (`兩百九十日圓` / `五百七十`), `m081`, `m082`, `m083`, `m098`, `s01.chapter`, and `youtube.title`.
- **60+ senior employee denominator (`m067`)**: `"改聘主婦與銀髮族，二零二零年光長輩破兩千二。"` matches `C08` (`2,249` employees aged 60+ as of March 2020) without folding homemakers into the count.
- **Overseas timeline & parent-group attribution (`m088`)**: `"一三年台北印尼、二一年倫敦，母集團海外破九百。"` separates 2013 (Taipei/Indonesia) from 2021 (London) and attributes `923` overseas stores explicitly to parent group `母集團`.
- **Precision items (`m012`, `m031`–`m032`, `m068`, `m082`)**: Unsourced `"只想開三家"` removed; `2011` 47 prefectures & 500 domestic Marugame stores aligned with `C04`; local events broadened in `m068`; `9.046×` profit ratio stated as `逾九倍` across `m008`, `m082`, `loops[8]`, `brief.md`, and `claims.md`.

## 2. Redlines, Visual Safety & Packaging Checks (100% PASS)
- **Strict 1956 real-person redline**: **PASS** — 0 living or post-1956 deceased real people named or depicted anywhere.
- **Brand/IP & zero-text visual safety**: **PASS** — 0 logos, brand signs, or copyrighted IP mascots across all 60 prompts; non-affiliation & AI-illustration disclaimers included.
- **`nobody: true` ratio & Ada consistency**: **PASS** — `39/60` (`65.0%`) `nobody: true` (100% flag-to-prompt match) + exactly `5` canonical Ada shots (`s05`, `s18`, `s31`, `s46`, `s60`).
- **Thumbnail headline/sub vs. ending payoff**: **PASS** — `heimao-left`, `丸龜製麵狂賣千億？` / `丸龜市零門市卻捨棄中央廚房`, 100% aligned with body mechanisms and ending reconciliation in Marugame City.
- **`claims.md` & `script.md` parity**: **PASS** — 100% synced (`v6` wording polish touched only conversational phrasing in `m009/m033–m035/m045–m046/m048/m053–m054/m061–m062` with zero factual changes).

**VERDICT: PASS**
