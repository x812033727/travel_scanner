---
id: 2026-09-16-news-batch-4-1-crypto-regulation
title: News batch 4.1: crypto regulation, technology and industry news
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-17T10:39:10Z
created_at: 2026-09-16T13:21:39Z
completed_at: 2026-09-17T12:02:20Z
branch: claude/brave-hopper-8ezxba
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - apps/api/app/guides/content/crypto-news-taiwan-vasp-act-20260630.json
  - apps/web/public/guides/crypto-news-taiwan-vasp-act-20260630
  - apps/api/app/guides/content/crypto-news-mica-transition-ends-20260701.json
  - apps/web/public/guides/crypto-news-mica-transition-ends-20260701
  - apps/api/app/guides/content/crypto-news-sec-crypto-interpretation-20260323.json
  - apps/web/public/guides/crypto-news-sec-crypto-interpretation-20260323
  - apps/api/app/guides/content/crypto-news-sec-regulation-crypto-assets-20260821.json
  - apps/web/public/guides/crypto-news-sec-regulation-crypto-assets-20260821
  - apps/api/app/guides/content/crypto-news-eba-psd2-mica-20260212.json
  - apps/web/public/guides/crypto-news-eba-psd2-mica-20260212
  - apps/api/app/guides/content/crypto-news-genius-act-occ-20260302.json
  - apps/web/public/guides/crypto-news-genius-act-occ-20260302
  - apps/api/app/guides/content/crypto-news-stablecoin-aml-20260410.json
  - apps/web/public/guides/crypto-news-stablecoin-aml-20260410
  - apps/api/app/guides/content/crypto-news-fdic-genius-act-20260410.json
  - apps/web/public/guides/crypto-news-fdic-genius-act-20260410
  - apps/api/app/guides/content/crypto-news-ncua-genius-act-20260518.json
  - apps/web/public/guides/crypto-news-ncua-genius-act-20260518
  - apps/api/app/guides/content/crypto-news-jfsa-working-group-20260216.json
  - apps/web/public/guides/crypto-news-jfsa-working-group-20260216
  - apps/api/app/guides/content/crypto-news-jfsa-cybersecurity-20260723.json
  - apps/web/public/guides/crypto-news-jfsa-cybersecurity-20260723
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/web/public/guides/crypto-news-2026-index
  - docs/crypto-news-2026
---

# News batch 4.1: crypto regulation, technology and industry news

## 站主圈選結果（2026-09-16）

站主的指示是「**幣圈和科技的先全部寫，AI 挑補漏那幾則**」。

**幣圈：候選清單 C1–C11 全部寫，11 篇。**

C6–C9 是美國 GENIUS Act 的四個主管機關版本，候選清單原本寫「可以合成一篇」。
站主說全部寫，所以**四篇分開**，各自寫自己主管機關管到誰、要求什麼；
四篇互相連結，不要四篇重複解釋一次 GENIUS Act 是什麼。

**沒有納入**：新加坡 MAS 那則（這個容器連不到 MAS，兩個網址都回 service unavailable）。
要寫必須在別的環境先驗過，現在納入就是照抄線索。
以太坊 2026 年升級那則維持 ❌ 查否：官方把日期列為 TBD，整合站的 Q3 2026 沒有官方依據。

| 代號 | 事件日 | slug | 題目 |
| --- | --- | --- | --- |
| C1 | 2026-06-30 | `crypto-news-taiwan-vasp-act-20260630` | 台灣《虛擬資產服務法》三讀通過 |
| C2 | 2026-07-01 | `crypto-news-mica-transition-ends-20260701` | 歐盟 MiCA 過渡期結束 |
| C3 | 2026-03-23 | `crypto-news-sec-crypto-interpretation-20260323` | CFTC 與 SEC 聯名的加密資產證券法解釋令 |
| C4 | 2026-08-21 | `crypto-news-sec-regulation-crypto-assets-20260821` | SEC 提出 Regulation Crypto Assets（草案） |
| C5 | 2026-02-12 | `crypto-news-eba-psd2-mica-20260212` | EBA 對 PSD2 與 MiCA 銜接的意見書 |
| C6 | 2026-03-02 | `crypto-news-genius-act-occ-20260302` | GENIUS Act 落地：OCC |
| C7 | 2026-04-10 | `crypto-news-stablecoin-aml-20260410` | 穩定幣發行商的洗錢防制與制裁遵循 |
| C8 | 2026-04-10 | `crypto-news-fdic-genius-act-20260410` | GENIUS Act 落地：FDIC |
| C9 | 2026-05-18 | `crypto-news-ncua-genius-act-20260518` | GENIUS Act 落地：NCUA |
| C10 | 2026-02-16 | `crypto-news-jfsa-working-group-20260216` | 日本 FSA 金融審議會工作小組報告 |
| C11 | 2026-07-23 | `crypto-news-jfsa-cybersecurity-20260723` | 日本 FSA：加密資產業者的資安問題與對策 |

`scope` 已經照這份清單逐篇填好（每篇兩行）。工作區是 `docs/crypto-news-2026/`。

## Why

站上目前**零篇**幣圈內容。這是全新的垂直領域，
詞彙（`crypto` 掛在 `finance` 底下）與免責機制（`finance_no_disclaimer`，error 級）
都由 PR #536 帶進來了，候選題目也查證完畢。

## 界線（站主定的，不是建議）

**只寫法規、技術與產業，不碰行情。** 明文禁止：幣價、漲跌幅、市值、交易量、
ETF 資金流、買賣時機、殖利率／質押報酬／空投、任何具體標的、交易所費率比較。
完整規則見 [`docs/news-2026-batch-4/crypto.md`](../../docs/news-2026-batch-4/crypto.md)。

**每篇必帶免責 callout**，逐字含該語言的標記字串
（`pack_ingest.FINANCE_DISCLAIMER_MARKERS`，五語各一）。
`finance_no_disclaimer` 是 **error**，CI 會擋。

**機器只擋得住樣板。**「有沒有變相推薦標的」「風險講得夠不夠」要人逐篇看，
這是這張票 Definition of done 的一部分，不要指望 lint。

## scope 已填好，但認領還要等兩件事

`scope` 已經照上面的圈選結果逐篇填好。認領之前還缺兩件事：

1. **`depends_on` 的 4.0 還沒 done**（`2026-09-16-news-batch-4-0-crypto-and`，
   目前 `review`，等 PR #536 合併）。詞彙、migration 與財經免責 lint 都在那張票裡，
   沒有它寫出來的內容包過不了 lint。
2. **`apps/api/app/guides/content` 整個目錄被
   `2026-09-15-content-summary-howto-and-life`（`in-progress`）持有**，
   在 2026-09-17T03:39Z 變 stale。

**兩件都不要用 `--force` 繞過。** 第 1 條會讓內容包 lint 失敗，
第 2 條正是用來擋兩個 agent 互相覆蓋的規則。

在那之前可以做、而且已經在做的是**研究**：工作區目錄不在任何人的 scope 裡，
研究紀錄先寫在那裡，鎖一讓出來就能直接開稿。

## 流程

照 [`docs/news-2026-batch-4/BRIEF.md`](../../docs/news-2026-batch-4/BRIEF.md)：
一篇一個撰稿代理 → **獨立查核代理**（不可省：批次 3 每篇 56–102 條主張、
每篇都改了 15–38 處）→ 翻譯（五語）→ 逐語系審稿 → 圖像 → 索引 → 驗證。

每篇必帶 `summary` 與 `faq` 區塊——這批是站上第一批全面帶的
（845 篇 life 只有 5 篇有 summary、1 篇有 faq）。

## 已知會擋路的兩件事

- **這個容器沒有 headless 瀏覽器**，而 `build_assets.py` 要靠它把 hero SVG 轉成 JPEG。
  圖像階段開始前先確認 Chromium 可用（環境有 `/opt/pw-browsers/chromium`，
  但 `build_assets.py` 目前找的是 Edge／Chromium 的路徑，要確認能不能指過去）。
- **`pack_cli ingest` 會拒絕帶子主題的內容包**（`_known_topics()` 只回父主題）。
  批次 3 是直接寫進 `content/` 不走 `ingest`，這批照做。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life    # 0 error
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
npm run check:tasks
```

## 進度與交接（2026-09-17，claude-fable-5-1 接手 PR #544 後）

完整交接在 [`docs/news-2026-batch-4/HANDOVER.md`](../../docs/news-2026-batch-4/HANDOVER.md)，這裡只記票的狀態。

- [x] 十一篇 zh-TW 全部撰稿並經獨立查核（C4、C7、C9 做了第二輪）；報告在 `docs/news-2026-batch-4/factcheck-draft/`。
- [x] 十篇五語併入、主圖與圖解五語產出（C1–C6、C8–C11）。
- [x] 索引 `crypto-news-2026-index` 的 zh-TW（另由獨立代理拿十一篇逐句核對，14 條發現全數套用）與 en。
- [x] C7 `crypto-news-stablecoin-aml-20260410` 的 ja、ko，索引的 ja、ko、zh-CN（第二個 session，協調者用 `l10n.py` 逐格翻，再交獨立審稿）。
- [x] 逐語審稿：4 語言 × 3 組共 12 位代理，採用 706 筆、退回 1 筆（`docs/news-2026-batch-4/translation-corrections*.json`），
      協調者另有 54 筆（`coordinator-corrections.json`：跨組用語、韓文站方語氣、免責句、11 個譯文標題）。
- [x] 審稿抓到一個兩輪查核都放過的**原稿事實錯誤**（日本審議會那篇：發行人未募資時是業者自行編製並公表），回金融廳 PDF 查證後五語改正、研究紀錄加註。
- [x] 同群文章互連用內容包的 `related`；`pack_cli relink` 已套用（165 條）；`autolink` 只找到法條引文裡的「澳門」→ 澳門一日遊，不套用。
- [x] 全垂直的 `manifest.json` 與 contact sheet，五語逐張看過，審稿改過圖上短字後重出一次。
- [x] 驗證：十一篇 `check_article.py --full --assets` OK、索引五語過 schema 與 lint、`pack_cli lint --kind life` 0 error、內容包測試 53 passed。
- [x] 站主 2026-09-17 指示合併 PR #544 並「匯入發布這十二篇」，視為驗收；審稿代理回報的繁中用詞疑點仍列在 HANDOVER 2.1 供日後修訂，沒有一項是事實錯誤。
- [x] 部署、匯入與發布（2026-09-17，UTC）：
      - 勘查：沒有 hold 檔、沒有進行中的分段發布、正式站只落後 main 一個 commit（#544 的 `f8938dc6`）、沒有 migration。
      - 部署：`/root/deploy-travel-scanner.sh`，11:53–11:56，health 3/3、alembic `0080_crypto_and_tech_topics (head)`，log `deploy_20260917_115306`。
      - 匯入：`guides-import --slug` ×12。先 `--dry-run --publish` 由腳本核對計畫剛好是 12 篇、60 個 `create`、沒有別的 slug，才執行 `--publish`：
        12 篇 × 5 語系全數 created＋published，`taxonomy_updated` 10 篇（`related` 第二輪套用），`failed: null`。
      - 公開站驗證：60 個網址（12 篇 × zh-TW／en／ja／ko／zh-CN）全部 HTTP 200、沒有 `noindex`、有 `#article-summary`；
        OCC 篇頁面連到另外三篇 GENIUS Act 文章與索引；`FAQPage` 與 `abstract` 結構化資料都在；主圖與圖解 200；
        五個語系的 `life-<locale>.xml` 子 sitemap 都收錄十二篇；`/zh-TW/life` 最新新聞列出現幣圈文章。
      - 活資料：C2–C11 的查核日就是發布當天（2026-09-17），C1 是前一天；沒有另外重抓。之後若五份美國草案出現定案規則或展延，要照 HANDOVER 2.2 回頭改。

第一個 session 停手的原因是帳號用量上限；第二個 session（2026-09-17，同為 `claude-fable-5-1`）重新認領並做到這裡。
發布完成後結案。

### 規格衝突（`BRIEF.md` 要求記進 tasks/）

1. `corrections-crypto.md` 寫查核日一律填 2026-09-16；`BRIEF.md` 寫實際查證當天。C2–C11 當天重抓重讀，用 **2026-09-17**。
2. `corrections-crypto.md` 的 stablecoin-aml must_fix 2 要把 1022.220 改成 1020.220、EBA must_fix 8 要補 `and the` 的空格；
   `BRIEF.md` 型態 7 要求照印來源並說明。照 BRIEF：兩種寫法並列、不代來源訂正（EBA 那個空格三種抽文法都印 `andthe`，是來源排版）。
3. `corrections-crypto.md` 傾向把 FDIC 的事件日訂為理事會通過日 04-07；站主圈選的 slug 是 20260410。
   五份美國聯邦規則一律以**聯邦公報刊登日**為事件日，另一個日期明寫在文章裡。
4. 撰稿規格原本寫「生效日一律寫公式」；FDIC 的聯邦公報文件自己印了 `January 18, 2027 … if earlier`。
   改成「照來源印的寫，來源沒印才只寫公式，不可自己換算」。
5. `RELATED`：C1 的第二個連結從 `epayment-vs-ewallet-taiwan`（只有 zh-TW）改成 MiCA 那篇，四個譯文才有標題可連。
