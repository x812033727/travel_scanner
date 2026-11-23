# Round-2 Independent Fact-Check Audit Report: `curio-w28-komeda-coffee`（客美多咖啡，`N9076`）

- **Auditor**: Independent Round-2 Fact-Checker
- **Audit Date**: 2026-11-22
- **Files Audited**:
  - `docs/videos/curio-w28-komeda-coffee/verify-1.md` (Round-1 baseline)
  - `docs/videos/curio-w28-komeda-coffee/claims.md`
  - `docs/videos/curio-w28-komeda-coffee/video.json` (v6: 60 scenes `s01`–`s60`, 120 narration lines `m001`–`m120`, 13 `loops`, `thumbnail`, `youtube`, 14 `sources`)
  - `docs/videos/curio-w28-komeda-coffee/script.md` (exact 120-line parity check against `video.json`)
- **Verification Method**: Independent re-verification of all Round-1 fixes, full 120-line & 60-prompt audit, automated parity/redline scan, and primary-source cross-check against Komeda Holdings (`3543`) FY2026/2 & FY2025/2 IFRS 決算短信 / 有価証券報告書, Doutor Nichires HD (`3087`) FY2026/2 決算短信, Komeda FY2021/2 EDINET filing (`S100LFEF`), JPX sector listing (`卸売業`), Komeda FC terms, and Nihon University (`食品経済研究` No. 53).

---

## 1. Round-1 Issue Closure Verification

Every blocking issue and non-blocking polish item flagged in `verify-1.md` has been cleanly fixed in both `claims.md` and `video.json` (v6) / `script.md`:

| # | Round-1 Finding (`verify-1.md`) | Verified Fix in Current Files | Status |
|---|---|---|---|
| **Blocking 1** | Old `m096` erroneously stated `併購新加坡三十三店` (conflating 30 acquired POON stores with 33 year-end total stores) | `video.json` `m084` (`s42-36-taiwan-stores`) & `script.md` L225 now read `更拓進港滬印尼，並在新加坡併購展至三十三店。`; `claims.md` L23 explicitly states `新加坡 33 家（含 2025 年 3 月併購 POON 30 家）` (30 acquired + 3 organic = 33). | **FIXED** |
| **Blocking 2** | Old `m047` (`統一焙煎供貨`) & old `s24` prompt (copper bean roasters only) misstated the 1983 factory's centralized liquid coffee extraction | `video.json` `m035` (`s18-coffee-extract-1983`) now reads `一九八三年它設專廠，統一萃取液態咖啡直送。` (aligned with `m036` `現場加熱就能維持一致風味`); prompt `s18-coffee-extract-1983` depicts `gleaming stainless brewing vessels, glass sight tubes of rich dark liquid brew, and sealed steel supply barrels`; `youtube.description` cites `咖啡萃取工廠`. | **FIXED** |
| **Blocking 3** | `claims.md` L7 had stray `東利多／` prefix (Toridoll `3397`, unrelated to Komeda `3543`) | `claims.md` L7 now reads `1. **客美多控股（3543）FY2026/2 IFRS 連結決算短信（2026 年 4 月 8 日公布，期間 2025/03/01–2026/02/28）**`; zero occurrences of `東利多` or `トリドール` remain anywhere across all files. | **FIXED** |
| **Polish 1** | Old `m056` used `淨賺逾二十二日圓` for domestic segment operating profit margin (`22.4%`) | `video.json` `m042` (`s21-aligned-flywheel-22pct`) now reads `單看日本事業，分部利益率竟破百分之二十二！` (`11,513M / 51,395M = 22.40%` domestic segment operating profit margin). | **FIXED** |
| **Polish 2** | Old `s37-simple-kitchen-ops` prompt said `pre-sliced loaves` (stores actually slice mountain loaves on-site) | `video.json` `s30-simple-kitchen-ops` prompt now reads `freshly sliced thick loaves`. Zero occurrences of `pre-sliced` remain. | **FIXED** |
| **Polish 3** | Old `m037` attributed the `1,500 JPY/seat` rate's exact inception to 1993 | `video.json` `m015` (`s08-1970-1993-fc-start`) now states `一九七零年開首間加盟，九三年公司化擴張。`, cleanly decoupled from the current FC royalty terms in `m026`–`m028`. | **FIXED** |

---

## 2. Full Quantitative, Comparison & Structural Audit (`video.json` v6 & `claims.md`)

| Audit Dimension | Verified Figures / Claims in `video.json` (v6) & `claims.md` | Primary Source Cross-Check | Status |
|---|---|---|---|
| **Komeda FY2026/2 Consolidated** | Revenue `57,225M JPY` (`五百七十二億`, +21.6%), Op. Profit `9,424M JPY` (`九十四億`, +6.8%), Margin `16.5%` (exact `16.47%`) (`m005`–`m007`, `m031`, `m097`) | Komeda FY2026/2 IFRS 決算短信 (2026-04-08) & Yuho (`S100Y6O9`): exact match | **PASS** |
| **Komeda FY2025/2 Consolidated** | Revenue `47,057M JPY`, Op. Profit `8,820M JPY`, Margin `18.7%` (exact `18.74%`, `近兩成`) (`m007`, `m087`, `claims.md` L9–L11) | Komeda FY2026/2 & FY2025/2 IFRS 決算短信: exact match | **PASS** |
| **Domestic vs. Overseas Segment (FY2026/2)** | Domestic rev `51,395M` (external `51,374M`), segment profit `11,513M`, margin `22.40%` (`破百分之二十二`, `m042`); Overseas rev `5,851M`, segment profit `142M` (`2.4%`, incl. Singapore POON direct-store mix & raw-material cost pressure explaining consolidated margin dip `18.7% -> 16.5%`, `m087`–`m088`) | Komeda FY2026/2 Yuho Segment Note (`国内事業` / `海外事業`): exact match | **PASS** |
| **Revenue Breakdown (FY2026/2)** | Consolidated wholesale `39,296M` (`三百九十三億`, `68.7%` = `近七成`); domestic wholesale `38,490M` (`74.9%` of domestic external = `近七成五`); other incl. royalties `3,906M` (`6.8%` = `不到百分之七`); direct sales `11,003M` (dom `6,067M` + overseas `4,936M`); dev `1,278M`; lease `1,742M` (`m032`–`m034`, `claims.md` L14–L17) | Komeda FY2026/2 IFRS 決算短信 Revenue Disaggregation: exact match | **PASS** |
| **Doutor Nichires FY2026/2 Comparison** | Revenue `159,147M JPY` (`2.78x` Komeda = `近三倍`), Op. Profit `10,150M JPY`, Margin `6.4%` (exact `6.38%`), Komeda margin `2.58x` higher (`贏同業兩倍`+) (`m008`, `m023`, `claims.md` L29–L33) | Doutor Nichires HD (`3087`) FY2026/2 J-GAAP 決算短信 (2026-04-14): exact match | **PASS** |
| **TSE Sector Classification** | Stock `3543`, TSE Prime, official 33-sector classification `卸売業` (Wholesale), not Retail/Foodservice (`m009`, `m017`–`m018`, `youtube.description`) | JPX Listed Company Info (`3543`): `東証プライム / 卸売業` | **PASS** |
| **FC Royalty Terms** | Fixed `1,500 JPY`/seat/month (tax excl.), non-revenue-linked; `80` seats = `120,000 JPY`/month ex-tax (`m027`–`m028`, `claims.md` L37) | `fc.komeda.co.jp` & JFA `47-1.pdf`: `1席あたり月額1,500円（消費税別）`, `80 × 1,500 = 120,000` | **PASS** |
| **Store Counts & Closure Rate** | Global `1,150` (`103` direct, 58-year high since 1968: `2026 - 1968 = 58`); Japan Komeda `1,030` (`22` direct, `1,008` FC = `97.9%`; `+25 / -3`, closure rate `3 / 1,008 = 0.30%`); Japan all brands `1,067` (`50` direct, `95.3%` FC); Overseas `83`: Taiwan `36` (`18` direct / `18` FC), Singapore `33` (`30` POON acquired + `3` organic), HK `7`, Shanghai `5`, Bali `2` (`m019`–`m020`, `m061`–`m062`, `m083`–`m085`, `m108`) | Komeda FY2026/2 IFRS 決算短信 Store Summary: exact match | **PASS** |
| **COVID Stress Test (FY2021/2) & Nihon Univ 2025 Paper** | FY2021/2 rev `28,836M` (`-7.6%`), op profit `5,330M` (`五十三億`), margin `18.5%` (exact `18.48%`); Nihon Univ `食品経済研究` No. 53 (Mar 2025) 5-chain comparison: Komeda FC index `90.0` (surpassed pre-COVID in 1 yr) vs. Doutor `73.6` (`-26.4%`) and Saint Marc `67.5` / `64.5` (`-32.5%` to `-35.5%`), urban peers ~3 yrs to recover (`m069`–`m076`) | Komeda FY2021/2 EDINET Yuho (`S100LFEF`) & Nihon Univ 2025 paper: exact match | **PASS** |
| **Historical Timeline & 2025 Pricing** | `1968/01` Nagoya rice-shop origin (`m011`–`m012`); `1970/02` 1st FC & `1993/04` KK Komeda (`m015`); `1977/02` suburban roadside prototype & Shiro-Noir (`m045`, `m052`); `1983/03` coffee extraction factory (`m035`); `2003` Yokohama, `2006` Kansai, `2011` bread factory acquisition, `2013` 500 stores, `2015–2023` Chiba/Okinawa/Kyushu regional factories, `2018` Taipei 1st store, `2019/06` Aomori / all 47 prefectures (`m065` uses standard spoken shorthand `全四十七縣` for Japan's 47 prefectures; `claims.md` L54 states `47 都道府縣`), `2023/07` 1,000 stores; `2025/06` menu hike with 2-month wholesale hike delay (`2025/09`) & `+9.5%` (`漲近一成`) FC wholesale same-store growth (`m093`–`m097`) | Komeda corporate history, Yuho, & FY2026/2 earnings release: exact match | **PASS** |
| **1956 Real-Person Redline** | Automated & manual scan of all 120 lines, 60 visual prompts, 13 `loops`, `thumbnail`, `youtube` metadata, `sources`, `claims.md`, and `script.md`: **ZERO** living or post-1956 deceased real people named or depicted (founder, CEOs, CFO, and academic authors are completely omitted; only fictional host `Ada` and generic unnamed patrons/staff appear). | Full text & prompt audit | **PASS** |
| **File & Loop Parity** | `video.json` has 60 scenes (`42/60 = 70.0%` `nobody: true`), 120 lines (`m001`–`m120`), 13 valid `loops` (all `setup` and `payoff` IDs resolve accurately to matching narration lines), and 100% line-by-line text parity with `script.md`. | Automated verification script | **PASS** |

---

## 3. Final Verdict

All Round-1 blocking and non-blocking items are cleanly resolved, every quantitative figure, comparison, structural claim, timeline milestone, and visual prompt is verified accurate against primary sources, and the 1956 real-person redline is strictly satisfied across every file.

**VERDICT: PASS**
