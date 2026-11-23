# Independent Fact-Check Audit Report: `curio-w28-komeda-coffee`（客美多咖啡，`N9076`）

- **Auditor**: Independent Fact-Checker
- **Audit Date**: 2026-11-22
- **Files Audited**:
  - `docs/videos/curio-w28-komeda-coffee/video.json` (lines `m001`–`m120`, chapters, `loops`, visual prompts, `thumbnail`, `youtube`, `sources`)
  - `docs/videos/curio-w28-komeda-coffee/claims.md`
  - `docs/videos/curio-w28-komeda-coffee/brief.md`
- **Verification Method**: Independent cross-check via primary Japanese statutory disclosures (FY2026/2 & FY2021/2 決算短信 / 有価証券報告書), JPX TSE listings, Komeda corporate/FC/menu official pages, Doutor Nichires FY2026/2 決算短信, and the Nihon University 2025 academic paper (`食品経済研究` No. 53).

---

## 1. Executive Summary

The script's core financial numbers, TSE sector classification (`卸売業`), Doutor Nichires comparison, FC royalty (`1,500 JPY/seat/month`), domestic store/closure counts (`1,030` / `22` direct / `1,008` FC = `97.9%` / `3` closures = `0.3%`), Taiwan store counts (`36`, 18/18 split, Feb 2018 opening), FY2021/2 COVID resilience (`28,836M` / `5,330M` = `18.5%`), Nihon University 2025 paper findings, historical milestones (`1968`–`2025`), and **1956 real-person redline** are **verified accurate** against primary official sources.

However, this audit identified **2 factual inaccuracies in `video.json` narration lines** (`m047`, `m096`) and **1 entity-name typo in `claims.md`** (line 7) that require correction before sign-off, plus 3 minor precision improvements (`m056`, `s24-coffee-factory-1983`, `s37-simple-kitchen-ops`).

---

## 2. Required Corrections (Blocking Issues)

### Issue 1 — `video.json` Line `m096` (Factual Error: Singapore Acquired vs. Year-End Store Count)
- **Current Text (`m096`)**: `更拓香港上海印尼，併購新加坡三十三店。`
- **Primary Source Fact**: Komeda Holdings FY2026/2 IFRS 決算短信 (p. 2 & p. 4, Note 4) explicitly states that on March 1, 2025 Komeda acquired 70% of `POON RESOURCES PTE. LTD.`, obtaining **30 stores** across three brands (`Kaffe & Toast`, `Saap Saap Thai`, `Ma Mum`), and **subsequently opened 3 new stores organically** during FY2026/2 (`Kaffe & Toast Tanglin Mall`, `Paad Paad Thai IMM`, `Saap Saap Thai White Sands Mall`), bringing Singapore's fiscal year-end store count to **33 stores**.
- **Problem**: Saying `併購新加坡三十三店` conflates the **30 acquired stores** with the **33 year-end total stores**. (`claims.md` line 23 actually notes `新加坡 33 家（含 2025 年 3 月併購 POON 30 家）`, so the error was introduced during script compression.)
- **Required Fix (`m096`)**: Change to accurately distinguish acquisition + expansion, e.g.:
  - `更拓香港上海印尼，新加坡併購展至三十三店。` (or `更拓香港上海印尼，新加坡併購後增至三十三店。`)

### Issue 2 — `video.json` Line `m047` & Prompt `s24-coffee-factory-1983` (Factual/Technical Inaccuracy: Coffee Extraction vs. Roasting)
- **Current Text (`m047`–`m048`)**:
  - `m047`: `早在一九八三年，它就自建製造線統一焙煎供貨。`
  - `m048`: `門市免養高薪咖啡師，加熱就能端出全國一致風味。`
- **Current Visual Prompt (`s24-coffee-factory-1983`)**: `Medium shot inside a traditional Japanese roasting facility with gleaming copper drum roasters tumbling dark aromatic beans...`
- **Primary Source Fact**:
  - Komeda FY2026/2 有価証券報告書 (`S100Y6O9.pdf`) states `ＦＣ加盟店向けのコーヒーの製造・販売を目的として1983年３月に有限会社セントラルコメダが設立されました`.
  - Komeda's official FC website (`https://fc.komeda.co.jp/kutsurogi/`), Integrated Report 2024, and Sept 29, 2026 corporate press release (regarding 2,000 tons/year of spent coffee grounds across its 5 coffee factories) explicitly state that Komeda's coffee factories **inspect the roast condition of beans and centrally brew/extract liquid coffee (`豆の焙煎状態を見極め、丁寧に抽出してお店に届ける`)**, shipping liquid coffee to stores so store staff only heat it up to serve consistent quality.
- **Problem**: Saying `統一焙煎供貨` ("unified roasting supply") misstates the core factory operation (centralized **liquid coffee extraction**, `抽出`/`萃取`) and logically clashes with `m048` (`加熱就能端出` — stores heat liquid coffee, not roasted beans).
- **Required Fix**:
  - `m047`: Change `統一焙煎供貨` to `統一萃取供貨` (e.g., `早在一九八三年，它就自建工廠統一萃取供貨。`).
  - `s24-coffee-factory-1983` prompt: Depict gleaming stainless-steel coffee extraction/brewing tanks and sealed supply containers rather than solely copper bean drum roasters.

### Issue 3 — `claims.md` Line 7 (Company Name Error)
- **Current Text (`claims.md` L7)**: `1. **東利多／客美多控股 FY2026/2 IFRS 連結決算短信（2026 年 4 月 8 日公布，期間 2025/03/01–2026/02/28）**`
- **Problem**: `東利多` is **Toridoll Holdings** (トリドールホールディングス, stock code `3397`, parent of Marugame Seimen), completely unrelated to **Komeda Holdings** (`コメダホールディングス`, stock code `3543`). (`video.json` is not affected.)
- **Required Fix (`claims.md` L7)**: Remove `東利多／`, leaving `1. **客美多控股（コメダホールディングス，3543）FY2026/2 IFRS 連結決算短信...**`.

---

## 3. Recommended Precision Improvements (Non-Blocking Polish)

1. **`video.json` Line `m056`**: `每百日圓國內營收，就淨賺逾二十二日圓。`
   - **Note**: The 22.4% figure (`11,513M / 51,395M = 22.40%`) is the domestic **segment operating profit margin** (`分部營業利益率`) before `-2,231M` unallocated corporate expenses and income taxes — not net profit (`純益`). Using `淨賺` can slightly mislead financially literate viewers. Suggested polish: `每百日圓國內營收，就貢獻逾二十二日圓營業利益。` (or `每百日圓國內營收，就能賺進逾二十二日圓。`).
2. **`video.json` Scene `s37-simple-kitchen-ops` visual prompt**: `...smoothly heating pre-sliced loaves in a steel oven...`
   - **Note**: Komeda's official page (`https://fc.komeda.co.jp/kutsurogi/`) explicitly emphasizes that mountain loaves (`山食パン`) are **sliced at each store** (`できたてのおいしさをお届けするために山食パンはお店でスライスする`), not pre-sliced at the factory. Suggested prompt tweak: change `pre-sliced loaves` to `freshly sliced thick loaves`.
3. **`video.json` Line `m037`**: `一九九三年設公司加盟時，它立下這條鐵律。`
   - **Note**: Primary Yuho filings verify April 1993 as the founding of KK Komeda (`株式会社コメダ`) to formalize FC expansion, though they do not explicitly date when the `1,500 JPY/seat` rate itself was first fixed. Phrasing `一九九三年設公司推進加盟，至今守著這條鐵律。` avoids over-claiming the exact 1993 inception date of the 1,500 JPY figure.

---

## 4. Comprehensive Verification Matrix (All Claims Checked)

| Category | Claim / Metric in Script & Brief | Primary Source Verification | Status |
|---|---|---|---|
| **TSE Sector** | Stock `3543`, TSE Prime (IPO June 2016), sector `卸売業` (Wholesale) not Retail (`m024`, `claims.md`) | JPX 上場会社情報サービス, Nomura, Kabutan, Yahoo Finance JP confirm `3543` = `東証プライム / 卸売業` | **PASS** |
| **FY2026/2 Consolidated** | Revenue `57,225M JPY` (~572億, +21.6%), Op. Profit `9,424M JPY` (~94億, +6.8%), Margin `16.5%` (`m005`–`m007`, `m099`, `m105`) | Komeda FY2026/2 IFRS 決算短信 (2026-04-08, p. 1): `57,225` (+21.6%), `9,424` (+6.8%), `16.5%` (exact `16.47%`). Confirmed record high (Yomiuri Shimbun 2026-04-14, Matsui Sec) | **PASS** |
| **FY2025/2 Consolidated** | Revenue `47,057M JPY`, Op. Profit `8,820M JPY`, Margin `18.7%` (`m007`, `m099`, `claims.md`) | Komeda FY2026/2 IFRS 決算短信 (p. 1): `47,057`, `8,820`, `18.7%` (exact `18.74%`) | **PASS** |
| **Domestic Segment FY2026/2** | Revenue `51,395M` (external `51,374M`), Profit `11,513M`, Margin `22.4%` (`m055`–`m056`) | Komeda FY2026/2 IFRS 決算短信 (p. 5, p. 13): `51,395` / `51,374`, `11,513`; `11,513 / 51,395 = 22.40%` (Note: segment operating profit, see Polish #1 for `m056`) | **PASS** (minor wording note on `m056`) |
| **Wholesale & Revenue Breakdown** | Domestic wholesale `38,490M` (~385億, `74.9%` of domestic external = `近七成五`); total wholesale `39,296M` (`68.7%`); Other incl. royalties `3,906M` (`6.8%` = `<7%`); Direct sales `11,003M` (Dom `6,067M` + Overseas `4,936M`); Dev `1,278M`; Lease `1,742M` (`m044`–`m046`, `claims.md`) | Komeda FY2026/2 IFRS 決算短信 (p. 13 / attachment p. 11): exact match to the single million yen across every line item | **PASS** |
| **Doutor Nichires FY2026/2** | Revenue `159,147M JPY` (~2.78x Komeda = `近三倍`), Op. Profit `10,150M JPY` (`略贏`), Margin `6.4%` (`m008`, `m031`–`m032`) | Doutor Nichires HD (3087) FY2026/2 J-GAAP 決算短信 (2026-04-14, p. 1): `159,147`, `10,150`, `6.4%` (exact `6.38%`); Komeda `16.5% / 6.4% = 2.58x` (`贏同業兩倍`+); Nihon Univ paper confirms Doutor has much higher direct-store share | **PASS** |
| **FC Royalty Terms** | Fixed `1,500 JPY/seat/month` (tax excl.), non-sales-linked; 80 seats = `120,000 JPY/month` (`m038`–`m040`) | `fc.komeda.co.jp` & JFA disclosure `47-1.pdf`: `1席あたり月額1,500円（消費税別）`, `売上に連動しない`; `80 × 1,500 = 120,000` | **PASS** |
| **Japan Komeda Store Counts** | `1,030` total (`22` direct, `1,008` FC = `97.9%`); opened `25`, closed `3` (`3 / 1,008 = 0.298%` → `0.3%`) (`m026`–`m028`, `m075`–`m076`) | Komeda FY2026/2 決算短信 (p. 4): `1,008(22)` → `+25(-)` / `-3(-)` → `1,030(22)`; `1,008 / 1,030 = 97.86%`; Japan all brands `1,067(50)` = `95.3%` FC | **PASS** |
| **Global & Overseas Stores** | Global `1,150` (`103` direct, 58-yr high since 1968); Overseas `83`: Taiwan `36` (`18` direct / `18` FC), HK `7`, Shanghai `5`, Indonesia (Bali) `2`, Singapore `33` (`33` direct) (`m095`–`m097`) | Komeda FY2026/2 決算短信 (p. 4): All counts verified **EXCEPT `m096` erroneously says `併購新加坡三十三店` (actual: 30 acquired via POON + 3 newly opened = 33)** | **FAIL on `m096`** |
| **FY2021/2 COVID Results** | Revenue `28,836M JPY` (`-7.6%`), Op. Profit `5,330M JPY`, Margin `18.5%` (`m083`–`m084`) | Komeda FY2021/2 有価証券報告書 (`S100LFEF.pdf`) & Integrated Report 2023: `28,836百万円` (`7.6%減`), `5,330百万円`; `5,330 / 28,836 = 18.48%` → `18.5%` | **PASS** |
| **Nihon Univ 2025 Paper** | `食品経済研究` No. 53 (Mar 2025), 5 coffee chains compared; 2020/21 business index: Komeda FC `90.0` (surpassed pre-COVID next year 2021/22), Doutor `73.6` (FY2021/2 rev `-26.7%`), Saint Marc direct `67.5` / FC `64.5`, ~3 yrs to recover (`m081`–`m088`) | Directly verified from `hp.brs.nihon-u.ac.jp/~imozuru/img/file11075.pdf` (Adachi & Ishida, Mar 2025, pp. 20–35) & JMR LSI Doutor FY2021/2 analysis (`961億`, `-26.7%`) | **PASS** |
| **Morning Service & Coffee Tickets** | Before 11:00 AM order drink → free thick toast (`山食パン`) or roll + egg / egg paste / Ogura red-bean paste (`m002`, `m115`–`m116`); single-store prepaid coffee ticket (`m071`) | Verified on `komeda.co.jp/menu/morning_komeda.html` & `komeda.com.tw/Qna` | **PASS** |
| **Price Hike & Same-Store Wholesale FY2026/2** | June 2025 store menu price hike, wholesale price raised 2 months later; wholesale same-store sales up ~10% (`m103`, `m105`) | Komeda FY2026/2 決算短信 (p. 5): Menu hiked June 26, 2025; wholesale held flat until Aug 31, raised Sept 1, 2025 (~2-month buffer); FC wholesale same-store YoY `109.5%` (+9.5% = `漲近一成`) | **PASS** |
| **1968–2025 Milestones** | `1968/01` Nagoya Nishi-ku Kikui rice-shop origin (`m011`–`m012`); `1970/02` Nakamura-ku partner/voluntary-chain 1st store (`m017`–`m018`); `1977/02` Ueyama suburban roadside flagship & Shiro-Noir (`m019`–`m021`); `1983/03` coffee factory subsidiary (`m047`); `1993/04` KK Komeda (`m037`); `2003/06` Yokohama (`m053`); `2006/11` Kansai/Nara (`m053`); `2011/10` bread factory acquisition (`有限会社フランスパン`, makes thick toast & 64-layer Danish) (`m049`); `2013/04` 500 stores (`m054`); `2015/07` Chiba bread factory (`m050`); `2016/06` TSE IPO & 700 stores (`m024`); `2018/02` Taiwan 1st store Taipei Nanjing Jianguo & 800 domestic (`m093`); `2019/06` Aomori / 47 prefectures (`m077`); `2023/07` 1,000 stores (`m092`); `2023/08` Kyushu coffee factory (`m050`) | Verified across `komeda-holdings.co.jp/history/`, FY2026/2 Yuho (`S100Y6O9.pdf`), Integrated Reports 2023–2025, `foodrink.co.jp`, `cocotame.jp` — **EXCEPT `m047` wording `統一焙煎供貨` (see Issue 2)** | **FAIL on `m047`** |
| **1956 Real-Person Redline** | Zero living or post-1956 deceased real people named or depicted in narration, metadata, or visual prompts | Full scan of `video.json`, `brief.md`, `claims.md`: Founder (b. 1945), CEOs, and paper authors are **never** named or depicted; only fictional host `Ada` and generic unnamed patrons/staff appear. | **PASS** |

---

## 5. Final Verdict & Exact Fix List

**VERDICT: FAIL**

### Exact Line IDs / Locations Requiring Correction Before Re-Verification:
1. **`video.json` → `m047`** (and visual prompt `s24-coffee-factory-1983`): Replace `統一焙煎供貨` with centralized liquid coffee extraction (`統一萃取供貨`), matching Komeda's actual 1983 central coffee factory operation and `m048` (`加熱就能端出`).
2. **`video.json` → `m096`**: Fix `併購新加坡三十三店` so it does not claim 33 stores were acquired (Komeda acquired **30** POON stores and opened **3** more to reach **33** year-end stores, e.g. `更拓香港上海印尼，新加坡併購展至三十三店。`).
3. **`claims.md` → Line 7**: Remove the erroneous `東利多／` prefix (`東利多` is Toridoll, not Komeda).

*(Optional polish recommended while editing: `m056` clarify operating profit vs. `淨賺`; `s37-simple-kitchen-ops` replace `pre-sliced loaves` with `freshly sliced thick loaves`; `m037` soften exact 1993 attribution for the 1,500 JPY figure.)*
