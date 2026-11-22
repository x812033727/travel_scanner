# Independent Fact-Check & Redline Audit (Round 1) — `curio-w27-marugame-seimen` (N9105)

**Auditor**: Independent Fact-Checker W27 v1 (read-only research subagent)
**Date**: 2026-11-22
**Result**: **VERDICT: FAIL** (defects logged below and resolved in v4 before Round 2 re-verification in `verify-2.md`)

## Verified Core Claims (PASS)
- Toridoll Holdings FY2026/3 IFRS (`278,715M JPY` consolidated revenue, `21,460M JPY` consolidated business profit; Marugame domestic `137,193M JPY` revenue / `21,955M JPY` business profit / `16.0%` margin / `887` 100% company-owned stores).
- Yoshinoya Holdings FY2026/2 Hanamaru segment (`32,991M JPY` revenue, `2,427M JPY` segment profit).
- Kagawa Prefecture `1` store (`Takamatsu Rainbow Street`) & Marugame City `0` stores; Apr 2022 revitalization pact; >100M JPY corporate hometown tax; Nov 2025 Marugame Udon Festival (0 bowls sold by Marugame).
- Porter Prize 2020 & Japan Service Award: 100% domestic wheat, demand-forecast batch boiling (10–15 min), 45-day limited menu cycle, urban compact store 1.3x sales, 2020 base Kamaage 290 JPY vs 570 JPY ticket, auto-controlled kama (-31.3% electricity, -47.6% water, FY2019 METI Minister's Prize), Men-shokunin 2016 launch (30% / 10% pass rates, sole Men-sho, Mar 2024 100% store placement with 1,632 artisans, maintained Feb 2026).
- Strict 1956 real-person redline: PASS (0 living/post-1956 deceased people named or depicted).
- Brand/IP visual safety: PASS.

## Round 1 Defects (All Fixed in v4)
1. **Revenue vs. profit conflation (`m002`, `m008`, `s01.chapter`, `thumbnail.data.headline`, `youtube.title`)**: Changed `"賺"` to revenue wording (`"狂賣"`, `"年營收"`, `"年賣"`) so 1,372億日圓 is unambiguously revenue, never profit.
2. **Overseas store attribution & London timeline (`m088`)**: Split 2013 (Taipei/Indonesia) from 2021 (London) and attributed >900 overseas stores explicitly to `"母集團"`.
3. **Missing currency `"日圓"` (`m008`, `m045`, `m081`, `m082`)**: Explicitly added `"日圓"` on JPY figures.
4. **Unsourced/imprecise details (`m012`, `m031`, `m067`, `m068`, `m082`)**: Removed unsourced `"只想開三家"`, clarified Jul 2011 Marugame 500 stores / 47 prefectures, changed `"反聘"` to `"改聘"` with 2020 anchor on `2,200+`, broadened `"鄰校運動會"` to `"在地活動"`, and changed `"近九倍"` to `"逾九倍"` (`9.046×`).
5. **Housekeeping (`loops[2]`, `s12`, `brief.md`)**: Aligned `loops[2]`, added anonymous diners to `s12`, synced `brief.md`.
