---
id: 2026-09-16-news-batch-4-2-non-ai
title: News batch 4.2: non-AI technology news
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-17T14:57:20Z
created_at: 2026-09-16T13:21:40Z
completed_at: 2026-09-17T22:13:52Z
branch: claude/news-batch-4-2-tech
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - apps/api/app/guides/content/tech-news-iphone-duo-20260909.json
  - apps/web/public/guides/tech-news-iphone-duo-20260909
  - apps/api/app/guides/content/tech-news-apple-september-hardware-20260909.json
  - apps/web/public/guides/tech-news-apple-september-hardware-20260909
  - apps/api/app/guides/content/tech-news-eu-cra-reporting-20260911.json
  - apps/web/public/guides/tech-news-eu-cra-reporting-20260911
  - apps/api/app/guides/content/tech-news-taiwan-sovereign-ai-corpus-20260915.json
  - apps/web/public/guides/tech-news-taiwan-sovereign-ai-corpus-20260915
  - apps/api/app/guides/content/tech-news-taiwan-6g-spectrum-20260910.json
  - apps/web/public/guides/tech-news-taiwan-6g-spectrum-20260910
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-20260623.json
  - apps/web/public/guides/tech-news-taiwan-matsu-cable-20260623
  - apps/api/app/guides/content/tech-news-apple-eu-business-terms-20260818.json
  - apps/web/public/guides/tech-news-apple-eu-business-terms-20260818
  - apps/api/app/guides/content/tech-news-windows-project-zenith-20260904.json
  - apps/web/public/guides/tech-news-windows-project-zenith-20260904
  - apps/api/app/guides/content/tech-news-pixel-drop-20260915.json
  - apps/web/public/guides/tech-news-pixel-drop-20260915
  - apps/api/app/guides/content/tech-news-apple-m6-m5-ultra-20260825.json
  - apps/web/public/guides/tech-news-apple-m6-m5-ultra-20260825
  - apps/api/app/guides/content/tech-news-nvidia-cuda-q-20260914.json
  - apps/web/public/guides/tech-news-nvidia-cuda-q-20260914
  - apps/api/app/guides/content/tech-news-nvidia-mediatek-20260831.json
  - apps/web/public/guides/tech-news-nvidia-mediatek-20260831
  - apps/api/app/guides/content/tech-news-nvidia-vera-rubin-20260915.json
  - apps/web/public/guides/tech-news-nvidia-vera-rubin-20260915
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/web/public/guides/tech-news-2026-index
  - docs/tech-news-2026
---

# News batch 4.2: non-AI technology news

## 站主圈選結果（2026-09-16）

站主的指示是「**幣圈和科技的先全部寫，AI 挑補漏那幾則**」。

**科技：候選清單全部寫，13 篇。**

數發部那四則拆成三篇：主權 AI 語料庫把 2026-07-24 的客語語料當前情併進 2026-09-15 那篇（T4a），
6G 研討會（T4b）與臺馬四號海纜（T4c）各自一篇。
NVIDIA 三則裡的 CUDA-Q（量子）、聯發科、Vera Rubin 都放科技垂直；
**NVIDIA 併購 Hugging Face 放 AI 垂直**，不要兩邊都寫。

**T7 September Pixel Drop 份量偏輕**，候選清單原本建議當次要新聞。
站主說全部寫，所以照寫，但研究階段要先判斷份量夠不夠獨立成篇，不夠就回報。

| 代號 | 事件日 | slug | 題目 |
| --- | --- | --- | --- |
| T1 | 2026-09-09 | `tech-news-iphone-duo-20260909` | Apple iPhone Duo 折疊機 |
| T2 | 2026-09-09 | `tech-news-apple-september-hardware-20260909` | 9/9 發表會的其餘硬體（只寫硬體） |
| T3 | 2026-09-11 | `tech-news-eu-cra-reporting-20260911` | 歐盟《網路韌性法》通報義務上路 |
| T4a | 2026-09-15 | `tech-news-taiwan-sovereign-ai-corpus-20260915` | 數發部主權 AI 語料庫民間徵集（含 7/24 客語語料） |
| T4b | 2026-09-10 | `tech-news-taiwan-6g-spectrum-20260910` | 數發部頻譜政策與 6G 國際研討會 |
| T4c | 2026-06-23 | `tech-news-taiwan-matsu-cable-20260623` | 臺馬四號海纜與馬祖微波站 |
| T5 | 2026-08-18 | `tech-news-apple-eu-business-terms-20260818` | Apple 調整歐盟 App 商業條款 |
| T6 | 2026-09-04 | `tech-news-windows-project-zenith-20260904` | Windows Project Zenith |
| T7 | 2026-09-15 | `tech-news-pixel-drop-20260915` | September Pixel Drop |
| T8 | 2026-08-25 | `tech-news-apple-m6-m5-ultra-20260825` | Apple M6 與 M5 Ultra（站主升級為重要新聞） |
| T9 | 2026-09-14 | `tech-news-nvidia-cuda-q-20260914` | NVIDIA CUDA-Q 量子運算平台 |
| T10 | 2026-08-31 | `tech-news-nvidia-mediatek-20260831` | NVIDIA 與聯發科深化合作 |
| T11 | 2026-09-15 | `tech-news-nvidia-vera-rubin-20260915` | AI Infra Summit：Vera Rubin 與 DSX |

`scope` 已經照這份清單逐篇填好（每篇兩行）。工作區是 `docs/tech-news-2026/`。

## Why

既有 38 篇 `ai-news-*` 幾乎全是 AI 模型發布，硬體／晶片／消費電子／電信／法規
只有 `ai-news-nvidia-rubin-20260105` 與 `ai-news-siri-ai-ios-27-20260914` 兩篇沾到邊。
`tech` 父主題與 `tech-news` 子主題由 PR #536 帶進來。

## 界線

見 [`docs/news-2026-batch-4/tech.md`](../../docs/news-2026-batch-4/tech.md)：
**不寫購買建議**（不寫「該不該買」「值不值得升級」），
廠商的效能宣稱一律歸因（「Apple 表示」），本站沒有實測；
資安題目寫影響範圍與該做什麼，**不寫攻擊手法與入侵指標**。

**不帶 `finance` 主題，所以不要自己加投資免責。**

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

## 狀態（2026-09-18）：已合併（PR #546）並匯入發布，結案

站主 2026-09-17 說「好 開始」後開工，分支 `claude/news-batch-4-2-tech`。完整交接（每篇的查核與審稿數字、留給站主決定的事、
這一輪學到的）在 [`docs/news-2026-batch-4/HANDOVER.md`](../../docs/news-2026-batch-4/HANDOVER.md) 第 1b、3、4 節，這裡只記票的狀態。
上面「認領還要等兩件事」與「已知會擋路的兩件事」是開工前的舊紀錄：4.0 已 done、content 目錄的鎖已讓出；
Windows 上出圖用 `CHROMIUM_BIN` 指到 Playwright 的 headless shell 即可。

- [x] 十三篇 zh-TW 撰稿（sonnet）並經**兩輪**獨立查核（opus；第一輪每篇改 11–30 處、第二輪再改 8–18 處）；報告在 `docs/news-2026-batch-4/factcheck-draft/tech-news-*.md`。
- [x] 協調者通讀十三篇、`hero.alt`／`image.alt` 改成實際畫面；三篇補中英文間空格並刪重複敘述騰字數（不刪但書）；CRA 篇的法條來源換成 EUR-Lex ELI 網址。
- [x] 索引 `tech-news-2026-index`（`build_tech_index.py` 產生 zh-TW，只重述十三篇已查核的事實；沒有免責 callout）。
- [x] 四語翻譯（sonnet，14 位）併入；逐語審稿 4 語言 × 3 組共 12 位 opus 代理，採用 799 筆（`translation-corrections.json`），
      另對錯字最多的馬祖海纜日文做第二次審稿（5 筆）；協調者自己的修訂在 `coordinator-corrections.json`。
- [x] 工具：`verticals.py` tech `order_base=300`、`check_article.py` 的 `RELATED`、`build_assets.py` 14 個主圖構圖、`align_links.py --only`、
      新增 `build_tech_index.py`、`translation_checks.py`、`normalize_locales.py`、`space_cjk.py`、`sync_captions.py`；代理規格在 `agents/tech/`。
- [x] `related`（延伸閱讀）、`pack_cli relink`、全垂直出圖與 contact sheet、`manifest.json`。
- [x] 驗證：十三篇 `check_article.py --full --assets` OK、索引五語 schema＋lint OK、`pack_cli lint --kind life` 0 error、
      `tests/test_guides_content_pack.py`＋`test_guides_content_links.py`＋`test_guides_pack_ingest.py` 通過、`npm run check:tasks`。
- [x] 合併：站主 2026-09-18（台北）明確選了「合併並發布」；PR #546 以 `--match-head-commit 17523605…` squash 為 `88e4cd1a`，合併後 main 的樹與 PR head 逐位元相同。
- [x] 發布前重開活頁面：EUR-Lex 的 ELI 網址 2026-09-17T21:56Z 回 200／974,702 bytes，讀到 Article 14 與「11 September 2026」；
      帶 `Accept-Language: zh-TW` 同樣 200 HTML，舊的 CELLAR 網址同條件回 404。
- [x] 部署：部署前查過沒有 hold 檔、沒有進行中的分段發布、沒有 migration，待部署的只有 #545、#546；
      `/root/deploy-travel-scanner.sh`（`deploy_20260917_220710`，22:07–22:10 UTC）health 3/3、alembic `0080_crypto_and_tech_topics`、首頁 200。
- [x] 匯入發布：`guides-import --slug` ×14。腳本先跑 `--dry-run --publish` 核對計畫＝14 篇／70 個 create／沒有別的 slug 才 `--publish`；
      結果 `taxonomy_updated` 13 篇（延伸閱讀）、`failed: null`。
- [x] 正式站驗證（User-Agent `Mokaair-editorial`）：70 個網址全部 200、沒有 noindex、有 `#article-summary`、JSON-LD 有 `FAQPage` 與 `abstract`、
      canonical 正確、主圖 70 張都 200；五語 sitemap 70／70 收錄；索引頁連到 13 篇，Vera Rubin 那篇的延伸閱讀看得到 `ai-news-nvidia-rubin-20260105`。
